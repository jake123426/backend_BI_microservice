class Producto():

    def __init__(self,id=None, nombre=None, estado=None, precio_compra=None, precio_venta=None) -> None:
        self.id = id
        self.name = nombre
        self.status = estado
        self.purchase_price = precio_compra
        self.sale_price = precio_venta


    def to_JSON(self):
        return{
            'id':self.id,
            'name':self.name,
            'status':self.status,
            'purchase_price':self.purchase_price,
            'sale_price':self.sale_price,
        }