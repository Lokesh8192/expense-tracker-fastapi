"""drop phone_verified and otp columns

Revision ID: drop_phone_verified_and_otp_columns
Revises: c7e68252e36f
Create Date: 2026-03-17 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "drop_phone_otp_cols"
down_revision = "c7e68252e36f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop fields no longer used by the application
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS phone_verified")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS mobile_otp")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS mobile_otp_expires")


def downgrade() -> None:
    # Add columns back in case of downgrade
    op.add_column(
        "users",
        sa.Column("phone_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "users",
        sa.Column("mobile_otp", sa.String(), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("mobile_otp_expires", sa.DateTime(), nullable=True),
    )
