import requests
from datetime import date
from dateutil.relativedelta import relativedelta
def extract_from_api(latitude, longitude):
    today: date = date.today()
    start_date: date = today - relativedelta(months=1)
    
    response = requests.get(f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date.isoformat()}&end_date={today.isoformat()}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Bogota")

    if(response.status_code == 200):

        return response.json()

    return None
