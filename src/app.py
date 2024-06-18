from flask import Flask
from flask_cors import CORS 

from controllers.CombustibleController import CombustibleController
from controllers.ProductoController import ProductoController

app = Flask(__name__)
CORS(app, origins="*")

if __name__ == '__main__':
    
    app.register_blueprint( CombustibleController, url_prefix='/api/fuel')
    app.register_blueprint( ProductoController, url_prefix='/api/product')
        
    app.run( debug=True, port=5000 )