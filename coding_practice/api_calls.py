import requests

def get_weather(lat, lon):
    # API Documentation: https://open-meteo.com/en/docs
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['current']['temperature_2m']
        unit = data['current_units']['temperature_2m']
        return f"The current temperature is {temp}{unit}."
    else:
        return "Error: Unable to fetch weather data."

# Demo call for Tokyo (35.67, 139.65)
print(get_weather(35.67, 139.65))

def get_country_info(name):
    # API Documentation: https://restcountries.com/
    url = f"https://restcountries.com/v3.1/name/{name}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()[0] # API returns a list, we want the first match
        common_name = data['name']['common']
        capital = data['capital'][0]
        population = data['population']
        region = data['region']
        latlng = data['capitalInfo']['latlng']
        
        return {
            "country": common_name,
            "capital": capital,
            "population": f"{population:,}",
            "continent": region,
            "latitude" : latlng[0],
            "longitude" : latlng[1],
        }
    else:
        return f"Error: Could not find information for '{name}'."

# Demo call for Brazil
print(get_country_info("Brazil"))

