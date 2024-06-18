import pandas as pd
import json

def quantityFuelSold( data_json ):
    # Crea un DataFrame de Pandas desde el JSON
    df = pd.read_json(data_json)
    
    # Define el período de tiempo (puedes ajustarlo según tus necesidades)
    # start_date = '2023-01-01'
    # end_date = '2024-06-17'
    
    # Convertir la columna 'date' a tipo datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Filtrar los datos por el período de tiempo especificado
    # filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # # Crear una nueva columna para el año y mes
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Calcular la cantidad total de combustible vendida por mes
    total_quantity_per_month = df.groupby('year_month')['quantity'].sum().reset_index()
    
    # Redondea los valores del campo quantity a 2 decimales
    total_quantity_per_month['quantity'] = total_quantity_per_month['quantity'].round(2)
    
    # Convierte los valores de la columna year_month a cadenas de texto (strings)
    total_quantity_per_month['year_month'] = total_quantity_per_month['year_month'].astype(str)   
    
    # Convertir los datos a formato JSON
    data = total_quantity_per_month.to_dict(orient='records')
    
    # Mostrar los datos en formato JSON
    # print(json.dumps(data, indent=4))
    
    # Crear listas separadas para quantity y year_month
    quantities = total_quantity_per_month['quantity'].tolist()
    year_months = total_quantity_per_month['year_month'].tolist()

    # Preparar la respuesta en el formato solicitado
    response_data = {
        "quantities": quantities,
        "year_months": year_months
    }
    
    return response_data    

def profitFuelSales( data_json ):
    # Crea un DataFrame de Pandas desde el JSON
    df = pd.read_json(data_json)
    
    # Convertir la columna 'date' a tipo datetime
    df['date'] = pd.to_datetime(df['date'])    
    
    #  Crear una nueva columna para el año y mes
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Calcular las ganancias por mes
    total_revenue_per_month = df.groupby('year_month')['price'].sum().reset_index()

    # Convertir los valores de 'year_month' a cadenas de texto
    total_revenue_per_month['year_month'] = total_revenue_per_month['year_month'].astype(str)

    # Redondear los valores del campo revenue a 2 decimales
    total_revenue_per_month['price'] = total_revenue_per_month['price'].round(2)

    # Crear listas separadas para revenue y year_month
    profit = total_revenue_per_month['price'].tolist()
    year_months = total_revenue_per_month['year_month'].tolist()

    # Preparar la respuesta en el formato solicitado
    response_data = {
        "profit": profit,
        "year_months": year_months
    }
    
    return response_data 

def profitCategorySales( data_json ):
    # Crea un DataFrame de Pandas desde el JSON
    df = pd.read_json(data_json)
    
    # Convertir la columna 'date' a tipo datetime
    df['date'] = pd.to_datetime(df['date'])    
    
    # Añadir una columna 'category' basada en el nombre del producto
    df['category'] = df['name'].apply(categorize_product)

    # Agrupar por 'category' y sumar las ganancias
    category_sales = df.groupby('category')['sub_total'].sum().reset_index()

    # Ordenar por ventas totales en orden descendente
    category_sales = category_sales.sort_values(by='sub_total', ascending=False)
    
    # Convertir el resultado a JSON
    # category_sales_json = category_sales.to_json(orient='records')

    result = {
        "profit": category_sales['sub_total'].tolist(),
        "categories": category_sales['category'].tolist()
    }
    # result_json = json.dumps(result, indent=4)
    
    return result


def categorize_product(name):
    name = name.lower()
    
    if 'aceite' in name:
        return 'Aceites y Líquidos'
    elif 'líquido' in name or 'refrigerante' in name or 'aditivo' in name:
        return 'Aceites y Líquidos'
    elif 'ambientador' in name or 'limpiador' in name or 'esponja' in name or 'paño' in name or 'cera' in name or 'raspador' in name or 'parasoles' in name or 'toallita' in name or 'bolsa de basura' in name:
        return 'Accesorios y Limpieza'
    elif 'herramienta' in name or 'kit' in name or 'manómetro' in name or 'sellador' in name or 'extintor' in name or 'triángulo de seguridad' in name or 'gato hidráulico' in name or 'cable de arranque' in name:
        return 'Herramientas y Seguridad'
    elif 'guante' in name or 'tapaboca' in name:
        return 'Protección Personal'
    elif 'batería' in name or 'cargador' in name or 'filtro' in name or 'fusible' in name or 'bombilla' in name or 'linterna' in name:
        return 'Baterías y Piezas de Repuesto'
    elif 'cubreasientos' in name or 'tapete' in name or 'portavasos' in name or 'cargador de teléfono' in name or 'limpiador multiusos' in name:
        return 'Accesorios del Interior'
    elif 'cadena' in name:
        return 'Accesorios para Clima'
    else:
        return 'Otros'