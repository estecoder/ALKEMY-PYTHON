# ALKEMY-PYTHON

`python@3.8` `postgresql@12.11` `SQLAlchemy@1.4` `pandas@1.4` `requests@2.28`

## Descripcion:

Este es un modulo sencillo que interactua con la API [CKAN](http://docs.ckan.org/en/latest/api/) obteniendo datos de [datos.gob.ar](https://datos.gob.ar/dataset)
procesando esta información y escribiendola en una base de datos relacional (PostgreSQL).

>Datasets Procesados:
> * Bibliotecas Populares<br>
> * Museo<br>
> * Salas de cine<br>
### Inicializar Proyecto

<br>

* Inicialice el entorno virtual. Posterior a esto instale los modulos necesarios para la ejecución.<br>

```bash
python -m venv env
pip install -r requirements.txt

```
<br>

* Ingrese al archivo [.env](./.env). y configure las variables correspondientes para la conexion a la base de datos.<br>

  ```diff
  + DB_HOST = localhost
  - DB_HOST =
  + DB_USER = postgres
  - DB_USER =
  + DB_PASSWORD = my_password
  - DB_PASSWORD = 
  + DB_DATABASE = alkemydb
  - DB_DATABASE = 
  + DB_PORT = 5432
  - DB_PORT = 
  ```
 <br>
 
* Verifique que el servidor de la base de datos ya haya sido iniciado. Es importante iniciar el servidor para poder realizar las operaciones con las tablas correspondientes.

```bash
#install postgres
brew install postgresql@12
#run postgres server on macOS
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
```
* Ejecuten en consola con el interprete de python.

```bash
python main.py
```

