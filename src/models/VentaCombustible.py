from utils.DateFormat import DateFormat

class VentaCombustible():

    def __init__(self, id=None, fecha=None, precio=None, cantidad=None, usuario_id=None) -> None:
        self.id = id
        self.date = fecha
        self.price = precio
        self.quantity = cantidad
        self.user_id = usuario_id

    def to_JSON(self):
        return{
            'id':self.id,
            'date': DateFormat.convert_date(self.date),
            'price': self.price,
            'quantity': self.quantity,
            'user_id': self.user_id,
        }