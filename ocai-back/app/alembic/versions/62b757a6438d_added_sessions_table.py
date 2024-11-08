"""Added Sessions Table

Revision ID: 62b757a6438d
Revises: 8c1e1576c747
Create Date: 2024-10-01 21:08:52.715155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62b757a6438d'
down_revision: Union[str, None] = '8c1e1576c747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('chatHistory', sa.BLOB(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('result', sa.BLOB(), nullable=True),
    sa.Column('lastActive', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('verification_token', 'identifier',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('verification_token', 'identifier',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('session')
    # ### end Alembic commands ###
