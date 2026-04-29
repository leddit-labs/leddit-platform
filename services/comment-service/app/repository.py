from datetime import datetime, UTC
from uuid import uuid4

from neo4j import Driver

from .models import Comment


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

    def create(self, post_id: str, parent_id: int | None, author_id: str, content: str) -> Comment:
        now = datetime.now(UTC).isoformat()
        u_id = str(uuid4())

        query = """
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
        OPTIONAL MATCH (p:Comment {id: $parent_id})
        FOREACH (_ IN CASE WHEN p IS NULL THEN [] ELSE [1] END | MERGE (p)-[:HAS_REPLY]->(c))
        RETURN c
        """

        with self.db.session() as session:
            record = session.run(
                query,
                u_id=u_id,
                post_id=post_id,
                parent_id=parent_id,
                author_id=author_id,
                content=content,
                created_at=now,
            ).single()
            return self._to_comment(dict(record["c"]))

    def get_by_id(self, comment_id: int) -> Comment | None:
        query = "MATCH (c:Comment {id: $id}) RETURN c"
        with self.db.session() as session:
            record = session.run(query, id=comment_id).single()
            if record is None:
                return None
            return self._to_comment(dict(record["c"]))

    def list_by_post_id(self, post_id: str) -> list[Comment]:
        query = """
        MATCH (c:Comment {post_id: $post_id})
        RETURN c
        ORDER BY c.created_at ASC
        """
        with self.db.session() as session:
            result = session.run(query, post_id=post_id)
            return [self._to_comment(dict(row["c"])) for row in result]

    def update_content(self, comment: Comment, content: str) -> Comment:
        now = datetime.now(UTC).isoformat()
        query = """
        MATCH (c:Comment {id: $id})
        SET c.content = $content,
            c.updated_at = $updated_at
        RETURN c
        """
        with self.db.session() as session:
            record = session.run(query, id=comment.id, content=content, updated_at=now).single()
            return self._to_comment(dict(record["c"]))

    def soft_delete(self, comment: Comment) -> Comment:
        now = datetime.now(UTC).isoformat()
        query = """
        MATCH (c:Comment {id: $id})
        SET c.content = '[deleted]',
            c.deleted_at = $deleted_at,
            c.updated_at = $updated_at
        RETURN c
        """
        with self.db.session() as session:
            record = session.run(query, id=comment.id, deleted_at=now, updated_at=now).single()
            return self._to_comment(dict(record["c"]))
