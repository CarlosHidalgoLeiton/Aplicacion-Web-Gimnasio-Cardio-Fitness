from datetime import datetime, timedelta, date
from collections import defaultdict
import re
from apps.db.models.Bill import Bill
from apps.db.models.Client import Client
from apps.db.repositories.RepositoryBase import RepositoryBase

class BillRepository(RepositoryBase):
    
    def __init__(self):
        super().__init__(Bill)
    
    def disable_bill(self, id):
        return self.update(id, State=0) 



    @classmethod
    def getDataTrainerBill(cls, request):
        # Obtener y convertir datos del formulario
        amount = request.form['AmountTrainerBill']
        description = request.form['Description']
        id_entity = request.form['DocumentIdTrainer']

        return Bill(
            Amount=amount,
            Type="Pago Entrenador",  # puedes cambiar esto si necesitás otro tipo
            Description=description,
            Date=datetime.now(),
            EntityType="Entrenador",
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
        ID_Entity = request.form['DocumentIdProduct']
        Amount = request.form['AmountProductBill']
        Description = request.form['Description']
        Lot = request.form['Amount']

        return Bill(Amount=Amount,Type="Pago Producto",Description=Description,Date=datetime.now(),EntityType="Producto",ID_Entity=ID_Entity, State=True, Lot=Lot)


    @classmethod
    def getDataMembershipBill(cls, request):
        ID_Entity = request.form['DocumentIdClient']
        Amount = request.form['AmountMembershipBill']
        Description = request.form['Description']

        return Bill(Amount=Amount, Type="Pago Membresia", Description=Description, Date=datetime.now(),EntityType="Cliente",ID_Entity=ID_Entity,State=True,Lot=None)
    
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

    @classmethod
    def getDataMembershipClient(self, membership_id):
        try:
            result = self.findOneFiltered(
                column_names=["Duracion_Dias"],
                filters={"ID_Membresia": membership_id}
            )

            if result:
                return result["Duracion_Dias"]
            return None
        except Exception as ex:
            print(f"Error al obtener duración de la membresía: {ex}")
            return None


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
        fecha_ingreso = datetime.now()

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
        
        if bill.ID_Entity == "":
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
        
        if bill.Lot != None:
            if "-" in bill.Lot or not bill.Lot.isdigit(): #Valida que sea alfabetico y que no tenga un "-" 
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

                if lot_int < stock_int:
                    return True
                else:
                    return False
            else:
                return False
        except (ValueError, TypeError) as ex:
            print(f"Error al convertir lot o stock a entero: {ex}")
            return False