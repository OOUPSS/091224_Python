"""create initial schema

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2025-08-10 13:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('email')
    )
    op.create_table('refresh_tokens',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('ip_address', sa.String(length=50), nullable=True),
    sa.Column('user_agent', sa.String(length=200), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=False),
    sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('token')
    )
    op.create_index('ix_refresh_tokens_token_user', 'refresh_tokens', ['token', 'user_uuid'], unique=False)
    op.create_table('roles_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table('tasks',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('owner_uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['owner_uuid'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )


def downgrade() -> None:
    op.drop_table('users_roles')
    op.drop_table('tasks')
    op.drop_table('roles_permissions')
    op.drop_index('ix_refresh_tokens_token_user', table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('permissions')