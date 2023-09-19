"""create address_id to user

Revision ID: fa439e4748d8
Revises: 690a7fb5f1cf
Create Date: 2023-09-18 13:39:26.926152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa439e4748d8'
down_revision: Union[str, None] = '690a7fb5f1cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_id', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE'
                         )


def downgrade() -> None:
    op.drop_constraint('address_users_id', table_name='users')
    op.drop_column('users', 'address_id')
