from flask import Blueprint, jsonify, request
import utils.DataAnalysis as dn
#Model
from models.VentaProducto import VentaProducto
from models.Producto import Producto
#Service
from services.ProductoService import ProductoService


ProductoController = Blueprint('ProductoController', __name__)


#-----------------------------------------------------------------------------------
@ProductoController.route('/productSalesByUserId/<id>')
def getProductSalesByUserId(id):
    try:        
        usuarioVentas = ProductoService.productSalesByUserId(id)        
        return jsonify(usuarioVentas), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#-----------------------------------------------------------------------------------
@ProductoController.route('/productSalesDetailsById/<id>')
def getProductSalesDetailsById(id):
    try:        
        ventaProductos = ProductoService.productSalesDetailsById(id)
        return jsonify(ventaProductos), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#-----------------------------------------------------------------------------------    
@ProductoController.route('/saveProductSale', methods=['POST'])
def saveProductSale():
    try:
        date = request.json['date']
        total_paid = float(request.json['total_paid'])
        user_id = int(request.json['user_id'])
        product_details = request.json['product_details']         
        ventaProducto = VentaProducto(0, date, total_paid, user_id)
        
        id = ProductoService.addProductSale(ventaProducto, product_details)  
        
        # ventaProductos = ProductoService.productSalesDetailsById(id)
        return jsonify("Se guardo el registro con exito"), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500

#------ruta para metodo GET ventaproducto-----------------------------------------------------------------------------
@ProductoController.route('/getAllProductSales')
def getAllProductSales():
    try:
        ventaProductos = ProductoService.getAllProductSales()
        return jsonify(ventaProductos), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}),500
    
#-----------------------------------------------------------------------------------
@ProductoController.route('/getProduct/<id>')
def getProduct(id):
    try:
        producto = ProductoService.getProduct(id)
        return jsonify(producto), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}),500
    
#-----------------------------------------------------------------------------------
@ProductoController.route('/getAllProducts')
def getAllProducts():
    try:
        productos = ProductoService.getAllProducts()
        return jsonify(productos), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}),500
#-----------------------------------------------------------------------------------

@ProductoController.route('/saveProduct', methods=['POST'])
def saveProduct():
    try:
        name = request.json['name']
        status = int(request.json['status'])
        purchase_price = float(request.json['purchase_price'])
        sale_price = float(request.json['sale_price'])
        
        producto = Producto(0, name, status, purchase_price, sale_price)
        affected_row = ProductoService.addProduct(producto)
        if affected_row == 1:
            return jsonify('Se guardo el producto'), 200
        else:
            return jsonify({'message':"Error on insert data"}), 500
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#-----------------------------------------------------------------------------------

    
@ProductoController.route('/product_category_profit', methods=['POST'])
def getProfitProductSales():
    try:
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        
        # Obtener los datos en formato json
        data_json = ProductoService.getProductSalesData(start_date, end_date)

        # Realizar el analisis
        data = dn.profitCategorySales(data_json)               
        
        return jsonify(data), 200        
    
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500