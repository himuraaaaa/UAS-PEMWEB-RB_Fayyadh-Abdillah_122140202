"""update schema

Revision ID: update_schema
Revises: d647f78f774f
Create Date: 2025-05-28 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_schema'
down_revision: Union[str, None] = 'd647f78f774f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old columns from barbers
    op.drop_column('barbers', 'email')
    op.drop_column('barbers', 'phone')
    op.drop_column('barbers', 'bio')
    op.drop_column('barbers', 'rating')
    op.drop_column('barbers', 'is_available')
    
    # Add new columns to barbers
    op.add_column('barbers', sa.Column('position', sa.String(100), nullable=False))
    op.add_column('barbers', sa.Column('image', sa.String(255), nullable=False))
    op.add_column('barbers', sa.Column('social', sa.JSON, nullable=True))
    
    # Drop barber_id from services
    op.drop_constraint('services_barber_id_fkey', 'services', type_='foreignkey')
    op.drop_column('services', 'barber_id')
    
    # Add image to services
    op.add_column('services', sa.Column('image', sa.String(255), nullable=False))
    
    # Update appointments
    op.alter_column('appointments', 'appointment_date',
                    new_column_name='date',
                    existing_type=sa.DateTime(),
                    type_=sa.Date(),
                    nullable=False)
    op.add_column('appointments', sa.Column('time', sa.Time(), nullable=False))
    op.add_column('appointments', sa.Column('notes', sa.String(255), nullable=True))
    op.alter_column('appointments', 'status',
                    existing_type=sa.String(20),
                    type_=sa.String(50),
                    nullable=False,
                    server_default='pending')


def downgrade() -> None:
    # Revert appointments changes
    op.drop_column('appointments', 'notes')
    op.drop_column('appointments', 'time')
    op.alter_column('appointments', 'date',
                    new_column_name='appointment_date',
                    existing_type=sa.Date(),
                    type_=sa.DateTime(),
                    nullable=False)
    op.alter_column('appointments', 'status',
                    existing_type=sa.String(50),
                    type_=sa.String(20),
                    nullable=True,
                    server_default=None)
    
    # Revert services changes
    op.drop_column('services', 'image')
    op.add_column('services', sa.Column('barber_id', sa.Integer(), nullable=True))
    op.create_foreign_key('services_barber_id_fkey', 'services', 'barbers', ['barber_id'], ['id'])
    
    # Revert barbers changes
    op.drop_column('barbers', 'social')
    op.drop_column('barbers', 'image')
    op.drop_column('barbers', 'position')
    op.add_column('barbers', sa.Column('is_available', sa.Boolean(), nullable=True))
    op.add_column('barbers', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('barbers', sa.Column('bio', sa.String(500), nullable=True))
    op.add_column('barbers', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('barbers', sa.Column('email', sa.String(120), nullable=False)) 