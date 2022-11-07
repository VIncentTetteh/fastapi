"""add column content

Revision ID: 4f3da52b9e76
Revises: ffc8abe93849
Create Date: 2022-11-01 21:34:43.785800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3da52b9e76'
down_revision = 'ffc8abe93849'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
