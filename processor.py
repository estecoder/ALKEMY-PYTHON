
import pprint as p

import pandas as pd
from typing import List, Dict
import time
# from config import Postgres as psql

class Processor:
    def __init__(self, path_file: str=None):
        self._path = path_file
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
        self.get_data_csv()
        self._normalize_columns()
        self._fill_final_table()

    def set_path_file(self, path_file: str):
        self._path=path_file
    
    def get_path_file(self):
        return self._path
    
    def get_data_csv(self):
        self.down_data = pd.read_csv(self._path)
        self._normalize_columns()
        return self.down_data
    
    def get_alt_columns(self):
        return self.alt_columns
    
    def set_alt_columns(self, llave: str, lista: List[str]):
        self.alt_columns[llave] += lista

    def get_final_data(self):
        self._run_()
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
        self.process = {'in':{}, 'no_in':{}}
        vals = []
        for h in list(self.alt_columns.values()):
            vals += h
        
        for i in self.down_data.columns:
            if i in self.tf.columns or i in vals:
                self.process['in'][i]=cont
            else:
                self.process['no_in'][i]=cont
            cont += 1 

    def _fill_final_table(self):
        self._filter_columns()
        cont = 0
        for i in self.tf.columns:
            try:
                src_key = self._find_keys(self.process['in'],cont)
                altkey = self._find_right_column(src_key)    
                if (self.tf[i].dropna().empty and altkey==i):                     
                    self.tf[i]=self.down_data[src_key]
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
                        if (self.down_data[or_key].dropna().empty):
                            break
                    x_cont += 1
            finally:
                cont +=1
        now = time.strftime("%Y-%m-%d %H:%M")
        now = pd.to_datetime(now)
        self.tf['fecha_in'] = self.tf['fecha_in'].replace(pd.np.nan,now)
        self.tf = self.tf.replace("s/d",pd.np.nan)
        self.filtered_column = self.process

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



    