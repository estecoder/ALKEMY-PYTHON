import psycopg2 as pg

class Postgres:
    settings = {}

    def __init__(self):
        self.DB_HOST = "localhost"
        self.DB_USER = "postgres"
        self.DB_PASSWORD = "toorpass"
        self.DB_DATABASE = "alkemydb"
        self.DB_PORT = "5432"


    def connection(self):
        con = pg.connect(
            host = self.DB_HOST,
            user = self.DB_USER,
            password = self.DB_PASSWORD,
            database = self.DB_DATABASE,
            port = self.DB_PORT
        )
        return con
    


