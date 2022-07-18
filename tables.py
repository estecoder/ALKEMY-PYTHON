from email.policy import default
from sqlalchemy import Column, String, Integer, DateTime, func, text

class MainData(base):  
    __tablename__ = 'data_principal'
    
    id = Column(Integer, primary_key=True)
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
    

