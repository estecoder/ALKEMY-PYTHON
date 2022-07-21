from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer,text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "toorpass"
DB_DATABASE = "alkemydb"
DB_PORT = "5432"
link =""\
    +f"postgresql://{DB_USER}:"\
    +f"{DB_PASSWORD}@{DB_HOST}:"\
    +f"{DB_PORT}/{DB_DATABASE}"

file = "/Users/sergioboada/PROYECTOS/ALKEMY-PYTHON/db_architecture.sql"

db = create_engine(link)  
base = declarative_base()
Session = sessionmaker(db)  
session = Session()


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
                    input(f'{sql_command}')
                    session.execute(text(sql_command))
                    session.commit()

                # Assert in case of error
                except:
                    print('Ops')

                # Finally, clear command string
                finally:
                    sql_command = ''



os.system(f"psql -f {file} postgres")

base.metadata.create_all(db)

class Prueba(base):  
    __tablename__ = 'prueba'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)



sergio = Prueba(nombre="luz", apellido="boada")
session.add(sergio)
session.commit()

# Read
users = session.query(Prueba)  
for user in users:  
    print(user.nombre)

# # Create 
# doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")  
# session.add(doctor_strange)  
# session.commit()

# # Read
# films = session.query(Film)  
# for film in films:  
#     print(film.title)

# # Update
# doctor_strange.title = "Some2016Film"  
# session.commit()

# # Delete
# session.delete(doctor_strange)  
# session.commit()  
