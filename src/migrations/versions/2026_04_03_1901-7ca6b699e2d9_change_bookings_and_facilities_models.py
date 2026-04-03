"""change bookings and facilities models

Revision ID: 7ca6b699e2d9
Revises: ebabfd67e2fa
Create Date: 2026-04-03 19:01:59.720114

"""

from typing import Sequence, Union

from alembic import op

revision: str = "7ca6b699e2d9"
down_revision: Union[str, Sequence[str], None] = "ebabfd67e2fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f("bookings_user_id_fkey"), "bookings", type_="foreignkey")
    op.create_foreign_key(
        None,
        "bookings",
        "users",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.drop_constraint(
        op.f("rooms_facilities_room_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_room_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        op.f("bookings_user_id_fkey"), "bookings", "users", ["user_id"], ["id"]
    )

