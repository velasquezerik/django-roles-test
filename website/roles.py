from rolepermissions.roles import AbstractUserRole

class SystemAdmin(AbstractUserRole):
    available_permissions = {}

class SystemUser(AbstractUserRole):
    available_permissions = {}