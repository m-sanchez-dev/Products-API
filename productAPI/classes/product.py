""" Product class """
class Product:

    # Init the object
    def __init__(self, productId: str, name: str, brand: str, retailer: str, price: float, inStock: str):
        self.productId = productId
        self.name = name
        self.brand = brand
        self.retailer = retailer
        self.price = price
        self.inStock = inStock

    # productId getter
    def getProductId(self) -> str:
        return self.productId