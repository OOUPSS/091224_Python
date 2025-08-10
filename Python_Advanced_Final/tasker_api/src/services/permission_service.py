from sqlalchemy.orm import Session
from src.db.models import Permission, Role

class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def initialize_permissions_and_roles(self):
        """
        Инициализирует базовые роли и права, если их нет в базе данных.
        """
        # Создание прав
        permissions = {
            "user:read:any": "Просмотр любого пользователя",
            "user:read:own": "Просмотр собственного профиля",
            "user:create": "Создание пользователя",
            "user:update:any": "Изменение любого пользователя",
            "user:update:own": "Изменение собственного профиля",
            "user:delete:any": "Удаление любого пользователя",
            "task:read:any": "Просмотр любой задачи",
            "task:read:own": "Просмотр собственной задачи",
            "task:create": "Создание задачи",
            "task:update:any": "Изменение любой задачи",
            "task:update:own": "Изменение собственной задачи",
            "task:delete:any": "Удаление любой задачи",
            "task:delete:own": "Удаление собственной задачи",
        }
        
        db_permissions = self.db.query(Permission).all()
        existing_permission_names = {p.name for p in db_permissions}
        
        for name, desc in permissions.items():
            if name not in existing_permission_names:
                new_permission = Permission(name=name)
                self.db.add(new_permission)
                print(f"Добавлено новое право: {name}")

        self.db.commit()

        # Создание ролей
        roles = {
            "admin": ["user:read:any", "user:update:any", "user:delete:any", 
                      "task:read:any", "task:update:any", "task:delete:any"],
            "user": ["user:read:own", "user:update:own", 
                     "task:read:own", "task:create", "task:update:own", "task:delete:own"],
        }
        
        db_roles = self.db.query(Role).all()
        existing_role_names = {r.name for r in db_roles}

        all_permissions = {p.name: p for p in self.db.query(Permission).all()}

        for name, required_permissions in roles.items():
            if name not in existing_role_names:
                new_role = Role(name=name)
                for perm_name in required_permissions:
                    if perm_name in all_permissions:
                        new_role.permissions.append(all_permissions[perm_name])
                self.db.add(new_role)
                print(f"Добавлена новая роль: {name}")

        self.db.commit()