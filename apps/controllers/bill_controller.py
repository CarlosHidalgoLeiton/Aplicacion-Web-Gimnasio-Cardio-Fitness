from apps.db.repositories.BillRepository import BillRepository
from apps.db.repositories.MembershipRepository import MembershipRepository
from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.ProductRepository import ProductRepository

class billController:
    BillRepository = BillRepository()
    MembershipRepository = MembershipRepository()
    ClientRepository = ClientRepository()
    ProductRepository = ProductRepository()
    
    @classmethod
    def get_all(cls):
        bills = cls.BillRepository.findAll()
        return bills
    
    @classmethod
    def get_one(cls,id):
         return cls.BillRepository.get_one(id)
    
    @classmethod
    def getDataTrainerBill(cls,request):
        trainer = cls.BillRepository.getDataTrainerBill(request)
        return trainer
    
    @classmethod
    def getDataGeneralBill(cls,request):
        general = cls.BillRepository.getDataGeneralBill(request)
        return general
    
    @classmethod 
    def getDataProductBill(cls,request):
        product = cls.BillRepository.getDataProductBill(request)
        return product
    
    @classmethod
    def validateDataFormTrainer(cls,data):
        trainer = cls.BillRepository.validateDataFormTrainer(data)
        return trainer
    
    @classmethod
    def validateDataFormGeneral(cls,data):
        general = cls.BillRepository.validateDataFormGeneral(data)
        return general
    
    @classmethod
    def validateDataFormProduct(cls,data):
        product = cls.BillRepository.validateDataFormProduct(data)
        return product
    
    @classmethod
    def create(cls, data):
        dataTrainer = cls.BillRepository.to_dict(data)
        trainer = cls.BillRepository.create(**dataTrainer)
        return trainer
    
    @classmethod
    def validateStock(cls, stock, lot):
        Validate = cls.BillRepository.validateStock(stock, lot)
        return Validate
    
    @classmethod
    def getDataMembershipBill(cls,request):
        membership = cls.BillRepository.getDataMembershipBill(request)
        return membership
    
    @classmethod
    def validateDataFormMembership(cls, data):
        membership = cls.BillRepository.validateDataFormMembership(data)
        return membership
    @classmethod
    def getDataMembership(cls,request):
        day= cls.MembershipRepository.getDataMembership(request)
        return day

    @classmethod
    def getDataMembershipClient(cls, request, days):
        data = cls.BillRepository.getDataMembershipClient(request,days)
        return data
    
    @classmethod
    def updateClientMembership(cls, client):
        id = client.DocumentId
        data = cls.ClientRepository.update(id,Registration_Date= client.Registration_Date,ExpirationMembership=client.ExpirationMembership,Membership_ID = client.Membership_ID)
        return data 


    def getDataMembershipDay(cls, membership_id):
        try:
            result = cls.findOneFiltered(
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
    def validateDataFormMembershipClient(cls,data):
        client = cls.BillRepository.validateDataFormMembershipClient(data)
        return client
    
    @classmethod
    def disable_bill(cls, id):
        return cls.BillRepository.disable_bill(id)
    
    @classmethod
    def get_allAble(cls):
        filters = {'State': True}
        Bills = cls.BillRepository.findAll(filters=filters)
        return Bills
    
    @classmethod
    def get_product_bills(cls):
        filters = {'EntityType': 'Producto'}
        return cls.BillRepository.findAll(filters=filters)
    
    @classmethod
    def get_productOne_bill(cls, month):
        filters = {'EntityType': 'Producto'}
        all_bills = cls.BillRepository.findAll(filters=filters)
        
        for bill in all_bills:
            date = bill.get('Date')
            if date and date.month == int(month):
                filterProduct = {'ID_Product': bill['ID_Entity']}
                product = cls.ProductRepository.findOne(filters=filterProduct)
                bill['product'] = product
                return bill  # Devuelve la primera factura que coincida
        return None

    @classmethod
    def get_reports(cls, group_by):
        return cls.BillRepository.get_reports(group_by=group_by)
    
    @classmethod
    def get_product_bills(cls):
        return cls.BillRepository.get_ProductBills()

    @classmethod
    def get_reports_bills(cls, group_by):
        return cls.BillRepository.get_reports_bills(group_by=group_by)
    
    @classmethod
    def updateQuantityProduct(cls, quantity, id):
        return cls.ProductRepository.quantity_Product(quantity, id)