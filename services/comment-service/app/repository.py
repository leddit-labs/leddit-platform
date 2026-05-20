from datetime import datetime, UTC
from uuid import uuid4

from neo4j import Driver

from .models import Comment, CommentVersion


class CommentRepository:
    def __init__(self, db: Driver):
        self.db = db

    @staticmethod
    def _to_comment(properties: dict) -> Comment:
        def parse_dt(value: str | None) -> datetime | None:
            if value is None:
                return None
            return datetime.fromisoformat(value)

        return Comment(
            id=properties["id"],
            u_id=properties["u_id"],
            post_id=properties["post_id"],
            parent_id=properties.get("parent_id"),
            author_id=properties["author_id"],
            content=properties["content"],
            created_at=parse_dt(properties["created_at"]),
            updated_at=parse_dt(properties.get("updated_at")),
            deleted_at=parse_dt(properties.get("deleted_at")),
        )
    
    def _to_comment_version(self, properties: dict) -> CommentVersion:
        def parse_dt(value: str | None) -> datetime | None:
            if value is None:
                return None
            return datetime.fromisoformat(value)

        return CommentVersion(
            version_id=properties["version_id"],
            content=properties.get("content"),
            created_at=parse_dt(properties.get("created_at")),
        )
    
    def _merge_comment_and_version(self, c: dict, r: dict | None) -> Comment:
        # Helper: use the content from the newest CommentVersion when returning a Comment
        if r is None:
            return self._to_comment(dict(c))

        v = self._to_comment_version(dict(r))
        c_props = dict(c)
        c_props["content"] = v.content
        c_props["updated_at"] = v.created_at.isoformat() if v.created_at is not None else None
        return self._to_comment(c_props)

    def create(self, post_id: str, parent_id: str | None, author_id: str, content: str) -> Comment:
        now = datetime.now(UTC).isoformat()
        u_id = str(uuid4())
        with self.db.session() as session:
            record = session.run(
                _CREATE_COMMENT,
                u_id=u_id,
                post_id=post_id,
                parent_id=parent_id,
                author_id=author_id,
                content=content,
                created_at=now,
            ).single()
            return self._to_comment(dict(record["c"]))

    def get_by_id(self, comment_id: int) -> Comment | None:
        with self.db.session() as session:
            record = session.run(_GET_COMMENT_WITH_LATEST_VERSION, id=comment_id).single()
            if record is None:
                return None
            return self._merge_comment_and_version(dict(record["c"]), record.get("r"))

    def get_by_u_id(self, comment_u_id: str) -> Comment | None:
        with self.db.session() as session:
            record = session.run(_GET_COMMENT_BY_U_ID_WITH_LATEST_VERSION, u_id=comment_u_id).single()
            if record is None:
                return None
            return self._merge_comment_and_version(dict(record["c"]), record.get("r"))

    def list_by_post_id(self, post_id: str) -> list[Comment]:
        with self.db.session() as session:
            result = session.run(_LIST_COMMENTS_WITH_LATEST_VERSION, post_id=post_id)
            return [
                self._merge_comment_and_version(dict(row["c"]), row.get("r")) for row in result
            ]

    def update_content(self, comment: Comment, content: str) -> Comment:
        now = datetime.now(UTC).isoformat()
        version_id = str(uuid4())
        with self.db.session() as session:
            record = session.run(
                _CREATE_VERSION,
                id=comment.id,
                content=content,
                created_at=now,
                version_id=version_id,
            ).single()
            return self._merge_comment_and_version(dict(record["c"]), dict(record["r"]))

    def soft_delete(self, comment: Comment) -> Comment:
        now = datetime.now(UTC).isoformat()
        query = """
        MATCH (c:Comment {id: $id})
        SET c.deleted_at = $deleted_at,
            c.updated_at = $updated_at
        RETURN c
        """
        with self.db.session() as session:
            record = session.run(query, id=comment.id, deleted_at=now, updated_at=now).single()
            return self._to_comment(dict(record["c"]))


# Cypher queries
_GET_COMMENT_WITH_LATEST_VERSION = """
MATCH (c:Comment {id: $id})
OPTIONAL MATCH (c)-[:HAS_VERSION]->(r:CommentVersion)
WITH c, r
ORDER BY r.created_at DESC
RETURN c, r LIMIT 1
"""

_GET_COMMENT_BY_U_ID_WITH_LATEST_VERSION = """
MATCH (c:Comment {u_id: $u_id})
OPTIONAL MATCH (c)-[:HAS_VERSION]->(r:CommentVersion)
WITH c, r
ORDER BY r.created_at DESC
RETURN c, r LIMIT 1
"""

_LIST_COMMENTS_WITH_LATEST_VERSION = """
MATCH (c:Comment {post_id: $post_id})
OPTIONAL MATCH (c)-[:HAS_VERSION]->(r:CommentVersion)
WITH c, r
ORDER BY c.created_at ASC, r.created_at DESC
RETURN c, r
"""

_CREATE_VERSION = """
MATCH (c:Comment {id: $id})
CREATE (r:CommentVersion {
    version_id: $version_id,
    content: $content,
    created_at: $created_at
})
CREATE (c)-[:HAS_VERSION]->(r)
SET c.updated_at = $created_at
RETURN c, r
"""


_CREATE_COMMENT = """
MERGE (ctr:Counter {name: 'comment_id'})
ON CREATE SET ctr.value = 0
SET ctr.value = ctr.value + 1
WITH ctr.value AS next_id
CREATE (c:Comment {
    id: next_id,
    u_id: $u_id,
    post_id: $post_id,
    parent_id: $parent_id,
    author_id: $author_id,
    content: $content,
    created_at: $created_at,
    updated_at: null,
    deleted_at: null
})
WITH c
OPTIONAL MATCH (p:Comment {u_id: $parent_id})
FOREACH (_ IN CASE WHEN p IS NULL THEN [] ELSE [1] END | MERGE (p)-[:HAS_REPLY]->(c))
RETURN c
"""