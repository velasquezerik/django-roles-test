from rolepermissions.roles import AbstractUserRole

class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'drop_tables': True,
    }

class SystemUser(AbstractUserRole):
	available_permissions = {
	    'drop_tables': True,
	}