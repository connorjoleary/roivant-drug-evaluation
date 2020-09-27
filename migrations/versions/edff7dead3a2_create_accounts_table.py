"""create accounts table

Revision ID: edff7dead3a2
Revises: 
Create Date: 2020-09-27 11:32:19.564727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edff7dead3a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    account = op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('account')
