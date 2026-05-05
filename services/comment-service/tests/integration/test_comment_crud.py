def create_comment(
    client,
    *,
    post_id="post-1",
    parent_id=None,
    author_id="author-1",
    content="test comment",
):
    r = client.post(
        "/api/v1/comments",
        json={
            "post_id": post_id,
            "parent_id": parent_id,
            "author_id": author_id,
            "content": content,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()


def test_create_comment_returns_201(client):
    data = create_comment(
        client,
        post_id="post-1",
        author_id="author-1",
        content="first comment",
    )

    assert data["post_id"] == "post-1"
    assert data["parent_id"] is None
    assert data["author_id"] == "author-1"
    assert data["content"] == "first comment"
    assert data["id"] > 0
    assert data["created_at"] is not None


def test_get_comment_returns_200(client):
    created = create_comment(client, content="hello world")
    comment_id = created["id"]

    r = client.get(f"/api/v1/comments/{comment_id}")
    assert r.status_code == 200, r.text
    fetched = r.json()

    assert fetched["id"] == comment_id
    assert fetched["content"] == "hello world"
    assert fetched["deleted_at"] is None


def test_list_comments_for_post_returns_ordered(client):
    create_comment(client, post_id="post-1", author_id="auth-1", content="first")
    create_comment(client, post_id="post-1", author_id="auth-2", content="second")
    create_comment(client, post_id="post-1", author_id="auth-3", content="third")

    r = client.get("/api/v1/posts/post-1/comments")
    assert r.status_code == 200, r.text
    comments = r.json()

    assert len(comments) == 3
    assert [c["content"] for c in comments] == ["first", "second", "third"]


def test_update_comment_patch_changes_content(client):
    created = create_comment(client, content="original")
    comment_id = created["id"]

    r = client.patch(
        f"/api/v1/comments/{comment_id}",
        json={"content": "updated"},
    )
    assert r.status_code == 200, r.text
    updated = r.json()

    assert updated["id"] == comment_id
    assert updated["content"] == "updated"
    assert updated["updated_at"] is not None


def test_delete_comment_soft_deletes(client):
    created = create_comment(client, content="will delete")
    comment_id = created["id"]

    r = client.delete(f"/api/v1/comments/{comment_id}")
    assert r.status_code == 200, r.text
    deleted = r.json()

    assert deleted["id"] == comment_id
    assert deleted["content"] == "[deleted]"
    assert deleted["deleted_at"] is not None

    r = client.get(f"/api/v1/comments/{comment_id}")
    assert r.status_code == 200
    assert r.json()["deleted_at"] is not None


def test_get_nonexistent_comment_returns_404(client):
    r = client.get("/api/v1/comments/999999")
    assert r.status_code == 404


def test_update_nonexistent_comment_returns_404(client):
    r = client.patch(
        "/api/v1/comments/999999",
        json={"content": "nope"},
    )
    assert r.status_code == 404


def test_delete_nonexistent_comment_returns_404(client):
    r = client.delete("/api/v1/comments/999999")
    assert r.status_code == 404


def test_create_comment_with_missing_parent_returns_400(client):
    r = client.post(
        "/api/v1/comments",
        json={
            "post_id": "post-1",
            "parent_id": "missing-parent-id",
            "author_id": "author-1",
            "content": "reply",
        },
    )
    assert r.status_code == 400, r.text
    assert "Parent comment does not exist" in r.json()["detail"]


def test_update_already_deleted_comment_returns_409(client):
    created = create_comment(client, content="will delete")
    comment_id = created["id"]

    r = client.delete(f"/api/v1/comments/{comment_id}")
    assert r.status_code == 200

    r = client.patch(
        f"/api/v1/comments/{comment_id}",
        json={"content": "nope"},
    )
    assert r.status_code == 409, r.text