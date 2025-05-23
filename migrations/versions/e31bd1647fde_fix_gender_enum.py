"""Fix gender enum

Revision ID: e31bd1647fde
Revises: 18f369952ea4
Create Date: 2025-05-21 02:48:57.291417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e31bd1647fde'
down_revision: Union[str, None] = '18f369952ea4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('telecom', sa.Enum('SKT', 'KT', 'LGU', name='telecom_enum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'telecom')
    # ### end Alembic commands ###
