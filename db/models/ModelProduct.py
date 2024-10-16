from .entities.Product import Product
from datetime import datetime
import re
from pymysql import IntegrityError
import base64

class ModelProduct:

    @classmethod
    def insertProduct(cls, conection, product):
        if product != None:
            try:
                product.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Producto (Nombre, Detalle, Precio, Cantidad, Imagen, Estado)
                VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (product.Name, product.Detail, product.Price, product.Stock, product.Image, product.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Producto {product.Name} creado exitosamente.")
                    return True
                else:
                    print("No se pudo crear el product.")
                    return "Error"
            except BaseException as ex:
                print(f"Error en ModelProduct insertProduct: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelProduct insertProduct: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def updateProduct(cls, conection, product, IdProducto):
        if product != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Product SET Nombre = %s, Detalle = %s, Precio = %s, Cantidad = %s, Imagen = %s, Estado = %s WHERE ID_Producto = %s"""
                cursor.execute(sql, (product.Nmae, product.Detail, product.Price, product.Stock, product.Image, product.State, IdProducto))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Producto {product.Nmae} actualizado exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar el producto.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelProduct updateProduct: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelProduct updateProduct: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

    @classmethod
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Producto, Nombre, Detalle, Precio, Cantidad, Imagen, Estado FROM Producto"
            cursor.execute(sql)
            rows = cursor.fetchall()
            products = []
            
            for row in rows:
            
                image_blob = row[5]  
                if image_blob:
                    image_base64 = base64.b64encode(image_blob).decode('utf-8')
                else:
                    image_base64 = None
                
                product = Product(
                    ID_Product=row[0],
                    Name=row[1],
                    Detail=row[2],
                    Price=row[3],
                    Stock=row[4],
                    Image=image_base64, 
                    State=row[6],
                )
                products.append(product)
            
            return products
        
        except Exception as ex:
            print(f"Error in get_all: {ex}")
            return None
        
    @classmethod
    def get_product_by_id(cls, conexion, IdProducto):
        try:
            cursor = conexion.cursor()
            sql = """SELECT ID_Producto, Nombre, Detalle, Precio, Cantidad, Imagen, Estado
                    FROM Producto WHERE ID_Producto = %s"""
            cursor.execute(sql, (IdProducto))
            row = cursor.fetchone()

            if row:
                # Crear y devolver un objeto product
                image_blob = row[5]  
                if image_blob:
                    image_base64 = base64.b64encode(image_blob).decode('utf-8')
                else:
                    image_base64 = None

                return Product(
                    ID_Product=row[0],
                    Name=row[1],
                    Detail=row[2],
                    Price=row[3],
                    Stock=row[4],
                    Image= image_base64,
                    State=row[6],
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener product por cédula: {ex}")
            return None
    

    # @classmethod
    # def disableProduct(cls, conection, productId):
    #     if productId != None:
    #         try:
    #             cursor = conection.cursor()
    #             sql = """UPDATE Producte SET Estado = 0  WHERE Cedula = %s"""
    #             cursor.execute(sql, (productId))
    #             if cursor.rowcount > 0:
    #                 conection.commit()
    #                 return True
    #             else:
    #                 print("No se pudo actualizar el product.")
    #                 conection.rollback()
    #                 return False

    #         except Exception as ex:
    #             print(f"Ocurrió un error en actualizar un product {ex}")
    #             conection.rollback()
    #             return False
    #     else:
    #         return False
        
    # @classmethod
    # def ableProduct(cls, conection, productId):
    #     if productId != None:
    #         try:
    #             cursor = conection.cursor()
    #             sql = """UPDATE Producte SET Estado = 1  WHERE Cedula = %s"""
    #             cursor.execute(sql, (productId))
    #             if cursor.rowcount > 0:
    #                 conection.commit()
    #                 return True
    #             else:
    #                 print("No se pudo actualizar el product.")
    #                 conection.rollback()
    #                 return False

    #         except Exception as ex:
    #             print(f"Ocurrió un error en actualizar un product {ex}")
    #             conection.rollback()
    #             return False
    #     else:
    #         return False
    
    @classmethod
    def getDataProduct(cls, request):
        name = request.form['Name']
        detail = request.form['Detail']
        price = request.form['Price']
        stock = request.form['Stock']
        image_file = request.files['Image']
        image_blob = None
        
        if image_file:
            image_blob = image_file.read()

        return Product(None, name, detail, price, stock, image_blob)

    @classmethod
    def validateDataForm(cls, product):
        # Validar que el nombre no esté vacío
        if not product.Name or len(product.Name.strip()) == 0:
            print("El nombre del producto es requerido.")
            return False
        
        # Validar que la imagen no sea None o esté vacía
        if not product.Image:
            print("La imagen del producto es requerida.")
            return False

        # Si todas las validaciones pasan
        return True
            
        
        
