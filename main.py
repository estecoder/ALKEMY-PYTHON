import config as db_con
import data as d
import os, csv
import pprint as p



        

if __name__=='__main__':
    # name_dataset1 = input("Ingrese el nombre del dataset1: ")
    #name_dataset2 = input("Ingrese el nombre del dataset2: ")
    #name_dataset3 = input("Ingrese el nombre del dataset3: ")
    name_dataset1 = "bibliotecas populares"
    dataset1 = d.Data(name_dataset1)
    bp = dataset1.make_request()
    

    
    # print(museos)
    
    # h = ["col1","col2"]
    # l = [["col1","col2"],[11,22],[21,22]]
    # print(list_to_dict(l,h))
    
    
    
    # connector = db_con.Postgres()
    # con = connector.connection()
    