from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {}

class User(AbstractUserRole):
    available_permissions = {}