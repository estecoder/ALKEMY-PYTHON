
import pprint as p
import os
from data import Data
from processor import Processor



from sqlalchemy import create_engine
from sqlalchemy import Column, String, text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from config import Postgres

def run_sql_file():
    # Open the .sql file
    file = "/Users/sergioboada/PROYECTOS/ALKEMY-PYTHON/db_architecture.sql"
    sql_file = open(file,'r')

    # Create an empty command string
    sql_command = ''

    # Iterate over all lines in the sql file
    for line in sql_file:
        # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):
            # Append line to the command string
            sql_command += line.strip('\n')

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statement and commit it
                try:
                    session.execute(text(sql_command))
                    session.commit()

                # Assert in case of error
                except:
                    print('Ops')

                # Finally, clear command string
                finally:
                    sql_command = ''

if __name__=='__main__':
    name_data1 = "Bibliotecas Populares"
    name_data2 = "Museo"
    name_data3 = "Salas de Cine"
    
    req_api = Data()
    save = Processor()
    
    req_api.set_name(name_data1) 
    # req_api.make_request()

    
    
    
    # tmp = "/Users/sergioboada/PROYECTOS/ALKEMY-PYTHON/Bibliotecas Populares/2022-July/bibliotecas-populares-15-July-2022.csv"
    # req_api.set_dir(tmp)
    path = req_api.get_dir()
    save.set_path_file(path)

    # print(dir(pg))

    ###############################################################################################

    
    
