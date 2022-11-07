"""create post table

Revision ID: ffc8abe93849
Revises: 
Create Date: 2022-10-29 17:22:52.065305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffc8abe93849'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title',sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
