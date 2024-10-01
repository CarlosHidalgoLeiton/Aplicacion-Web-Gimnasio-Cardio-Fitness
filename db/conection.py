import pymysql

class Conection:
    _conexion = None  # Variable de clase para almacenar la conexión

    @classmethod
    def conectar(cls):
        if cls._conexion is None:  # Solo conecta si no hay una conexión existente
            try:
                cls._conexion = pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='gimnasio'
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
