"""add_user_fields

Revision ID: 2cec323900af
Revises: c4d8d6f0efb3
Create Date: 2025-05-28 08:36:16.222818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cec323900af'
down_revision: Union[str, None] = 'c4d8d6f0efb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # Add columns with default values first
    op.add_column('users', sa.Column('first_name', sa.String(length=50), nullable=True, server_default='Unknown'))
    op.add_column('users', sa.Column('last_name', sa.String(length=50), nullable=True, server_default='User'))
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))
    
    # Make columns NOT NULL after adding default values
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               server_default=None)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               server_default=None)
    
    # Make username nullable
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
