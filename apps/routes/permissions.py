from flask_principal import Permission, RoleNeed

#Definicion de los roles
admin_permission = Permission(RoleNeed('Admin'))
client_permission = Permission(RoleNeed('Client'))
trainer_permission = Permission(RoleNeed('Trainer'))