import requests
import click

def realtime_weather(city: str) -> dict:
    api_key = "28bccbad55ce43c293f05737251509"  # replace with your own key
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"  # optional: include air quality data
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # WeatherAPI returns {"error": {...}} if something went wrong
        if "error" in data:
            return {"error": data["error"]["message"]}
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@click.command()
@click.option('--city', prompt='City name', help='Name of the city to get weather information for.')
def get_weather(city):
    """Fetch and display real-time weather information for a specified city using WeatherAPI.com."""
    weather_data = realtime_weather(city)
    
    if "error" in weather_data:
        print(f"Error fetching weather data: {weather_data['error']}")
        return

    location = weather_data["location"]["name"]
    country = weather_data["location"]["country"]
    temp = weather_data["current"]["temp_c"]
    humidity = weather_data["current"]["humidity"]
    wind_speed = weather_data["current"]["wind_kph"]
    weather_desc = weather_data["current"]["condition"]["text"]

    print(f"Weather in {location}, {country}:")
    print(f"Description: {weather_desc}")
    print(f"Temperature: {temp}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} kph")

if __name__ == "__main__":
    get_weather()
