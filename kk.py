from typing import List
import pandas as pd
from config import Postgres as pg

def limpiar_acentos(text: List[str]):
	acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
	for palabra in text:
		for acen in acentos:
			if acen in palabra:
				i = text.index(palabra)
				palabra = palabra.replace(acen, acentos[acen])
				text[i]=palabra
	return text
l = ["holá","no","tél"]
limpiar_acentos(l)
dt = pd.DataFrame({
	"A":[1,2,3,4],
	"B":[0,None,5,7],
	"C":[9,3,2,None]
})
obj = pg()
obj.connection()
con = obj.get_connector()
q = "SELECT * FROM \"public\".\"prueba\""
r = con.execute(q)
for line in r:  
    print(line)

dt.to_sql("python1",con, if_exists='replace')
q = "SELECT * FROM \"public\".\"python1\""
r = con.execute(q)
for line in r:  
    print(line)




