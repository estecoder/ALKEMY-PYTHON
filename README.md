# ALKEMY-PYTHON

`python@3.8` `postgresql@12.11` `SQLAlchemy@1.4` `pandas@1.4` `requests@2.28`

## Descripcion:

* Este es un modulo sencillo que interactua con la API [CKAN](http://docs.ckan.org/en/latest/api/) - [datos.gob.ar](https://datos.gob.ar/dataset)


### Inicializar Proyecto

<br>

* [ ] Inicialice el entorno virtual. Posterior a esto instale los modulos necesarios para la ejecución.<br>

```bash
python -m venv env
pip install -r requirements.txt

```
<br>

* [ ] Ingrese al archivo [.env](./.env). y configure las variables correspondientes para la conexion a la base de datos.<br>

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
 
* [ ] Verifique que el servidor de la base de datos ya haya sido iniciado. Es importante iniciar el servidor para poder realizar las operaciones con las tablas correspondientes.






