from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer,text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

class Postgres:
    settings = {}

    def __init__(self):
        self.DB_HOST = "localhost"
        self.DB_USER = "alkemy"
        self.DB_PASSWORD = "toorpass"
        self.DB_DATABASE = "alkemy2"
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
        self.base = declarative_base()
        Session = sessionmaker(self.db)  
        self.session = Session()
    
    # def gcon(self):
    #     print(self.str_link)
    
    def run_sql_file(self):
        # Open the .sql file
        sql_file = open('file.sql','r')

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



