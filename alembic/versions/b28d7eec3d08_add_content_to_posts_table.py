"""add content to posts table

Revision ID: b28d7eec3d08
Revises: 8a75ec4afef3
Create Date: 2022-01-06 16:58:55.833520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b28d7eec3d08'
down_revision = '8a75ec4afef3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
