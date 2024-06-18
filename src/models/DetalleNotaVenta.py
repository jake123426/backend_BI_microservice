class DetalleNotaVenta():

    def __init__(self,id,cantidad=None,descripcion=None,precio_unitario=None, sub_total=None, ventaproducto_id=None)->None:
        self.id = id
        self.cantidad = cantidad
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.sub_total = sub_total
        self.ventaproducto_id = ventaproducto_id


    def to_JSON(self):
        return{
            'id':self.id,
            'cantidad':self.cantidad,
            'descripcion':self.descripcion,
            'precio_unitario':self.precio_unitario,
            'sub_total':self.sub_total,
            'ventaproducto_id':self.ventaproducto_id,
        }