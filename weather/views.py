import json
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


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


def get_weather(request):
    city = json.loads(request.GET.get('city', ''))

    result = {
        'today': None,
        'twoweeks': None
    }

    response = requests.get('https://api.open-meteo.com/v1/forecast',
        params={
            'latitude': city['latitude'],
            'longitude': city['longitude'],
            'current_weather': True
        }
    )

    result['today'] = response.json()

    if response.status_code != 200:
        return HttpResponse(status=response.status_code, content=response.text)

    return JsonResponse(json.dumps(result), safe=False)


def index(request):
    return render(request, 'index.html')
