from apps.db.models.CancelledBill import CancelledBill
from datetime import datetime
from pymysql import IntegrityError
from apps.db.repositories.RepositoryBase import RepositoryBase

class BillRepository(RepositoryBase):
    
        def __init__(self):
         super().__init__(CancelledBill)

        @classmethod
        def getDataCanceledBill(cls, request):
            motive = request.form['Motive']
            idBill = request.form['ID_Bill']

            return CancelledBill(Motive=motive,CancelledDate=datetime.now(),ID_Bill=idBill)

        @classmethod
        def validateDataForm(cls, cancelledBill):
            if cancelledBill.Motive == None:
                return "Debe ingresar el motivo de la anulación de la factura."
            
            if cancelledBill.ID_Bill == None:
                return "No se encontró el número de factura."
            
            return True