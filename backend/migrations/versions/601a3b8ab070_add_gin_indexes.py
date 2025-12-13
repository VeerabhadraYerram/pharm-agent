"""add gin indexes

Revision ID: 601a3b8ab070
Revises: 340ac0d03db5
Create Date: 2025-12-13 15:00:05.955067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '601a3b8ab070'
down_revision: Union[str, Sequence[str], None] = '340ac0d03db5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "idx_worker_responses_outputs_gin",
        "worker_responses",
        ["outputs"],
        postgresql_using="gin"
    )
    op.create_index(
        "idx_worker_responses_sources_gin",
        "worker_responses",
        ["sources"],
        postgresql_using="gin"
    )

    op.create_index(
        "idx_jobs_status",
        "jobs",
        ["status"]
    )

    op.create_index(
        "idx_jobs_user_created",
        "jobs",
        ["user_id", "created_at"]
    )

    op.create_index(
        "idx_tasks_status",
        "tasks",
        ["status"]
    )

    op.create_index(
        "idx_artifacts_job_type",
        "artifacts",
        ["job_id", "type"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_artifacts_job_type", table_name="artifacts")
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_index("idx_jobs_user_created", table_name="jobs")
    op.drop_index("idx_jobs_status", table_name="jobs")
    op.drop_index("idx_worker_responses_sources_gin", table_name="worker_responses")
    op.drop_index("idx_worker_responses_outputs_gin", table_name="worker_responses")

