# Clima ETL DAG

Este DAG de Airflow orquesta una ETL (Extract → Transform → Load) diaria para obtener datos meteorológicos de varias ciudades y almacenarlos en una base de datos.

**Resumen**
- **Nombre del DAG:** `clima_etl`
- **Horario:** `@daily` (ejecuta diariamente)


**Flujo de trabajo**
- **Carga de ciudades:** tarea `cargar_ciudades` — inserta las ciudades definidas en el diccionario `CITIES` en la base de datos.
- **Procesamiento por ciudad:** tarea `procesar_ciudad(city_name, coords)` — para cada ciudad realiza:
  1. `extract_from_api(lat, lon)` — extrae datos meteorológicos desde la API.
  2. `transform_weather_data(...)` — transforma/normaliza los datos para el modelo de persistencia.
  3. `load_weather(records, city_id, conn)` — guarda los registros en la BD usando `get_connection()` y `get_city_ids()`.

**Estructura del proyecto**
- Archivo principal del DAG: [clima_dag.py](clima_dag.py)
- Módulos ETL: la carpeta `etl/` contiene `extract.py`, `transform.py`, y `load.py`.

**Configuración y dependencias**
- El DAG usa funciones en `etl/` para manejar la API y la base de datos; asegúrate de que las credenciales y la cadena de conexión estén configuradas donde `get_connection()` las espera (por ejemplo variables de entorno o un archivo de configuración en `etl/config.py`).
- Instala dependencias necesarias para las llamadas a la API y el acceso a la base de datos (requests, driver DB correspondiente, etc.).

**Cómo ejecutar**
- Desplegar la carpeta en el directorio de `dags` de Airflow (ya está en `/dags/weather-etl`).
- Desde la interfaz web de Airflow: activar el DAG `clima_etl` y disparar manualmente.
- Desde la CLI: `airflow dags trigger clima_etl`

**Notas rápidas**
- El diccionario `CITIES` (en [clima_dag.py](clima_dag.py)) contiene las ciudades y coordenadas que se procesan. Cambiarlo añade/quita ciudades del flujo.
- Cada ejecución abre y cierra conexiones a la base de datos por tarea para evitar conexiones persistentes.

