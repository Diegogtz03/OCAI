"""fix userid column name

Revision ID: 4de72c85ef49
Revises: d4fb92eade32
Create Date: 2024-10-31 15:54:26.711444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4de72c85ef49'
down_revision: Union[str, None] = 'd4fb92eade32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('verification_token', 'identifier',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('verification_token', 'identifier',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
