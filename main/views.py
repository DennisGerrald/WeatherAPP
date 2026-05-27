import hashlib
import time
import random
import requests
from django.shortcuts import render
from django.conf import settings
from .models import SearchHistory

API_KEY = getattr(settings, 'OPENWEATHER_API_KEY', 'your_api_key_here')

def get_mock_weather(city):
    """
    Generates realistic, deterministic weather data based on the city name hash
    and current time/date factors to enable out-of-the-box local testing.
    """
    city_clean = city.strip().title()
    h = int(hashlib.md5(city_clean.encode('utf-8')).hexdigest(), 16)
    
    # Deterministic base conditions based on city name hash
    conditions = [
        ("Clear", "Clear Sky", "01d", 25.0, 45, 1015, 3.2),
        ("Clouds", "Few Clouds", "02d", 20.0, 55, 1012, 4.1),
        ("Clouds", "Scattered Clouds", "03d", 18.0, 60, 1010, 5.5),
        ("Clouds", "Broken Clouds", "04d", 14.0, 75, 1008, 6.0),
        ("Rain", "Light Rain", "10d", 12.0, 85, 1005, 4.8),
        ("Rain", "Moderate Rain", "09d", 10.0, 90, 1002, 7.2),
        ("Thunderstorm", "Thunderstorm", "11d", 15.0, 95, 998, 9.5),
        ("Snow", "Light Snow", "13d", -1.0, 80, 1009, 3.5),
        ("Mist", "Mist", "50d", 8.0, 95, 1013, 2.0)
    ]
    
    cond_idx = h % len(conditions)
    main_cond, desc, icon, base_temp, humidity, pressure, wind_speed = conditions[cond_idx]
    
    # Diurnal temperature cycle: peak around 14:00, coolest around 05:00
    hour = time.localtime().tm_hour
    diurnal_offset = 5.0 * (1.0 - abs(hour - 14) / 12.0)
    temp = base_temp + diurnal_offset
    
    # Dynamic daily shift so weather changes slightly day to day
    day = time.localtime().tm_mday
    random.seed(h + day)
    temp += random.uniform(-2.0, 2.0)
    humidity = min(100, max(0, humidity + random.randint(-10, 10)))
    pressure += random.randint(-5, 5)
    wind_speed = round(max(0.5, wind_speed + random.uniform(-1.5, 1.5)), 1)
    
    countries = ["US", "GB", "JP", "FR", "DE", "CA", "AU", "BR", "IN", "ZA"]
    country = countries[h % len(countries)]
    
    return {
        'city': f"{city_clean}, {country}",
        'temperature': round(temp, 1),
        'humidity': humidity,
        'pressure': pressure,
        'description': desc,
        'icon': icon,
        'wind_speed': wind_speed,
        'is_mock': True
    }

def index(request):
    weather = None
    error = None
    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]

    if request.method == "POST":
        city = request.POST.get('city', '').strip()
        if city:
            use_simulation = (not API_KEY or API_KEY == "your_api_key_here")
            
            if use_simulation:
                weather = get_mock_weather(city)
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                try:
                    resp = requests.get(url, timeout=5)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        weather = {
                            'city': f"{data['name']}, {data['sys']['country']}",
                            'temperature': data['main']['temp'],
                            'humidity': data['main']['humidity'],
                            'pressure': data['main']['pressure'],
                            'description': data['weather'][0]['description'].title(),
                            'icon': data['weather'][0]['icon'],
                            'wind_speed': data['wind']['speed'],
                            'is_mock': False
                        }
                    elif resp.status_code == 401:
                        # API key invalid, fallback to simulation mode
                        weather = get_mock_weather(city)
                    else:
                        data = resp.json()
                        error = data.get("message", "Could not fetch weather data.").capitalize()
                except requests.RequestException:
                    # Fallback to simulation mode due to network issue
                    weather = get_mock_weather(city)
                    weather['network_fallback'] = True

            if weather:
                # Save search with the detailed data
                SearchHistory.objects.create(
                    city_name=weather['city'],
                    temperature=weather['temperature'],
                    humidity=weather['humidity'],
                    pressure=weather['pressure'],
                    description=weather['description'],
                    icon=weather['icon'],
                    wind_speed=weather['wind_speed'],
                    is_mock=weather['is_mock']
                )
                # Refresh list
                recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
        else:
            error = "Please enter a city name."

    return render(request, "main/index.html", {
        'weather': weather,
        'error': error,
        'recent_searches': recent_searches,
        'is_api_key_set': (API_KEY and API_KEY != "your_api_key_here")
    })