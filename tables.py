# from sqlalchemy import Column, String, Integer, DateTime, func, text
from requests import session
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from base import base



class MainData(base):  
    __tablename__ = 'data_principal'
    
    index = Column(Integer, primary_key=True)
    cod_localidad = Column(Integer, default=None)
    id_provincia = Column(Integer, default=None)
    id_departamento = Column(Integer, default=None)
    categoria = Column(String, default=None)
    provincia = Column(String, default=None)
    localidad = Column(String, default=None)
    nombre = Column(String, default=None)
    domicilio = Column(String, default=None)
    codigo_postal = Column(String, default=None)
    telefono = Column(String, default=None)
    mail = Column(String, default=None)
    web = Column(String, default=None)
    fecha_in = Column(DateTime, default=func.now())
    
    
    def truncate(conex):
        conex.execute(text("TRUNCATE TABLE public.data_principal;"))
    
    def is_empty(conex):
        data = conex.execute(text("SELECT * FROM public.data_principal"))
        data = data.fetchall()
        if not data :
            return true
        else:
            return false

    def count_totales(conex):
        data = conex.execute(text("\
                            SELECT categoria, COUNT(*) as total, (SELECT now() as fecha) FROM\
                            public.data_principal\
                            GROUP BY categoria;\
                            "))
        data = data.fetchall()
        data = list(map(list,data))
        return data

class Totales (base):
    __tablename__= 'totales'

    index = Column(Integer, primary_key=True)
    categoria = Column(String, default=None)
    total = Column(Integer, default=None)
    fecha = Column(DateTime, default=func.now())

    
class Cines(base):
    __tablename__ = 'cines'

    index = Column(Integer, primary_key=True) 
    provincia = Column(String, default=None)
    pantallas = Column(Integer, default=None) 
    butacas = Column(Integer, default=None) 
    espacios_INCAA = Column(String, default=None)

        
