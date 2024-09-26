# db/conection.py
import pymysql

class Conection:
    def __init__(self):
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                passwd='',
                db='gimnasio'
            )
            print("Conexión exitosa a la base de datos")
            return self.conexion
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Desconexión exitosa de la base de datos")
        else:
            print("No hay conexión para cerrar")