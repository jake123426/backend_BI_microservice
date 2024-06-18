from flask import Blueprint, jsonify, request
import uuid
import utils.DataAnalysis as dn
from utils.DateFormat import DateFormat

#Model
from models.VentaCombustible import VentaCombustible
#Service
from services.CombustibleService import CombustibleService

CombustibleController = Blueprint('CombustibleController', __name__)

#------ ruta para obtener todas las ventas de combustible -----------------------------------------------------------------------------
@CombustibleController.route('/getAllFuelSales')
def getAllFuelSales():
    try:
        ventaCombustibles = CombustibleService.getAllFuelSales()
        return jsonify(ventaCombustibles), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#-----------------------------------------------------------------------------
@CombustibleController.route('/fuelSalesByUserId/<id>') 
def getFuelSaleByUserId(id):
    try:
        ventaCombustibles = CombustibleService.fuelSaleByUserId(id)
        # print("El total de elementos en la lista es: " , len(ventaCombustibles))
        return jsonify(ventaCombustibles), 200
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#------ ruta para guardar una venta de combustible -----------------------------------------------------------------------------
@CombustibleController.route('/saveFuelSale', methods=['POST'])
def saveFuelSale():
    try:
        # date = DateFormat.stringDate_to_fomattedDate(request.json['date'])
        date = request.json['date']                
        price = float(request.json['price'])
        quantity = float(request.json['quantity'])
        user_id = int(request.json['user_id']) 
        
        ventaCombustible = VentaCombustible( 0, date, price , quantity, user_id)
        
        affected_row = CombustibleService.addFuelSale(ventaCombustible)

        if affected_row == 1:
            return jsonify('Se guardo la venta de combustible'), 200
        else:
            return jsonify({'message':"Error on insert data"}), 500        
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
#-----------------------------------------------------------------------------------

@CombustibleController.route('/quantity_fuel_month', methods=['POST'])
def getQuantityFuelSold():
    try:
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        
        # Obtener los datos en formato json
        data_json = CombustibleService.getFuelSalesData(start_date, end_date)

        # Realizar el analisis
        data = dn.quantityFuelSold(data_json)               
        
        return jsonify(data), 200        
    
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500
    
#-----------------------------------------------------------------------------------
    
@CombustibleController.route('/fuel_profit_month', methods=['POST'])
def getProfitFuelSales():
    try:
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        
        # Obtener los datos en formato json
        data_json = CombustibleService.getFuelSalesData(start_date, end_date)

        # Realizar el analisis
        data = dn.profitFuelSales(data_json)               
        
        return jsonify(data), 200        
    
    except Exception as ex:
        return jsonify({'message':str(ex)}), 500



