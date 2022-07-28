
import pprint as p
import logging as lg
import pandas as pd
from typing import List, Dict
import time
# from config import Postgres as psql

class Processor:

    """
    NOMBRE:
        Processor
    DESCRIPCION:
        Procesa archivos csv con el fin de filtrar columnas innecesarias
        frente a una tabla final pre-establecida, realizando una comparacion 
        entre los posibles valores. Retorna objetos pandas.DataFrame
    METODOS:
        set_path_file - Asignar ruta de csv a procesar
        get_path_file - Retorna la ruta del csv a procesar
        get_data_csv - Retorna el csv sin modificaciones. Objeto tipo pandas.DataFrame
        get_alt_columns - Retorna relacion columnas finales opcion de columnas originales
        set_alt_columns - Asigna opciones alternativas a columna final especifica
        get_final_data - Retornar data filtrada. objeto pandas.DataFrame
        get_filter_column - Retorna las columnas aceptas y descartadas de la tabla fuente

    """
    def __init__(self, path_file: str=None):
        self._path = path_file
        self.check_run = False
        self.down_data = None
        self.filtered_column = None
        self.alt_columns = {'cod_localidad': ['cod_loc'],
                            'id_provincia':['idprovincia'],
                            'id_departamento':['iddepartamento'],
                            'categoria':[],
                            'provincia': [],
                            'localidad': [],
                            'nombre':[],
                            'domicilio': ['direccion'],
                            'codigo_postal': ['cp'],
                            'telefono':[],
                            'mail':[],
                            'web':[],
                            'fecha_in':[],
                            }
        
        self.tf = pd.DataFrame({
                                'cod_localidad': pd.Series(dtype='int64'),
                                'id_provincia': pd.Series(dtype='int64'),
                                'id_departamento': pd.Series(dtype='int64'),
                                'categoria': pd.Series(dtype='object'),
                                'provincia': pd.Series(dtype='object'),
                                'localidad': pd.Series(dtype='object'),
                                'nombre': pd.Series(dtype='object'),
                                'domicilio': pd.Series(dtype='object'),
                                'codigo_postal': pd.Series(dtype='int64'),
                                'telefono': pd.Series(dtype='object'),
                                'mail': pd.Series(dtype='object'),
                                'web': pd.Series(dtype='object'),
                                'fecha_in': pd.Series(dtype='object')
                                })
    
    def _run_(self):
        self.check_run = True
        self.get_data_csv()
        self._normalize_columns()
        self._filter_columns()


    def set_path_file(self, path_file: str):
        self._path=path_file

    
    def get_path_file(self):
        return self._path
    
    def get_data_csv(self):
        self.down_data = pd.read_csv(self._path)
        return self.down_data
    
    def get_alt_columns(self):
        return self.alt_columns
    
    def set_alt_columns(self, llave: str, lista: List[str]):
        self.alt_columns[llave] += lista

    def get_final_data(self):
        if not self.check_run:
            self._run_()
        self._fill_final_table()
        return self.tf

    def get_filter_column(self):
        self._run_()
        return self.filtered_column
    
    def _normalize_columns(self):
        self.down_data.columns = map(str.lower, self.down_data.columns)
        cols = self.down_data.columns.to_list()
        self.down_data.columns = self._limpiar_acentos(cols)

        

    def _find_right_column(self, src_key):
        for k in self.alt_columns:
            if src_key in self.alt_columns[k]:
                alt_key = k
                break
            elif len(self.alt_columns[k])==0 and src_key==k:
                alt_key = k
                break
            elif src_key==k:
                alt_key = k
                break
        return alt_key 
    
    def _filter_columns(self):
        cont = 0
        self.process = {'in':{}, 'out':{}}
        vals = []
        for h in list(self.alt_columns.values()):
            vals += h
        for i in self.down_data.columns:
            if i in self.tf.columns or i in vals:
                self.process['in'][i]=cont
            else:
                self.process['out'][i]=cont
            cont += 1 
        self.filtered_column = self.process
        lg.info(f"Columnas aceptadas:\n{self.filtered_column['in'].keys()}\n\
Columnas Rechazadas:{self.filtered_column['out'].keys()}")

    def _fill_final_table(self):
        cont = 0
        for i in self.tf.columns:
            try:
                if i == 'fecha_in':
                    now = time.strftime("%Y-%m-%d %H:%M")
                    now = pd.to_datetime(now)
                    try:
                        self.tf['fecha_in'] = self.tf['fecha_in'].replace(pd.np.nan,now)
                    except FutureWarning as w:
                        lg.info(f"{w}")
                src_key = self._find_keys(self.process['in'],cont)
                altkey = self._find_right_column(src_key)
                if (self.tf[i].dropna().empty and altkey==i):                     
                    self.tf[i]=self.down_data[src_key]
                    lg.info(f"Columna:{i} ha sido llenada")
                elif (self.tf[i].dropna().empty):
                    raise Exception(f"{i} is not filled")
                
            except Exception as e:
                x_cont = 0
                process_val = list(self.process['in'].values())
                while (self.tf[i].dropna().empty):
                    if x_cont in process_val:
                        or_key = self._find_keys(self.process['in'],x_cont)
                        alt_key = self._find_right_column(or_key)
                        if i == alt_key:
                            self.tf[i]=self.down_data[or_key]
                            lg.info(f"Columna:{i} ha sido llenada")
                        if (self.down_data[or_key].dropna().empty):
                            break
                    x_cont += 1
            finally:
                cont +=1
        try:
            self.tf = self.tf.replace("s/d",pd.np.nan)
        except FutureWarning as w:
            lg.info(f"Error futuro.\n{w}")
        

    def _find_keys(self, in_dict: dict, val: int):
        keys = list(in_dict.keys())
        values = list(in_dict.values())
        return keys[values.index(val)]
    
    def _limpiar_acentos(self, text: List[str]):
        acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
        for palabra in text:
            for acen in acentos:
                if acen in palabra:
                    i = text.index(palabra)
                    palabra = palabra.replace(acen, acentos[acen])
                    text[i]=palabra
        return text


    