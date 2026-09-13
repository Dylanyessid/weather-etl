import psycopg2
from psycopg2.extras import execute_values
from airflow.hooks.base import BaseHook
#from etl.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT , DB_USER

def get_connection():
    conn = BaseHook.get_connection("weather_etl_db")
    return psycopg2.connect(
        host=conn.host,
        port=conn.port,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password
    )

def load_cities(cities_dict, conn):
    cur = conn.cursor()
    
    data = [(name, lat, lon) for name, (lat, lon) in cities_dict.items()]
    
    execute_values(cur, """
        INSERT INTO cities (name, latitude, longitude)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """, data)
    
    conn.commit()
    cur.close()


def load_weather(weather_records, city_id, conn):
    cur = conn.cursor()
    data = [
        (city_id, r["date"], r["temp_max"], r["temp_min"], r["precipitation"], r["thermal_range"], r["is_rainy"])
        for r in weather_records
    ]

    execute_values(cur, """
        INSERT INTO weather_daily (city_id, date, temp_max, temp_min, precipitation, thermal_range, is_rainy)
        VALUES %s
        ON CONFLICT (city_id, date) DO NOTHING
    """, data)
    
    conn.commit()
    cur.close()

def get_city_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM cities")
    rows = cur.fetchall()
    cur.close()
    
    return {name: id for id, name in rows}