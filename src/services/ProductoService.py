from database.PostgresConnection import get_connection
from models.VentaProducto import VentaProducto
from models.Producto import Producto
from models.DetalleNotaVenta import DetalleNotaVenta
import json
from utils.DateFormat import DateFormat


class ProductoService():

#API metodo GET , devuelve una lista con todas las ventas hechas por un usuario   
    @classmethod
    def productSalesByUserId(self, id):
        try:
            connection = get_connection()
            ventas_de_usuario = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM product_sales WHERE product_sales.user_id = %s", (id,))
                resultset=cursor.fetchall()

                for row in resultset:
                    ventaProducto = VentaProducto(row[0],row[1],row[2],row[3])
                    ventas_de_usuario.append(ventaProducto.to_JSON())
            connection.close()
            return ventas_de_usuario
        except Exception as ex:
            raise Exception(ex)
#---------------------------------------------------------------------------------------------------------------------------    
#API metodo GET , devuelve una lista con las ventas de productos por Id y sus detalles   
    @classmethod
    def productSalesDetailsById(self, id):
        try:
            connection = get_connection()
            productos = []

            with connection.cursor() as cursor:                
                cursor.execute("SELECT date, total_paid, user_id FROM product_sales WHERE id=%s",(id,))                
                product_sale = cursor.fetchone()                
                if product_sale != None:
                    cursor.execute("SELECT p.name , dn.amount, dn.sub_total FROM detail_note_sales dn JOIN product p ON dn.id_product=p.id  WHERE id_product_sales=%s", (id,))
                    detalleNotaVentas = cursor.fetchall()
                    for detalle in detalleNotaVentas:                        
                        productos.append(
                            {
                                "product": detalle[0],
                                "amount": detalle[1], 
                                "sub_total": detalle[2],
                            }
                        )
                        data = {
                                "date": DateFormat.convert_date(product_sale[0]),
                                "totail_paid": product_sale[1],
                                "products": productos
                            }                          
                else:  
                    data = {}            
            connection.close()
            return data
        except Exception as ex:
            raise Exception(ex)
        
#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def addProductSale(self, ventaProducto, product_details):
            try:
                connection = get_connection()
                
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO product_sales (date, total_paid, user_id) VALUES (%s, %s, %s) ", 
                                (ventaProducto.date, ventaProducto.total_paid, ventaProducto.user_id))
                    connection.commit()       
                    cursor.execute("SELECT id FROM product_sales ORDER BY id DESC LIMIT 1")                    
                    productSale = cursor.fetchone()                    
                    if productSale != None :
                        for product in product_details:
                            cursor.execute(" INSERT INTO detail_note_sales (id_product_sales, id_product, amount, sub_total) VALUES (%s, %s, %s, %s) ", 
                                            (productSale[0], product['id_product'], product['amount'], 0))
                connection.commit()     
                connection.close()
                return productSale[0]
            except Exception as ex:
                raise Exception(ex) 
#----------------------------------------------------------------------------------------------------------------------------
#API metodo GET , devuelve una lista con todas las ventas de productos    
    @classmethod
    def getAllProductSales(self):
        try:
            connection = get_connection()            
            listaDetalles = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM product_sales")
                ventaProductos = cursor.fetchall()                
                for row in ventaProductos:                                     
                    cursor.execute("SELECT p.name , dn.amount, dn.sub_total FROM detail_note_sales dn JOIN product p ON dn.id_product=p.id  WHERE id_product_sales=%s", (row[0],))
                    detalleNotaVentas = cursor.fetchall()
                    productos = []
                    for detalle in detalleNotaVentas:                           
                        productos.append(
                            {
                                "name": detalle[0],
                                "amount": detalle[1], 
                                "sub_total": detalle[2],
                            }
                        )

                    listaDetalles.append(
                        {
                            "date": DateFormat.convert_date(row[1]),
                            "total_paid": row[2],
                            "user_id": row[3],
                            "products": productos 
                        }
                    )
            connection.close()
            return listaDetalles
        except Exception as ex:
            raise Exception(ex)
        
#-----------------------------------------------------------------------------------------------------------------------            
    @classmethod
    def getProduct(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
                row = cursor.fetchone()                
                producto = Producto(row[0], row[1], row[2], row[3], row[4])                
            connection.close()
            return producto.to_JSON()
        except Exception as ex:
            raise Exception(ex)

#-----------------------------------------------------------------------------------------------------------------------               
    @classmethod
    def getAllProducts(self):
        try:
            connection = get_connection()
            productos = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM product")
                resultset = cursor.fetchall()

                for row in resultset:
                    producto = Producto(row[0],row[1],row[2],row[3], row[4])
                    productos.append(producto.to_JSON())
            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)

#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def addProduct(self, producto):
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO product (name , status , purchase_price, sale_price) VALUES ( %s, %s, %s, %s) ", 
                        (producto.name, producto.status, producto.purchase_price, producto.sale_price))                    
                    affected_rows = cursor.rowcount
                    connection.commit()

                connection.close()
                return affected_rows
            except Exception as ex:
                raise Exception(ex)
            
#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def getProductSalesData(self, start_date, end_date):
        try:
            connection = get_connection()    
            # Consulta SQL para extraer los datos necesarios
            query = f"""
            SELECT p.name, ds.sub_total, ps.date
            FROM detail_note_sales ds
            JOIN product_sales ps ON ds.id_product_sales = ps.id
            JOIN product p ON ds.id_product = p.id
            WHERE ps.date BETWEEN '{start_date}' AND '{end_date}';
            """

            # Ejecuta la consulta y obtiene los datos
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Obtiene los nombres de las columnas
            colnames = [desc[0] for desc in cursor.description]    
            
            # Convierte los datos a una lista de diccionarios
            data = [dict(zip(colnames, row)) for row in rows]
            
            # Convierte la lista de diccionarios a JSON
            data_json = json.dumps(data, default=str)  # Usamos default=str para convertir fechas a cadenas
            
            # Cierra la conexión
            cursor.close()
            connection.close()
            
            return data_json
        except Exception as ex:
            raise Exception(ex)