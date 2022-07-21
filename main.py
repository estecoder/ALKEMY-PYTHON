
import pprint as p
import os
import pandas as pd

from data import Data
from processor import Processor

from config import Postgres 
from tables import MainData

if __name__=='__main__':
    name_data1 = "Bibliotecas Populares"
    name_data2 = "Museo"
    name_data3 = "Salas de Cine"
    
    req_bp = Data()
    req_museo = Data()
    req_cines = Data()
    save = Processor()
    sql = Postgres()
    sql.connection()
    
    req_bp.set_name(name_data1) 
    req_bp.make_request()
    path = req_bp.get_dir()
    input(save.set_path_file(path))
    bp = save.get_final_data()

    req_museo.set_name(name_data2) 
    req_museo.make_request()
    path = req_museo.get_dir()
    save.set_path_file(path)
    input(save.get_path_file())
    museo = save.get_final_data()
    
    req_cines.set_name(name_data3) 
    req_cines.make_request()
    path = req_cines.get_dir()
    input(save.set_path_file(path))
    cines = save.get_final_data()

    input(f"{bp}\n\n{museo}\n\n{cines}")
    
    # tab_final = pd.concat([bp,museo,cines],axis=0)
    # con = sql.get_connector()
    # tab_final.to_sql('data_principal',con,if_exists='replace')

    

    

    
