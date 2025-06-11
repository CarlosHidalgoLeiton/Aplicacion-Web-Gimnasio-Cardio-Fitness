
from apps.db.repositories.CancelledBillRepository import BillRepository


class cancelledBillController:

    BillRepository = BillRepository()

    @classmethod
    def getCancelBill(cls, id_factura):
        try:
            result = cls.BillRepository.findOneFiltered(
                column_names=["Motive", "CancelledDate"],
                filters={"ID_Bill": id_factura}
            )
            return result  # Diccionario con claves: 'Motivo', 'FechaAnulacion' o None
        except Exception as ex:
            print(f"Error en get_cancelled_bill: {ex}")
            return None
        

    @classmethod
    def getDataCanceledBill(cls,request):
        return cls.BillRepository.getDataCanceledBill(request) 
    
    @classmethod
    def validateDataForm(cls,cancelBill):
        return cls.BillRepository.validateDataForm(cancelBill)
    
    @classmethod
    def create(cls, data):
        dataCancelledBill = cls.BillRepository.to_dict(data)
        cliente = cls.BillRepository.create(**dataCancelledBill)
        return cliente
    
    @classmethod
    def disable_client(cls, id):
        return cls.BillRepository.disable_client(id)


