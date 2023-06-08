"""init

Revision ID: 1bb93129311d
Revises: 
Create Date: 2023-06-07 20:56:24.221370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1bb93129311d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "unregistered_users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("telegram_id", sa.Integer, primary_key=False, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("last_sent_message", sa.DateTime),
    )
    op.create_table(
        "registered_users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("telegram_id", sa.Integer, primary_key=False, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("last_sent_message", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("unregistered_users")
    op.drop_table("registered_users")
