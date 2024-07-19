import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from weather.models import SearchCity


def search_geo(request):
    name = request.GET.get('name', '')
    language = request.GET.get('language', 'en')
    response = requests.get('https://geocoding-api.open-meteo.com/v1/search',
        params={
            'name': name,
            'language': language,
            'count': 10,
            'format': 'json'
        }
    )

    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.text)

    return JsonResponse(response.json())


def get_current(city):
    response = requests.get('https://api.open-meteo.com/v1/forecast',
        params={
            'timezone': 'auto',
            'latitude': city['latitude'],
            'longitude': city['longitude'],
            'current': [
                'temperature_2m',
                'weather_code',
                'wind_speed_10m',
                'wind_direction_10m',
                'relative_humidity_2m',
                'pressure_msl',
                'is_day'
            ],
        }
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def get_today(city):
    response = requests.get('https://api.open-meteo.com/v1/forecast',
        params={
            'timezone': 'auto',
            'latitude': city['latitude'],
            'longitude': city['longitude'],
            'hourly': [
                'temperature_2m',
                'weather_code',
                'is_day'
            ],
            'forecast_hours': 24,
        }
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def get_two_weeks(city):
    response = requests.get('https://api.open-meteo.com/v1/forecast',
        params={
            'timezone': 'auto',
            'latitude': city['latitude'],
            'longitude': city['longitude'],
            'daily': [
                'temperature_2m_max',
                'weather_code',
            ],
            'forecast_days': 14
        }
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def get_weather(request):
    try:
        city = json.loads(request.GET.get('city', ''))
        city_stat, _ = SearchCity.objects.get_or_create(name=city['name'])
        city_stat.searchs = city_stat.searchs + 1
        city_stat.save()
    except json.decoder.JSONDecodeError:
        return HttpResponse(status=400, content='Bad request')
    except KeyError:
        return HttpResponse(status=400, content='Bad request')

    try:
        result = {
            'current': get_current(city),
            'today': get_today(city),
            'twoweeks': get_two_weeks(city),
        }
    except Exception as e:
        return HttpResponse(status=500, content=e)

    return JsonResponse(json.dumps(result), safe=False)


def get_stats(request):
    all_cities = SearchCity.objects.order_by('-searchs')
    all_cities = [city.serialize() for city in all_cities]
    return JsonResponse(all_cities, safe=False)


def index(request):
    return render(request, 'index.html')
