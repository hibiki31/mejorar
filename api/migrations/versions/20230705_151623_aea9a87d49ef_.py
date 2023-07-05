"""empty message

Revision ID: aea9a87d49ef
Revises: 
Create Date: 2023-07-05 15:16:23.545591

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = 'aea9a87d49ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contents',
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=256), nullable=False),
    sa.Column('hashed_password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('contents_dependencies',
    sa.Column('content_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('dependencies_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.ForeignKeyConstraint(['content_uuid'], ['contents.uuid'], ),
    sa.ForeignKeyConstraint(['dependencies_uuid'], ['contents.uuid'], ),
    sa.PrimaryKeyConstraint('content_uuid', 'dependencies_uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contents_dependencies')
    op.drop_table('users')
    op.drop_table('contents')
    # ### end Alembic commands ###