from utils.DateFormat import DateFormat

class VentaProducto():

    def __init__( self, id=None, fecha=None, total_pagar=None, usuario_id=None ) -> None:
        self.id = id
        self.date = fecha
        self.total_paid = total_pagar
        self.user_id = usuario_id

    def to_JSON(self):
        return{
            'id':self.id,
            'date':DateFormat.convert_date(self.date),
            'total_paid':self.total_paid,
            'user_id':self.user_id,
        }