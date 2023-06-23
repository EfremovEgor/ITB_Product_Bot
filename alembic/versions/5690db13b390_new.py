"""new

Revision ID: 5690db13b390
Revises: 
Create Date: 2023-06-08 12:52:15.708912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5690db13b390"
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
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("api_key", sa.String, nullable=False),
        sa.Column("marketplace", sa.String, nullable=False),
    )
    op.create_table(
        "goods",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("marketplace", sa.String, nullable=False),
        sa.Column("notification_id", sa.Integer, nullable=False),
        sa.Column("market_place_id", sa.Integer, nullable=False),
        sa.Column("importance", sa.String, nullable=False),
        sa.Column("last_sent_notification", sa.DateTime),
        sa.Column("available", sa.Boolean),
    )


def downgrade() -> None:
    op.drop_table("unregistered_users")
    op.drop_table("registered_users")
    op.drop_table("accounts")
    op.drop_table("goods")
