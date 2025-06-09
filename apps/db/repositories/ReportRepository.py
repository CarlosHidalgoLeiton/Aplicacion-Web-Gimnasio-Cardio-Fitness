# apps/db/repositories/reportRepository.py
from datetime import date, datetime
import pymysql.cursors


class reportRepository:

    # ---------- INVENTARIO (ventas por producto) ----------
    @staticmethod
    def get_product_bills(connection):
        """
        Devuelve  { 'YYYY-MM': [ fila_dict, ... ], ... }
        """
        try:
            with connection.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT p.Codigo AS ProductCode,
                           p.Nombre AS ProductName,
                           p.Precio AS Price,
                           SUM(dp.Cantidad)               AS QuantitySold,
                           SUM(dp.Cantidad * p.Precio)    AS TotalSold,
                           DATE_FORMAT(f.Fecha,'%Y-%m')   AS Mes
                    FROM   detalleproducto dp
                    JOIN   productos       p ON p.Codigo   = dp.producto
                    JOIN   facturas        f ON f.Codigo   = dp.factura
                    GROUP  BY Mes, ProductCode
                    ORDER  BY Mes DESC
                """
                cur.execute(sql)
                registros = cur.fetchall()

            # Agrupar por Mes
            grouped: dict[str, list[dict]] = {}
            for row in registros:
                month = row['Mes']
                grouped.setdefault(month, []).append(row)

            return grouped

        except Exception as e:
            print(f"Error en get_product_bills: {e}")
            return None

    # ---------- FACTURAS GENERALES ----------
    @staticmethod
    def get_general_reports(connection, agrupador):
        """
        agrupador = 'diaria' | 'semanal' | 'mensual'
        Devuelve  { 'clave-grupo-str': [ fila_dict, ... ], ... }
        """
        try:
            group_sql = {
                'diaria':  "DATE(F.Fecha)",
                'semanal': "YEARWEEK(F.Fecha,1)",
                'mensual': "DATE_FORMAT(F.Fecha,'%Y-%m')"
            }
            if agrupador not in group_sql:
                raise ValueError("Tipo de reporte no válido")

            sql = f"""
                SELECT {group_sql[agrupador]}      AS group_key,
                       F.ID_Factura,  F.Monto, F.Tipo, F.Descripcion,
                       F.TipoEntidad, F.ID_Entidad, F.Estado, F.Fecha,
                       COALESCE(C.Cedula,  E.Cedula)  AS Cedula,
                       COALESCE(C.Nombre,  E.Nombre)  AS Nombre,
                       P.Nombre                        AS Producto
                FROM   factura F
                LEFT JOIN cliente     C ON F.TipoEntidad='Cliente'    AND C.Cedula      = F.ID_Entidad
                LEFT JOIN entrenador  E ON F.TipoEntidad='Entrenador' AND E.Cedula      = F.ID_Entidad
                LEFT JOIN producto    P ON F.TipoEntidad='Producto'   AND P.ID_Producto = F.ID_Entidad
                ORDER BY group_key, F.Fecha
            """

            with connection.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)
                rows = cur.fetchall()

            reports: dict[str, list[dict]] = {}
            for row in rows:
                # -- aseguramos que la clave sea string serializable --
                gkey = row.pop('group_key')
                if isinstance(gkey, (date, datetime)):
                    gkey = gkey.isoformat()          # 'YYYY-MM-DD'
                else:
                    gkey = str(gkey)                 # YEARWEEK ó 'YYYY-MM'

                row['Monto'] = float(row['Monto'])   # útil para sumatorias

                reports.setdefault(gkey, []).append(row)

            return reports

        except Exception as ex:
            print(f"Error en get_general_reports: {ex}")
            return None
