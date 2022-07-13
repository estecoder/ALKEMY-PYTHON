from importlib.resources import path
from operator import or_
import requests, os, csv, pprint as p, time

class Data:
    def __init__(self, name_dataset: str):
        #Definicion de variables internas de la clase
        self.dataset: str = name_dataset
        self.all_data = None
        self.file_dir = None
        self.data_csv = None
        self.id_dataset = "cultura-mapa-cultural-espacios-culturales"
        self._url_request = "http://datos.gob.ar/api/3/action/package_show?id="+self.id_dataset
        #aplicando metodos necesarios
        self._create_dirs(self.dataset)
        
    #metodo disponible al usuario
    def make_request(self):
        
        r = requests.get(self._url_request)
        answer = r.json()
        datasets = answer['result']['resources']
        for i in datasets:
            if i['name'] == self.dataset.title():
                self.all_data = i
        self._donwload_csv()
        return self.data_csv
    
    #metodos privados de la clase
    def _donwload_csv(self):
        url_d = self.all_data['url']
        with requests.Session() as down_data:
            download = down_data.get(url_d)
            content = download.content.decode('utf-8')
            reader = csv.reader(content.splitlines(), delimiter=',')
            my_list = list(reader)
        headers = my_list.pop(0)
        self.data_csv = self._list_to_dict(my_list,headers) 
        self._w_csv(self.file_dir,self.data_csv)

    def _list_to_dict(self, lista: list, headers: list):
        if len(lista) > 1:
            medio = len(lista) // 2
            izquierda = lista[:medio]
            derecha = lista[medio:]
            
            # llamada recursiva en cada mitad
            self._list_to_dict(izquierda,headers)
            self._list_to_dict(derecha,headers)
            
            # Iteradores para recorrer las dos sublistas
            i = 0
            j = 0
            # Iterador para la lista principal
            k = 0

            while i < len(izquierda) and j < len(derecha):
                if type(izquierda[i])!=dict:
                    lista[k] = dict(zip(headers,izquierda[i]))
                    i += 1
                    k += 1
                elif type(derecha[j])!=dict:
                    lista[k] = dict(zip(headers,derecha[j]))
                    j += 1
                    k += 1
                else:
                    lista[k] = izquierda[i]
                    lista[k+1] = derecha[j]
                    i += 1
                    j += 1
                    k += 2
            #Escribe restante por izquierda cuando excede el index
            while i < len(izquierda):
                if type(izquierda[i])!=dict:
                    lista[k] = dict(zip(headers,izquierda[i]))
                    k +=1
                else:
                    lista[k] = izquierda[i]
                    k +=1
                i += 1
            #Escribe restante por derecha cuando excede el index    
            while j < len(derecha):
                if type(derecha[j])!=dict:
                    lista[k] = dict(zip(headers,derecha[j]))
                    k += 1
                else:
                    lista[k] = derecha[j]
                    k += 1
                j += 1
            
            return lista

    def _create_dirs(self,cat: str):
        date = time.strftime("%Y-%B-%d")
        directory = f"\"{cat}\"/{date.split('-')[0]}-{date.split('-')[1]}"
        file_name = f'{directory}/{cat.replace(" ","-")}-{"-".join(date.split("-")[::-1])}'
        os.system(f"mkdir -pv {directory}")
        os.system(f"touch {file_name}.csv")
        tmp_name = file_name.replace('\"','')
        self.file_dir = f'{tmp_name}.csv'

    def _w_csv (self,path_file: str, list_to_write: list):
        scheme_list = list(list_to_write[0].keys())
        tmp_file='{}.tmp'.format(path_file)
        with open(tmp_file, mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=scheme_list)
            writer.writerows(list_to_write)
            os.remove(path_file)
            os.rename(tmp_file,path_file)
            file.close()
        

    


#Redirecting you to https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d  
#Redirecting you to https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae 
#Redirecting you to https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7
'''
id_dataset = "cultura-mapa-cultural-espacios-culturales"
r = requests.get("http://datos.gob.ar/api/3/action/package_show?id="+id_dataset)
data = r.json()
print("#"*120)
refer = [
    "cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d",
    "cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae",
    "cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7" 
]
list_url = []
for i in data['result']['resources']:
    #print(i['url'])
    tmp_dict = {}
    if i['url'] not in list_url:
        if i['id'] in refer: 
            name = i["name"]
            tmp_dict ['package_id'] = i['package_id']
            tmp_dict ['id'] = i['id']
            tmp_dict [name] = i['url']
            list_url.append(tmp_dict)
pprint.pprint(list_url)

# print(dir(requests))
with requests.Session() as down_data:
    download = down_data.get(list_url[0]['Bibliotecas Populares'])
    content = download.content.decode('utf-8')
    reader = csv.reader(content.splitlines(), delimiter=',')
    my_list = list(reader)

print(my_list)

#d = requests.get(list_url['Bibliotecas Populares'])
#bp = d.json()
# 
'''
