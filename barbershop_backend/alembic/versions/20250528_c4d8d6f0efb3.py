"""add user profile fields

Revision ID: c4d8d6f0efb3
Revises: 0ab45922c650
Create Date: 2025-05-28 04:17:53.077048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4d8d6f0efb3'
down_revision: Union[str, None] = '0ab45922c650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
