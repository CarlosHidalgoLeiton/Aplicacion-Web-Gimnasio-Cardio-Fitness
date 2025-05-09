import pymysql

class Conection:
    _conexion = None  # Variable de clase para almacenar la conexión

    @classmethod
    def conectar(cls):
        if cls._conexion is None:  # Solo conecta si no hay una conexión existente
            try:
                # cls._conexion = pymysql.connect(
                #     host='168.231.68.243',
                #     user='admin',
                #     passwd='CardioFit2025#',
                #     db='gimnasio',
                #     port=3306
                # )
                cls._conexion = pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',  # En XAMPP, por defecto, el usuario 'root' no tiene contraseña
                    db='gimnasio',
                    port=3306
                )
                print("Conexión exitosa a la base de datos")
            except pymysql.MySQLError as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._conexion = None
        return cls._conexion

    @classmethod
    def desconectar(cls):
        if cls._conexion:
            cls._conexion.close()
            cls._conexion = None  # Resetear la conexión
            print("Desconexión exitosa de la base de datos")
