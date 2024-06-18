import json
from database.PostgresConnection import get_connection
from models.VentaCombustible import VentaCombustible

class CombustibleService():

#---------------------------------------------------------------------------------------------------------------------------    
    @classmethod
    def getAllFuelSales(self):
        try:
            connection = get_connection()
            ventaCombustibles = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM fuel_sales")
                resultset = cursor.fetchall()

                for row in resultset:
                    ventaCombustible = VentaCombustible(row[0], row[1], row[2], row[3], row[4])
                    ventaCombustibles.append(ventaCombustible.to_JSON())
            connection.close()            
            return ventaCombustibles
        except Exception as ex:
            raise Exception(ex)

#-----------------------------------------------------------------------------------------------------
    @classmethod
    def fuelSaleByUserId(self,id):
            try:
                connection = get_connection()
                lista_ventas_combustible_usuario = []

                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM fuel_sales WHERE fuel_sales.user_id =  %s", (id,))
                    resultset = cursor.fetchall()

                    for row in resultset:
                        usuarioVentaCombustible = VentaCombustible(row[0],row[1],row[2],row[3],row[4],)
                        lista_ventas_combustible_usuario.append(usuarioVentaCombustible.to_JSON())
                connection.close()
                return lista_ventas_combustible_usuario
            except Exception as ex:
                raise Exception(ex)

#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def addFuelSale(self, ventaCombustible):
            try:
                connection = get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO fuel_sales (date, price , quantity ,user_id) VALUES ( %s, %s, %s, %s) ", 
                        (ventaCombustible.date, ventaCombustible.price, ventaCombustible.quantity, ventaCombustible.user_id))                    
                    affected_rows = cursor.rowcount
                    connection.commit()

                connection.close()
                return affected_rows
            except Exception as ex:
                raise Exception(ex) 
#----------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def getFuelSalesData(self, start_date, end_date):
        try:
            connection = get_connection()            
            # Define tu consulta SQL
            # query = "SELECT * FROM fuel_sales;"
            query = f"""
                    SELECT * FROM fuel_sales
                    WHERE date >= '{start_date}' AND date <= '{end_date}';
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
