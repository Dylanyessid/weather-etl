from airflow.decorators import dag, task
from datetime import datetime
import sys
import os

sys.path.append((os.path.dirname(__file__)))

from etl.extract import extract_from_api
from etl.transform import transform_weather_data
from etl.load import get_connection, load_cities, get_city_ids, load_weather

CITIES = {
    "Medellín": (6.24, -75.58),
    "Bogotá": (4.71, -74.07),
    "Cali": (3.45, -76.53),
}

@dag(
    schedule="@daily",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["clima"]
)
def weather_etl():

    @task
    def load_cities_task():
        conn = get_connection()
        load_cities(CITIES, conn)
        conn.close()

    @task
    def proccess_city_task(city_name: str, coords: tuple):
        city_data = extract_from_api(coords[0], coords[1])
        weather_records = transform_weather_data(city_data)
        
        conn = get_connection()
        city_ids = get_city_ids(conn)
        city_id = city_ids[city_name]
        load_weather(weather_records, city_id, conn)
        conn.close()

    loaded_cities = load_cities_task()
    
    for city_name, coords in CITIES.items():
        process_city = proccess_city_task(city_name, coords)
        loaded_cities >> process_city

weather_etl()