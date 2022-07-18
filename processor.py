import pprint as p
import pandas as pd
from typing import List, Dict
# from config import Postgres as psql

class Processor:
    def __init__(self, path_file: str=None):
        self._path = path_file
        self.down_data = None
        self.filtered_column = None
        self.alt_columns = ['cp', 'cod_loc', 'idprovincia', 'iddepartamento','direccion']
        
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
    
    def set_alt_columns(self, lista: List[str]):
        self.alt_columns+lista

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

    def _fill_final_table(self):
        cont = 0
        process = {'in':{}, 'no_in':{}}
        for i in self.down_data.columns:
            if i in self.tf.columns or i in self.alt_columns:
                process['in'][i]=cont
            else:
                process['no_in'][i]=cont
            cont += 1 

        cont = 0
        for i in self.tf.columns:
            try:
                self.tf[i]=self.down_data[self._find_keys(process['in'],cont)]
            except Exception as e:
                x_cont = cont
                process_val = list(process['in'].values())
                if (self.tf[i].isnull):
                    while (True):
                        x_cont += 1
                        if x_cont in process_val:
                            a = self._find_keys(process['in'],x_cont)
                            self.tf[i]=self.down_data[a]
                            break
            finally:
        
                cont +=1
        self.filtered_column = process

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

    #B#Cod_Loc,IdProvincia,IdDepartamento,Observacion,Categoría, Subcategoria,Provincia, Departamento,Localidad,Nombre,Domicilio,Piso,CP,Cod_tel,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud,Fuente,Tipo_gestion,año_inicio,Año_actualizacion
    #M#Cod_Loc,IdProvincia,IdDepartamento,Observaciones,categoria, subcategoria,provincia,localidad,nombre,direccion,piso,CP,cod_area,telefono,Mail,Web,Latitud,Longitud,TipoLatitudLongitud,Info_adicional,fuente,jurisdiccion,año_inauguracion,actualizacion
    #C#Cod_Loc,IdProvincia,IdDepartamento,Observaciones,Categoría, Provincia, Departamento,Localidad,Nombre,Dirección,Piso,CP,cod_area,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud,Fuente,tipo_gestion,Pantallas,Butacas,espacio_INCAA,año_actualizacion

    #cine no tiene: subcategoria NULL
    # museo no tiene: departamento NULL
    #B domicilio es direccion


    