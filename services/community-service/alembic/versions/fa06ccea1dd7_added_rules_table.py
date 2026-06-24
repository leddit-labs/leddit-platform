"""Added Rules table

Revision ID: fa06ccea1dd7
Revises:
Create Date: 2026-05-20 19:48:40.044771

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fa06ccea1dd7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "community_rules",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("community_id", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("text", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["community_id"], ["communities.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("community_id", "order", name="uq_community_rule_order"),
    )
    op.create_index(
        op.f("ix_community_rules_community_id"),
        "community_rules",
        ["community_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_community_rules_community_id"),
        table_name="community_rules",
    )
    op.drop_table("community_rules")

    op.drop_table("community_moderators")

    op.drop_index(
        op.f("ix_communities_created_by"),
        table_name="communities",
    )
    op.drop_index(
        op.f("ix_communities_name"),
        table_name="communities",
    )
    op.drop_table("communities")

    op.execute("DROP TYPE IF EXISTS moderatorrole")
