from datetime import datetime, timedelta, date, datetime
from collections import defaultdict
import re
from apps.db.models.Bill import Bill
from apps.db.models.Client import Client
from apps.db.repositories.RepositoryBase import RepositoryBase
from apps.db.db import db
from sqlalchemy import text
import pytz

class BillRepository(RepositoryBase):
    
    def __init__(self):
        super().__init__(Bill)

    @classmethod
    def get_ProductBills(cls):
        try:
            sql = text("""
                SELECT ID_Factura, Monto, Fecha, Tipo, Descripcion, TipoEntidad, ID_Entidad, Estado, Cantidad 
                FROM factura 
                WHERE TipoEntidad = 'Producto'
            """)
            rows = db.session.execute(sql).fetchall()

            bills_by_month = defaultdict(list)

            for row in rows:
                product_id = row.ID_Entidad

                # Obtener detalles del producto
                product_sql = text("SELECT ID_Producto, Nombre, Precio FROM producto WHERE ID_Producto = :id")
                product_row = db.session.execute(product_sql, {'id': product_id}).fetchone()

                if product_row:
                    bill = {
                        'ID_Producto': product_row.ID_Producto,
                        'Precio': product_row.Precio,
                        'Nombre_Producto': product_row.Nombre,
                        'Cantidad': row.Cantidad,
                        'Total_Vendido': row.Cantidad * product_row.Precio,
                        'ID_Factura': row.ID_Factura,
                        'Monto': row.Monto,
                        'Tipo': row.Tipo,
                        'Descripcion': row.Descripcion,
                        'TipoEntidad': row.TipoEntidad or 'Desconocido',
                        'ID_Entidad': row.ID_Entidad,
                        'Estado': row.Estado,
                        'Fecha': row.Fecha,
                        'Cantidad': row.Cantidad
                    }

                    # Agrupación por mes y año
                    month_year = row.Fecha.strftime('%Y-%m') if isinstance(row.Fecha, (datetime, date)) else str(row.Fecha)
                    bills_by_month[month_year].append(bill)

            return dict(bills_by_month)

        except Exception as ex:
            print(f"Error en get_ProductBills: {ex}")
            return None

    @classmethod
    def get_reports_bills(cls, group_by):
        try:
            # Definir agrupamiento por tipo
            group_sql = {
                'diaria': "DATE(Fecha)",
                'semanal': "YEARWEEK(Fecha, 1)",
                'mensual': "DATE_FORMAT(Fecha, '%Y-%m')"
            }

            if group_by not in group_sql:
                raise ValueError("Tipo de reporte no válido: 'diaria', 'semanal', 'mensual'.")

            # Consulta SQL principal
            sql = f"""
                SELECT {group_sql[group_by]} AS group_key, ID_Factura, Cantidad, Monto, Tipo, Descripcion,
                       TipoEntidad, ID_Entidad, Estado, Fecha
                FROM factura
                ORDER BY group_key
            """

            result = db.session.execute(text(sql)).fetchall()

            reports = defaultdict(list)

            for row in result:
                group_key = row.group_key

                if isinstance(group_key, (datetime, date)):
                    group_key = group_key.strftime('%Y-%m-%d') if group_by == 'diaria' else group_key.strftime('%Y-%m')

                report = {
                    'ID_Factura': row.ID_Factura,
                    'Monto': row.Monto,
                    'Tipo': row.Tipo,
                    'Descripcion': row.Descripcion,
                    'TipoEntidad': row.TipoEntidad or 'Desconocido',
                    'ID_Entidad': row.ID_Entidad,
                    'Estado': row.Estado,
                    'Fecha': row.Fecha,
                    'Cantidad': row.Cantidad
                }

                # Consultar datos de entidad relacionada
                tipo_entidad = row.TipoEntidad
                id_entidad = row.ID_Entidad

                if tipo_entidad in ('cliente', 'entrenador'):
                    entity_sql = text(f"SELECT Cedula, Nombre FROM {tipo_entidad} WHERE Cedula = :cedula")
                    entity_row = db.session.execute(entity_sql, {'cedula': id_entidad}).fetchone()
                    if entity_row:
                        report['Cedula'] = entity_row.Cedula
                        report['Nombre'] = entity_row.Nombre
                elif tipo_entidad == 'Producto':
                    product_sql = text("SELECT Nombre FROM producto WHERE ID_Producto = :id")
                    product_row = db.session.execute(product_sql, {'id': id_entidad}).fetchone()
                    if product_row:
                        report['Producto'] = product_row.Nombre

                reports[group_key].append(report)

            return dict(reports)

        except Exception as ex:
            print(f"Error en get_reports_bill: {ex}")
            return None

    @classmethod
    def get_reports(cls, group_by):
        try:
            # Definir formato de agrupación
            group_sql = {
                'diaria': "DATE(Fecha)",
                'semanal': "YEARWEEK(Fecha, 1)",
                'mensual': "DATE_FORMAT(Fecha, '%Y-%m')"
            }

            if group_by not in group_sql:
                raise ValueError("Tipo de agrupación no válido: 'diaria', 'semanal', 'mensual'.")

            sql = text(f"""
                SELECT {group_sql[group_by]} AS group_key, ID_Factura, Cantidad, Monto, Tipo, Descripcion,
                    TipoEntidad, ID_Entidad, Estado, Fecha
                FROM factura
                ORDER BY group_key
            """)

            result = db.session.execute(sql).fetchall()

            reports = defaultdict(list)
            totals = defaultdict(float)

            for row in result:
                group_key = row.group_key

                # Normaliza el group_key a string según el tipo de agrupación
                if group_by == 'diaria':
                    if isinstance(group_key, (datetime, date)):
                        group_key = group_key.strftime('%Y-%m-%d')
                    else:
                        group_key = str(group_key)
                elif group_by == 'mensual':
                    if isinstance(group_key, (datetime, date)):
                        group_key = group_key.strftime('%Y-%m')
                    else:
                        group_key = str(group_key)
                elif group_by == 'semanal':
                    group_key = str(group_key)  # YEARWEEK ya devuelve un int o string

                report = {
                    'ID_Factura': row.ID_Factura,
                    'Monto': row.Monto,
                    'Tipo': row.Tipo,
                    'Descripcion': row.Descripcion,
                    'TipoEntidad': row.TipoEntidad or 'Desconocido',
                    'ID_Entidad': row.ID_Entidad,
                    'Estado': row.Estado,
                    'Fecha': row.Fecha,
                    'Cantidad': row.Cantidad
                }

                tipo_entidad = row.TipoEntidad

                # Buscar entidad relacionada
                if tipo_entidad in ('cliente', 'entrenador'):
                    entity_sql = text(f"SELECT Cedula, Nombre FROM {tipo_entidad} WHERE Cedula = :cedula")
                    entity_result = db.session.execute(entity_sql, {'cedula': row.ID_Entidad}).fetchone()
                    if entity_result:
                        report['Cedula'] = entity_result.Cedula
                        report['Nombre'] = entity_result.Nombre
                elif tipo_entidad == 'Producto':
                    product_sql = text("SELECT Nombre FROM producto WHERE ID_Producto = :id")
                    product_result = db.session.execute(
                        product_sql,
                        {'id': row.ID_Entidad}
                    ).fetchone()
                    if product_result:
                        report['Producto'] = product_result.Nombre

                reports[group_key].append(report)
                totals[group_key] += float(row.Monto or 0)

            return {
                'data': dict(reports),
                'totals': dict(totals)
            }

        except Exception as ex:
            print(f"Error en get_reports: {ex}")
            return None
    
    def disable_bill(self, id):
        return self.update(id, State=0) 

    @classmethod
    def getDataTrainerBill(cls, request):
        # Obtener y convertir datos del formulario
        amount = request.form['AmountTrainerBill']
        description = request.form['Description']
        id_entity = request.form.get('DocumentIdTrainer')

        return Bill(
            Amount=amount,
            Type="Pago Entrenador",  # puedes cambiar esto si necesitás otro tipo
            Description=description,
            Date=datetime.now(),
            EntityType="entrenador",
            ID_Entity=id_entity,
            State=True,
            Lot=None # o generarlo dinámicamente si hace falta
        )


    @classmethod
    def getDataGeneralBill(cls, request):
        Amount = request.form['AmountGeneralBill']
        Description = request.form['Description']

        return Bill(Amount=Amount, Type="Pago General", Description=Description, Date=datetime.now(), EntityType="General", ID_Entity=0,  State=True, Lot=None)
    
    @classmethod
    def getDataProductBill(cls, request):
        ID_Entity = request.form.get('DocumentIdProduct')
        Amount = request.form.get('AmountProductBill')
        Description = request.form['Description']
        Quantity = request.form.get('Amount')

        return Bill(Amount=Amount,Type="Pago Producto",Description=Description,Date=datetime.now(),EntityType="Producto",ID_Entity=ID_Entity, State=True,Lot= None, Quantity=Quantity)


    @classmethod
    def getDataMembershipBill(cls, request):
        ID_Entity = request.form.get('DocumentIdClient')
        Amount = request.form.get('AmountMembershipBill')
        Description = request.form.get('Description')

        return Bill(Amount=Amount, Type="Pago Membresia", Description=Description, Date=datetime.now(),EntityType="cliente",ID_Entity=ID_Entity,State=True,Lot=None)
    
    @classmethod
    def validateDataFormTrainer(cls, bill):
        
        if not bill.ID_Entity:
            return "Debe seleccionar el entrenador."
        
        if bill.Amount != None:
            if "-" in bill.Amount or not bill.Amount.isdigit(): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def validateDataFormGeneral(cls, bill):
        
        if bill.Amount != None:
            if "-" in bill.Amount and not any( m.isalpha() for m in bill.Amount): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def validateDataFormMembership(cls, bill):
        
        if not bill.ID_Entity:
            return "Debe seleccionar el producto."
        
        if bill.Amount:
            # Remueve cualquier espacio en blanco alrededor del monto
            amount = bill.Amount.strip()
    
            # Verifica si el monto comienza con el signo de colones (₡) y quítalo para validar los números
            if amount.startswith("₡"):
                amount = amount[1:].strip()  # Elimina el símbolo de colón

            # Valida que el monto no contenga un "-" y que el resto sea un número
            try:
                amount_float = float(amount)  # Intenta convertir a número decimal
                if amount_float < 0:
                    return "El monto ingresado no es válido."
                
                # Actualiza el valor de bill.Amount con el monto limpio
                bill.Amount = amount_float  # Sobrescribimos el valor limpio sin el símbolo
            except ValueError:
                return "El monto ingresado no es válido."
        else:
            return "Debe ingresar un monto."


        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True

    @classmethod
    def validateDataFormMembershipClient(cls,client):
        # Validaciones del formulario
        if not client.DocumentId:
            return "Debe seleccionar un cliente."
        
        if not client.Membership_ID:
            return "Debe seleccionar una membresía."
        
        if not client.Registration_Date:
            return "No se logro obtener la fecha actual"
        
        if not client.ExpirationMembership:
            return "No se logro obtener la duracion"
        return True

    # @classmethod
    # def getDataMembershipClient(self, membership_id):
    #     try:
    #         result = self.findOneFiltered(
    #             column_names=["Duracion_Dias"],
    #             filters={"ID_Membresia": membership_id}
    #         )

    #         if result:
    #             return result["Duracion_Dias"]
    #         return None
    #     except Exception as ex:
    #         print(f"Error al obtener duración de la membresía: {ex}")
    #         return None


    @classmethod
    def get_membership_duration(self, membership_id):
        try:
            result = self.findOneFiltered(
                column_names=["Duracion_Dias"],
                filters={"ID_Membresia": membership_id}
            )
            if result:
                return result["Duracion_Dias"]
            return None
        except Exception as ex:
            print(f"Error al obtener la duración de la membresía con ID {membership_id}: {ex}")
            return None


    @classmethod
    def getDataMembershipClient(cls,request,membership_days):
        documentId = request.form['DocumentIdClient']
        membershipId = request.form['DocumentIdMembresia']

        if membership_days is None:
            return "Tipo de membresía no encontrado"
        # Obtener la fecha actual
        zona = pytz.timezone("America/Costa_Rica")
        fecha_ingreso = datetime.now(zona)

        # Calcular la fecha de vencimiento sumando los días de la membresía
        vencimiento_membresia = fecha_ingreso + timedelta(days=membership_days)


        # Retornar el objeto Client con la información necesaria
        return Client(
                DocumentId=documentId,
                Name=None,
                First_LastName=None,
                Second_LastName=None,
                Date_Birth=None,
                Age=None,
                Mail=None,
                Phone=None,
                Registration_Date=fecha_ingreso,
                Occupation=None,
                TelephoneEmergency=None,
                Address=None,
                Entry_Date=None,
                Ailments=None,
                Limitation=None,
                ExpirationMembership=vencimiento_membresia,
                State=None,
                Membership_ID=membershipId
            )
    
    @classmethod
    def validateDataFormProduct(cls, bill):
        
        if bill.ID_Entity == "" or bill.ID_Entity is None:
            return "Debe seleccionar el producto."
                
        if bill.Amount:
            # Remueve cualquier espacio en blanco alrededor del monto
            amount = bill.Amount.strip()
    
            # Verifica si el monto comienza con el signo de colones (₡) y quítalo para validar los números
            if amount.startswith("₡"):
                amount = amount[1:].strip()  # Elimina el símbolo de colón

            # Valida que el monto no contenga un "-" y que el resto sea un número
            try:
                amount_float = float(amount)  # Intenta convertir a número decimal
                if amount_float < 0:
                    return "El monto ingresado no es válido."
                
                # Actualiza el valor de bill.Amount con el monto limpio
                bill.Amount = amount_float  # Sobrescribimos el valor limpio sin el símbolo
            except ValueError:
                return "El monto ingresado no es válido."
        else:
            return "Debe ingresar un monto."


        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        if bill.Quantity != None:
            if "-" in bill.Quantity or not bill.Quantity.isdigit(): #Valida que sea alfabetico y que no tenga un "-" 
                return "La cantidad ingresada no es válida."
        else:
            return "Debe de ingresar la cantidad."

        return True
    

    @classmethod
    def validateStock(cls, stock, lot):
        try:
            if lot is not None and stock is not None:
                lot_int = int(lot)
                stock_int = int(stock)

                if lot_int <= stock_int:
                    return True
                else:
                    return False
            else:
                return False
        except (ValueError, TypeError) as ex:
            print(f"Error al convertir lot o stock a entero: {ex}")
            return False