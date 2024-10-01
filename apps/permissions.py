from flask_principal import Permission, RoleNeed

#Definicion de los roles
admin_permission = Permission(RoleNeed('Admin'))
client_permission = Permission(RoleNeed('Cliente'))
trainer_permission = Permission(RoleNeed('Entrenador'))