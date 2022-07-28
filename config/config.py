from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer,text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from config.base import base as base_in
import logging as lg
from decouple import config

class Postgres:
    """
    NOMBRE: Postgres
    ===========================================================================
    DESCRIPCION
        Clase que implementa la conexion a traves de SQLAlchemy. con valores
        configurados en el archivo .env de manera local.
    """
    def __init__(self):
        
        self.base = base_in
        self.DB_HOST = config('DB_HOST')
        self.DB_USER = config('DB_USER')
        self.DB_PASSWORD = config('DB_PASSWORD')
        self.DB_DATABASE = config('DB_DATABASE')
        self.DB_PORT = config('DB_PORT')
        self.db = None
        self.session = None


    def set_host(self, host: str):
        self.DB_HOST = host

    def set_user(self, user: str):
        self.DB_USER = user
    def set_password(self, password: str):
        self.DB_PASSWORD = password

    def set_database(self, dataBase: str):
        self.DB_DATABASE = dataBase

    def set_port(self, port: str):
        self.DB_PORT = port  

    def get_host(self):
        return self.DB_HOST

    def get_user(self):
        return self.DB_USER

    def get_password(self):
        return self.DB_PASSWORD

    def get_database(self):
        return self.DB_DATABASE

    def set_port(self):
        return self.DB_PORT
    
    def get_connector(self):
        return self.db
    
    def get_session(self):
        return self.session

    def connection(self):
        """
        NOMBRE: 
            Data.connection

        DESCRIPCION:
            Inicia la conexion.
        """

        if  self.DB_HOST == None\
            or self.DB_USER == None\
            or self.DB_PASSWORD == None\
            or self.DB_DATABASE == None\
            or self.DB_PORT == None:
            lg.critical(f"host:{self.DB_HOST}\nuser:{self.DB_USER}\n\
                password:{self.DB_PASSWORD}\ndatabase:{self.DB_DATABASE}\n\
                port:{self.DB_PORT}\n variables de configuracion son None")
        self.link =""\
            +f"postgresql+psycopg2://{self.DB_USER}:"\
            +f"{self.DB_PASSWORD}@{self.DB_HOST}:"\
            +f"{self.DB_PORT}/{self.DB_DATABASE}"
        
        try:
            self.db = create_engine(self.link)  
            self.base.metadata.create_all(self.db)
            Session = sessionmaker(self.db)  
            self.session = Session()
            data_con = f"\thost:{self.DB_HOST}\n\tuser:{self.DB_USER}\n"
            data_con += f"\tpassword:{self.DB_PASSWORD}\n\tdatabase:{self.DB_DATABASE}\n"
            data_con += f"\tport:{self.DB_PORT}"
            lg.info(f"\nConexion a base de datos exitosa.\nDatos de conexion:\n{data_con}")
        except Exception as e:
            lg.fatal(f"Error en la conexion a la base de datos.\n{e}")


