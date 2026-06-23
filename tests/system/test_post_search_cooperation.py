import base64
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib import request, error
from urllib.parse import quote_plus
from uuid import uuid4
import pytest


API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
RABBITMQ_MGMT_URL = os.getenv("RABBITMQ_MGMT_URL")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
SYSTEM_TEST_TIMEOUT_SECONDS = int(os.getenv("SYSTEM_TEST_TIMEOUT_SECONDS"))
ELASTICSEARCH_POST_INDEX = os.getenv("ELASTICSEARCH_POST_INDEX")

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: Any

def _http_json(method: str, url: str, payload: dict[str, Any] | None = None, *, headers: dict[str, str] | None = None) -> HttpResponse:
    request_body = None if payload is None else json.dumps(payload).encode("utf-8")
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    req = request.Request(url, data=request_body, headers=request_headers, method=method)
    try:
        with request.urlopen(req, timeout=10) as response:
            response_body = response.read()
            parsed = json.loads(response_body.decode("utf-8")) if response_body else None
            return HttpResponse(status=response.status, body=parsed)
    except error.HTTPError as exc:
        try:
            body = exc.read()
            parsed = json.loads(body.decode("utf-8")) if body else None
        except Exception:
            parsed = None
        return HttpResponse(status=exc.code, body=parsed)


def _wait_until_ready(url: str, *, headers: dict[str, str] | None = None) -> None:
    deadline = time.time() + SYSTEM_TEST_TIMEOUT_SECONDS

    while time.time() < deadline:
        try:
            resp = _http_json("GET", url, headers=headers)
            if 200 <= resp.status < 300:
                return
        except Exception:
            logger.debug("Waiting for %s to become ready failed", url, exc_info=True)
        time.sleep(10)

    raise AssertionError(f"Timed out waiting for {url} to become ready")


def _wait_for_search_result(title_query: str, post_id: str, *, expected_present: bool) -> None:
    deadline = time.time() + SYSTEM_TEST_TIMEOUT_SECONDS

    url = f"{API_GATEWAY_URL}/api/v1/search/posts?q={quote_plus(title_query)}"
    while time.time() < deadline:
        try:
            resp = _http_json("GET", url)
            body = resp.body if isinstance(resp.body, list) else []
            matches = [item for item in body if item.get("u_id") == post_id]
            if expected_present and matches:
                return
            if not expected_present and not matches:
                return
        except Exception:
            logger.debug(
                "Waiting for search result on %s failed (expected_present=%s, post_id=%s)",
                url,
                expected_present,
                post_id,
                exc_info=True,
            )
        time.sleep(5)

    raise AssertionError(
        f"Timed out waiting for search result presence={expected_present} for post {post_id}"
    )


def _wait_for_dependencies() -> None:
    _wait_until_ready(f"{API_GATEWAY_URL}/api/v1/posts")
    _wait_until_ready(f"{API_GATEWAY_URL}/api/v1/search/posts?q=title")
    _wait_until_ready(ELASTICSEARCH_URL)
    _wait_until_ready(RABBITMQ_MGMT_URL, headers={"Authorization": f"Basic {_basic_auth('guest', 'guest')}"})
    print("All dependencies are ready waiting 30 seconds before starting tests...")
    time.sleep(30)


def _basic_auth(username: str, password: str) -> str:
    token = f"{username}:{password}".encode("utf-8")
    return base64.b64encode(token).decode("ascii")


def _create_post(title: str) -> dict[str, Any]:
    payload = {
        "community_id": str(uuid4()),
        "author_id": str(uuid4()),
        "title": title,
        "content": "system test content",
    }
    response = _http_json("POST", f"{API_GATEWAY_URL}/api/v1/posts", payload)
    assert response.status == 200
    assert isinstance(response.body, dict)
    return response.body


def _update_post(post_id: str, title: str) -> dict[str, Any]:
    response = _http_json(
        "PUT",
        f"{API_GATEWAY_URL}/api/v1/posts/{post_id}",
        {"title": title, "content": "system test content updated"},
    )
    assert response.status == 200
    assert isinstance(response.body, dict)
    return response.body


def _delete_post(post_id: str) -> dict[str, Any]:
    response = _http_json("DELETE", f"{API_GATEWAY_URL}/api/v1/posts/{post_id}")
    assert response.status == 200
    assert isinstance(response.body, dict)
    return response.body


@pytest.fixture(scope="session", autouse=True)
def wait_for_dependencies_fixture() -> None:
    _wait_for_dependencies()


def test_post_create_is_replicated_to_search_service():
    unique_id = uuid4().hex
    title = f"system-test-created-{unique_id}"

    created_post = _create_post(title)
    post_id = created_post["u_id"]

    try:
        _wait_for_search_result(title, post_id, expected_present=True)
    finally:
        try:
            _delete_post(post_id)
        except Exception:
            pass


def test_post_update_is_replicated_to_search_service():
    unique_id = uuid4().hex
    initial_title = f"system-test-update-initial-{unique_id}"
    updated_title = f"system-test-update-updated-{unique_id}"

    created_post = _create_post(initial_title)
    post_id = created_post["u_id"]

    try:
        _wait_for_search_result(initial_title, post_id, expected_present=True)

        _update_post(post_id, updated_title)
        _wait_for_search_result(updated_title, post_id, expected_present=True)
        _wait_for_search_result(initial_title, post_id, expected_present=False)
    finally:
        try:
            _delete_post(post_id)
        except Exception:
            pass


def test_post_delete_is_replicated_to_search_service():
    unique_id = uuid4().hex
    title = f"system-test-delete-{unique_id}"

    created_post = _create_post(title)
    post_id = created_post["u_id"]

    _wait_for_search_result(title, post_id, expected_present=True)

    _delete_post(post_id)
    _wait_for_search_result(title, post_id, expected_present=False)