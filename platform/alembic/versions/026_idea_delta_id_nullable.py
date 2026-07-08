"""Relax legacy contribution_to_canonical_idea.idea_delta_id when present.

Migration 020 removes `idea_delta_id` after rewiring contributions to
`delta_card_id`. Older databases may still have the legacy column if 020 was
edited or applied differently; for the current linear migration chain this is
a no-op.

Revision ID: 026
Revises: 025
"""

revision = "026"
down_revision = "025"

from alembic import op


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    rows = bind.exec_driver_sql(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
        """,
        (table_name, column_name),
    ).fetchone()
    return rows is not None


def upgrade() -> None:
    if _has_column("contribution_to_canonical_idea", "idea_delta_id"):
        op.alter_column("contribution_to_canonical_idea", "idea_delta_id",
                        nullable=True)


def downgrade() -> None:
    if _has_column("contribution_to_canonical_idea", "idea_delta_id"):
        # Down only succeeds if you've backfilled idea_delta_id for every row.
        op.alter_column("contribution_to_canonical_idea", "idea_delta_id",
                        nullable=False)
