"""add user table

Revision ID: 2ac4c93dc728
Revises: 4f3da52b9e76
Create Date: 2022-11-01 21:41:47.002596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ac4c93dc728'
down_revision = '4f3da52b9e76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
            sa.Column('id', sa.Integer(),nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
            )


def downgrade() -> None:
    op.drop_table('users')
