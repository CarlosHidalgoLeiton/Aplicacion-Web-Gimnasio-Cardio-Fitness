from apps.db.repositories.ProductRepository import ProductRepository

from apps.db.models.Product import Product

from apps.utils.utils import getDataProductInsert, getDataUpdateProductUpdate, validateDataProduct
import base64

class productController:

    ProductRepository = ProductRepository()


    @classmethod
    def get_all(cls):
        products = cls.ProductRepository.findAll()

        for product in products:
            if product.get('Image'):
                # Codifica el binario a base64
                product['Image'] = base64.b64encode(product['Image']).decode('utf-8')
    
        return products

        
    @classmethod
    def getProductById(cls,id):
        try:
            # Obtener la estadística con sus relaciones
            product = cls.ProductRepository.get_one(id,)

            if not product:
                raise Exception(f"Error al obtener el producto {id}.")

            return product
        except Exception as ex:
            raise Exception(f'Error en productController.getProductById: {ex}')
        
    @classmethod
    def getDataProduct(cls, request, image):
            return getDataProductInsert(request, image) 
    
    @classmethod
    def getDataUpdateProduct(cls, request, image):
            return getDataUpdateProductUpdate(request, image) 

        
    @classmethod
    def productValidated(cls, request):
           # Validar que el product no exista ya
            existing_product = cls.ProductRepository.findOne({'Name': request.Name})
            if existing_product:
                return f"Ya existe un producto registrado con el mismo nombre '{request.Name}'."
            else:
                return  validateDataProduct(request)
            

    @classmethod
    def productValidatedUpdate(cls, Name, request):
        if Name == request.Name:
             return  validateDataProduct(request)
        else:
            existing_product = cls.ProductRepository.findOne({'Name': request.Name})
            if existing_product:
                return f"Ya existe un producto registrado con el mismo nombre'{request.Name}'."
            return  validateDataProduct(request)
           

    @classmethod
    def create(cls, data):
        dataProduct = cls.ProductRepository.to_dict(data)
        product = cls.ProductRepository.create(**dataProduct)
        return product
    
    @classmethod
    def updateProduct(cls,id, data):
        dataProduct = cls.ProductRepository.to_dict(data)
        product = cls.ProductRepository.update(id,**dataProduct)
        return product

    @classmethod
    def get_one(cls,id):
         return cls.ProductRepository.get_one(id)

    @classmethod
    def disable_product(cls, id):
         return cls.ProductRepository.disable_product(id)
    
    @classmethod
    def able_Product(cls, id):
         return cls.ProductRepository.able_Product(id)
    
    @classmethod
    def get_allAble(cls):
        filters = {'State': True}
        products = cls.ProductRepository.findAll(filters=filters)
        if not products:
            raise Exception('No se encontraron productos')
        return products
    
    @classmethod
    def get_stock(cls,product_id):
        stock= cls.ProductRepository.get_stock(product_id)
        return stock
    
    