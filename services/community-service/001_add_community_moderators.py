"""add community_moderators table

Revision ID: 001
Revises:
Create Date: 2025-05-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the enum type first (PostgreSQL-specific)
    moderator_role = sa.Enum("owner", "moderator", name="moderatorrole")
    moderator_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "community_moderators",
        sa.Column("community_id", sa.String(), sa.ForeignKey("communities.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.String(), primary_key=True),
        sa.Column("role", moderator_role, nullable=False),
        sa.UniqueConstraint("community_id", "user_id", name="uq_community_user"),
    )

    # Seed: make every existing community creator an owner
    op.execute(
        """
        INSERT INTO community_moderators (community_id, user_id, role)
        SELECT id, created_by, 'owner'
        FROM communities
        ON CONFLICT DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_table("community_moderators")
    sa.Enum(name="moderatorrole").drop(op.get_bind(), checkfirst=True)
