import psycopg2 
from psycopg2 import DatabaseError
from dotenv import load_dotenv
import os

def get_connection():
    try:
        return psycopg2.connect(
            host = os.getenv('PGSQL_HOST'),
            port = os.getenv('PGSQL_PORT'),
            user = os.getenv('PGSQL_USER'),
            password = os.getenv('PGSQL_PASSWORD'),
            database = os.getenv('PGSQL_DATABASE')
        )
    except DatabaseError as ex:
        raise ex   