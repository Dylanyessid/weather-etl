def transform_weather_data(city_data):
    daily = city_data["daily"]
    
    dates = daily["time"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    precipitations = daily["precipitation_sum"]

     
    weather_records = []
    for date, tmax, tmin, precip in zip(dates, max_temps, min_temps, precipitations):
        record = {
            "date": date,
            "temp_max": tmax,
            "temp_min": tmin,
            "precipitation": precip,
            "thermal_range": tmax - tmin,
            "is_rainy": precip > 0
        }
        weather_records.append(record)
    
    return weather_records

