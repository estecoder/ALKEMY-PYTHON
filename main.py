import os
import pandas as pd
import logging as lg
from sqlalchemy import text

from data import Data
from processor import Processor
from config import Postgres 
from tables import MainData

lg.basicConfig(filename='main.logs', filemode='w', level=lg.DEBUG )

def print_options(options):
    while True:
        for i in range(0,len(options)):
            print(f"{i+1}. {options[i]}")

        in_name = int(input(f"\n\nIngrese una opcion valida de la lista: [ingrese 0 para salir]"))
        if in_name <= len(options) and in_name > 0:
            sel = options[in_name-1]
            break
        elif in_name==0:
            break
    return sel

def solve_challenge(name_data):
    req = Data()
    save = Processor()    
    req.make_request()
    options = req.get_options()
    #sel = print_options(options)
    req.set_name(name_data) 
    req.get_specific_data()
    path = req.get_dir()
    save.set_path_file(path)
    csv_data = save.get_data_csv()
    final_data = save.get_final_data()
    return [final_data, csv_data]


if __name__=='__main__':
    try:
        sql = Postgres()
        sql.connection()
        
        bp = solve_challenge("Bibliotecas Populares")
        museo = solve_challenge("Museo")
        cines = solve_challenge("Salas de Cine")


        tabla_final = pd.concat([bp[0],museo[0],cines[0]],axis=0).reset_index(drop=True)
        con = sql.get_connector()
        tabla_final.to_sql('data_principal',con,if_exists='replace')
        res = MainData.is_empty(con)

        if (MainData.is_empty(con)):
            tabla_final.to_sql('data_principal',con,if_exists='replace')
        else:
            MainData.truncate(con)
            tabla_final.to_sql('data_principal',con,if_exists='replace')

        sel = con.execute(text("\
                                SELECT categoria, COUNT(*) as total, (SELECT now() as fecha) FROM\
                                public.data_principal\
                                GROUP BY categoria;\
                                "))
        
        totales = pd.DataFrame(sel.fetchall())
        totales.to_sql('totales',con,if_exists='replace')
        
        col_cines = [cines[1]['Pantallas'],cines[1]['Butacas'],cines[1]['espacio_INCAA']]
        data_cines = pd.DataFrame(col_cines)
        data_cines = data_cines.transpose()
        data_cines = data_cines.assign(fecha_in=cines[0]['fecha_in'])
        data_cines.to_sql('cines',con,if_exists='replace')
        print(data_cines)
    except Exception or Warning as e:
        lg.warning(f"{e}")

    
    

    

    

    
