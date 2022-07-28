import logging as lg
import requests, os, csv, time
    
class Data:
    """
    NOMBRE: Data

    DESCRIPCION:
        Data - Consumo de API: CKAN
        ==============================================================================
        Esta clase te permite hacer el consumo de la API: CKAN.
            link    - http://datos.gob.ar/api
            package - cultura-mapa-cultural-espacios-culturales
        
        De manera interna escribe los archivos .csv correspondientes
        a cada conjunto de datos dentro de la estructura del proyecto.

        PRINCIPALES CARACTERISTICAS:
        ------------------------------------------------------------------------------
            - Solicitud (request) a API CKAN.
            - Creacion de estructura para manejo de archivos fuente.
            - Conversion automatica: lista de listas -> lista de diccionarios.
            - Descarga y escritura de archivos .csv.
        
    METODOS:
        set_name        - Ingresar el nombre del conjunto de datos.
        get_dir         - Obtener la direccion del archivo csv creado.
        make_request    - Hacer solicitud a API: CKAN.
        _donwload_csv   - (privado) Descarga de archivo .csv desde el link origen.
        _list_to_dict   - (privado) Convertir lista de listas a lista de diccionarios.
        _create_dirs    - (privado) Constructor de arquitectura de archivos.
        _w_csv          - (privado) Guardar lista de diccionarios a .csv en storage.
    """    """"""    
    def __init__(self, name_dataset: str=None):
        #Definicion de variables internas de la clase
        self._dataset: str = name_dataset
        self.answer = None
        self.names = None
        self.__all_data = None
        self.file_dir = None
        self.data_csv = None
        self.id_dataset = "cultura-mapa-cultural-espacios-culturales"
        self._url_request = "http://datos.gob.ar/api/3/action/package_show?id="+self.id_dataset
        #aplicando metodos necesarios
        
    
    def set_name(self, name_dataset: str):
        self._dataset = name_dataset
    
    def get_name(self):
        return self.file_dir

    def set_dir(self, path_file: str):
        self.file_dir = path_file

    def get_dir(self):
        return self.file_dir

    #metodo disponible al usuario
    def make_request(self):
        """
        NOMBRE:
            Metodo - make_request()
        
        DESCRIPCION:
            Hace solicitud a API obteniendo un paquete de datos contenedor de
            las direcciones para la descarga de archivos fuente .csv.

        """
        try:
            r = requests.get(self._url_request)
            answer = r.json()
            self.source_data = answer['result']['resources']
            lg.info("Request a API exitoso.")
        except Exception as e:
            lg.critical(f"Error en request a API.\n{e}")

        
    
    def get_options(self):
        self.names = []
        for info in self.source_data:
            self.names.append(info['name'])
        return self.names 
    
    def get_specific_data(self):
        if self._dataset != None:
            if self._dataset in self.names:
                for i in self.source_data:
                    if i['name'] == self._dataset:
                        self.__all_data = i
                self._create_dirs(self._dataset.lower())
                self._donwload_csv()
            else:
                lg.warning(f"{self._dataset} no se encuentra en:\n{self.names}") 
        else:
            lg.warning(f"Dataset name is {self._dataset}")
    
    #metodos privados de la clase
    def _donwload_csv(self):
        """
        NOMBRE:
            Metodo - _download_csv
        
        DESCRIPCION:
            Metodo interno para la descarga de datos que proviene de un .csv
        """        """"""
        
        try:
            url_d = self.__all_data['url']
            with requests.Session() as down_data:
                download = down_data.get(url_d)
                content = download.content.decode('utf-8')
                reader = csv.reader(content.splitlines(), delimiter=',')
                my_list = list(reader)
            headers = my_list[0]
            self.data_csv = self._list_to_dict(my_list,headers) 
            self._w_csv(self.file_dir,self.data_csv)
        except Exception as e:
            lg.critical(f"\n\
                {url_d} no pudo ser descargado. Verifique si el request fue exitoso.\n Error: {e}")

    def _list_to_dict(self, lista: list, headers: list):
        """
        NOMBRE:
         metodo - _list_to_dict
        
        DESCRIPCION:
            Convierte una lista de listas a una lista de diccionarios aplicando recursividad.

        ARGUMENTOS:
            lista (list): Lista a escribir con la data que correponderá a los values de los diccionarios.
            headers (list): Cabeceras de columnas que corresponden a las keys de los diccionarios.

        Returns:
            lista (list): Retorna una lista de diccionarios.
        """
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
        """
        NAME: 
            Metodo - _create_dirs
        
        DESCRIPCION:
            Crea estructura de archivos, carpetas y csv vacios para sobre escribir con
            la informacion descargada.
        
        ARGUMENTOS: 
            cat (str): Titulo principal del dataset. Nombre principal de estructura de 
            directorios y archivos.
        """
        date = time.strftime("%Y-%B-%d")
        directory = f"\"{cat}\"/{date.split('-')[0]}-{date.split('-')[1]}"
        file_name = f'{directory}/{cat.replace(" ","-")}-{"-".join(date.split("-")[::-1])}'
        os.system(f"mkdir -pv {directory}")
        os.system(f"touch {file_name}.csv")
        tmp_name = file_name.replace('\"','')
        self.file_dir = f'{tmp_name}.csv'
    

    def _w_csv (self,path_file: str, list_to_write: list):
        """
        NAME:
            Metodo - _w_csv
        
        DESCRIPCION:
            Escribe datos csv desde un diccionario python.

        Args:
            path_file (str): Ruta del archivo en storage a escribir. 
                            (El archivo ya debe existir. Sobre escribe el archivo en su totalidad)
            list_to_write (list): Lista de diccionarios contenedora de la informacion a escribir.
        """
        scheme_list = list(list_to_write[0].keys())
        tmp_file='{}.tmp'.format(path_file)
        with open(tmp_file, mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=scheme_list)
            writer.writerows(list_to_write)
            os.remove(path_file)
            os.rename(tmp_file,path_file)
            file.close()