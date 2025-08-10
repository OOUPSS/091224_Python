"""insert initial data

Revision ID: 2g3h4i5j6k7l
Revises: 1a2b3c4d5e6f
Create Date: 2025-08-10 13:46:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2g3h4i5j6k7l'
down_revision: Union[str, None] = '1a2b3c4d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO roles (name)
        VALUES ('admin'), ('moderator'), ('user')
        ON CONFLICT (name) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO permissions (name) VALUES
        ('task:create'),
        ('task:read:own'),
        ('task:update:own'),
        ('task:delete:own'),
        ('task:read:any'),
        ('task:update:any'),
        ('task:delete:any')
        ON CONFLICT (name) DO NOTHING;
        """
    )
    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles, permissions
        WHERE (roles.name = 'admin' AND permissions.name IN (
        'task:create', 
        'task:read:any', 
        'task:update:any', 
        'task:delete:any'
        ))
        OR (roles.name = 'moderator' AND permissions.name IN (
        'task:read:any', 
        'task:delete:any'
        ))
        OR (roles.name = 'user' AND permissions.name IN (
        'task:create',
        'task:read:own', 
        'task:update:own', 
        'task:delete:own'
        ));
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM roles_permissions
        WHERE role_id IN (
            SELECT id FROM roles WHERE name IN ('admin', 'moderator', 'user')
        )
        AND permission_id IN (
            SELECT id FROM permissions WHERE name IN (
                'task:create',
                'task:read:any',
                'task:update:any',
                'task:delete:any',
                'task:read:own',
                'task:update:own',
                'task:delete:own'
            )
        );
        """
    )
    op.execute(
        """
        DELETE FROM roles WHERE name IN ('admin', 'moderator', 'user');
        """
    )
    op.execute(
        """
        DELETE FROM permissions
        WHERE name IN (
        'task:create',
        'task:read:own',
        'task:update:own',
        'task:delete:own',
        'task:read:any',
        'task:update:any',
        'task:delete:any'
        );
        """
    )