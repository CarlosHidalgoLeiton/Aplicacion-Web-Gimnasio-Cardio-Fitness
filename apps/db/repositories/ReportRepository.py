# from datetime import date, datetime
# import pymysql.cursors
# from apps.db.repositories.RepositoryBase import RepositoryBase

# class reportRepository(RepositoryBase):

#     def __init__(self):
#         super().__init__(Product)

#     # ---------- INVENTARIO (ventas por producto) ----------
#     @classmethod
#     def get_ProductBills(cls):

        


#     @classmethod
#     def get_ProductBills2(cls, conection):
#         try:
#             cursor = conection.cursor()
#             sql = "SELECT ID_Factura, Monto, Fecha, Tipo, Descripcion, TipoEntidad, ID_Entidad, Estado, Cantidad FROM Factura WHERE TipoEntidad = 'Producto'"
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             bills_by_month = defaultdict(list)

#             for row in rows:
#                 product_id = row[6]
#                 product = ModelProduct.get_product_by_id(conection, product_id)

               
#                 if product:
#                     price = product.Price if product.Price is not None else 0  
#                     bill = {
#                         'ID_Bill': row[0],
#                         'Amount': row[1],
#                         'Date': row[2],
#                         'Type': row[3],
#                         'Description': row[4],
#                         'EntityType': row[5],
#                         'ID_Entity': product_id,
#                         'ProductCode': product.ID_Product,
#                         'Price': product.Price,
#                         'ProductName': product.Name,
#                         'QuantitySold': row[8],
#                         'TotalSold': row[8] * price,  
#                     }
#                     month_year = row[2].strftime('%Y-%m')
#                     bills_by_month[month_year].append(bill)

#             cursor.close()
#             return bills_by_month
#         except Exception as ex:
#             print(f"Error en get_ProductBills: {ex}") 
#             return None

#     # ---------- FACTURAS GENERALES ----------
#     @staticmethod
#     def get_general_reports(connection, agrupador):
#         """
#         agrupador = 'diaria' | 'semanal' | 'mensual'
#         Devuelve  { 'clave-grupo-str': [ fila_dict, ... ], ... }
#         """
#         try:
#             group_sql = {
#                 'diaria':  "DATE(F.Fecha)",
#                 'semanal': "YEARWEEK(F.Fecha,1)",
#                 'mensual': "DATE_FORMAT(F.Fecha,'%Y-%m')"
#             }
#             if agrupador not in group_sql:
#                 raise ValueError("Tipo de reporte no válido")

#             sql = f"""
#                 SELECT {group_sql[agrupador]}      AS group_key,
#                        F.ID_Factura,  F.Monto, F.Tipo, F.Descripcion,
#                        F.TipoEntidad, F.ID_Entidad, F.Estado, F.Fecha,
#                        COALESCE(C.Cedula,  E.Cedula)  AS Cedula,
#                        COALESCE(C.Nombre,  E.Nombre)  AS Nombre,
#                        P.Nombre                        AS Producto
#                 FROM   factura F
#                 LEFT JOIN cliente     C ON F.TipoEntidad='Cliente'    AND C.Cedula      = F.ID_Entidad
#                 LEFT JOIN entrenador  E ON F.TipoEntidad='Entrenador' AND E.Cedula      = F.ID_Entidad
#                 LEFT JOIN producto    P ON F.TipoEntidad='Producto'   AND P.ID_Producto = F.ID_Entidad
#                 ORDER BY group_key, F.Fecha
#             """

#             with connection.cursor(cursor=pymysql.cursors.DictCursor) as cur:
#                 cur.execute(sql)
#                 rows = cur.fetchall()

#             reports: dict[str, list[dict]] = {}
#             for row in rows:
#                 # -- aseguramos que la clave sea string serializable --
#                 gkey = row.pop('group_key')
#                 if isinstance(gkey, (date, datetime)):
#                     gkey = gkey.isoformat()          # 'YYYY-MM-DD'
#                 else:
#                     gkey = str(gkey)                 # YEARWEEK ó 'YYYY-MM'

#                 row['Monto'] = float(row['Monto'])   # útil para sumatorias

#                 reports.setdefault(gkey, []).append(row)

#             return reports

#         except Exception as ex:
#             print(f"Error en get_general_reports: {ex}")
#             return None
