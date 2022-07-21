from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer,text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from base import base as base_in

class Postgres:
    def __init__(self):
        self.base = base_in
        self.DB_HOST = "localhost"
        self.DB_USER = "alkemy"
        self.DB_PASSWORD = "toorpass"
        self.DB_DATABASE = "alkemydb"
        self.DB_PORT = "5432"
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

    def  get_base_obj(self):
        return self.base

    def connection(self):
        if  self.DB_HOST == None\
            or self.DB_USER == None\
            or self.DB_PASSWORD == None\
            or self.DB_DATABASE == None\
            or self.DB_PORT == None:
            raise Exception("Verifique variables de configuracion")
        self.link =""\
            +f"postgresql+psycopg2://{self.DB_USER}:"\
            +f"{self.DB_PASSWORD}@{self.DB_HOST}:"\
            +f"{self.DB_PORT}/{self.DB_DATABASE}"
        self.db = create_engine(self.link)  
        self.base.metadata.create_all(self.db)
        Session = sessionmaker(self.db)  
        self.session = Session()
