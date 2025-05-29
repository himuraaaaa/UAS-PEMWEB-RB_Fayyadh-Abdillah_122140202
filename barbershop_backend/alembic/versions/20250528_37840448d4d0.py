"""merge heads

Revision ID: 37840448d4d0
Revises: update_schema, a1d8cfe50ba1
Create Date: 2025-05-28 11:34:04.841628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37840448d4d0'
down_revision: Union[str, None] = ('update_schema', 'a1d8cfe50ba1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
