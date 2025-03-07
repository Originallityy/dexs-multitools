import requests
import sys
import os
import json
from datetime import datetime

# wttr.in service URL - doesn't require an API key
WTTR_URL = "https://wttr.in/"

def get_weather(location, format_type="j1"):
    """
    Get weather data from wttr.in service
    format_type options:
    - j1: JSON format with current weather only
    - j2: JSON format with current + forecast
    - '': Text format (ASCII art)
    """
    url = f"{WTTR_URL}{location}"
    
    # Add format parameter if specified
    if format_type:
        url = f"{url}?format={format_type}"
    
    headers = {
        'User-Agent': 'curl/7.68.0'  # Pretend to be curl to get full response
    }
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if format_type.startswith('j'):
            # Parse the JSON response
            return response.json()
        else:
            # Return the text response
            return response.text
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: Location '{location}' not found.")
        else:
            print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("Error: Connection failed. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while making the request: {e}")
    except json.JSONDecodeError:
        print(f"Error: Could not parse weather data for '{location}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

def display_weather_ascii(location):
    """Display weather in ASCII art format"""
    print(f"\n===== Weather for {location} =====\n")
    
    # Get weather in ASCII art format
    weather_art = get_weather(location, format_type="")
    if weather_art:
        print(weather_art)

def display_weather_data(weather_data, location):
    """Display weather in data format"""
    if not weather_data:
        return
    
    try:
        # Extract current weather info
        current = weather_data.get('current_condition', [{}])[0]
        
        temp_c = current.get('temp_C', 'N/A')
        temp_f = current.get('temp_F', 'N/A')
        feels_like_c = current.get('FeelsLikeC', 'N/A')
        feels_like_f = current.get('FeelsLikeF', 'N/A')
        humidity = current.get('humidity', 'N/A')
        description = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
        wind_speed = current.get('windspeedKmph', 'N/A')
        wind_dir = current.get('winddir16Point', 'N/A')
        visibility = current.get('visibility', 'N/A')
        pressure = current.get('pressure', 'N/A')
        
        print(f"\n===== Current Weather for {location} =====")
        print(f"Temperature: {temp_c}°C / {temp_f}°F")
        print(f"Feels like: {feels_like_c}°C / {feels_like_f}°F")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_speed} km/h, Direction: {wind_dir}")
        print(f"Visibility: {visibility} km")
        print(f"Pressure: {pressure} hPa")
        print(f"Conditions: {description}")
        print("="*50)
        
        # Display forecast if available
        if 'weather' in weather_data:
            print("\n===== 3-Day Forecast =====")
            for day in weather_data['weather'][:3]:
                date = day.get('date', 'N/A')
                max_temp_c = day.get('maxtempC', 'N/A')
                min_temp_c = day.get('mintempC', 'N/A')
                max_temp_f = day.get('maxtempF', 'N/A')
                min_temp_f = day.get('mintempF', 'N/A')
                desc = day.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', 'N/A')
                
                print(f"{date}: {min_temp_c}-{max_temp_c}°C / {min_temp_f}-{max_temp_f}°F - {desc}")
            
            print("="*50)
            
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")

def main():
    # Get location from command line arguments or prompt the user
    if len(sys.argv) > 1:
        location = ' '.join(sys.argv[1:])
    else:
        location = input("Enter location (City, State/Country): ")
    
    # Ask for display preference
    display_type = "data"  # Default to data display
    
    # Get and display weather according to preference
    if display_type == "ascii":
        display_weather_ascii(location)
    else:
        # Get weather data in JSON format
        weather_data = get_weather(location, format_type="j2")
        if weather_data:
            display_weather_data(weather_data, location)

if __name__ == "__main__":
    main()
