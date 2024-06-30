import requests
from django.http import JsonResponse
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_temperature(city):
    # Replace with your OpenWeatherMap API key
    url = f"""http://api.openweathermap.org/data/2.5/weather?q={
        city}&units=metric&appid={'6534af216891588b0a9c01b841b17cc6'}"""
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperature = data['main']['temp']
        return temperature
    else:
        return None


def say_hello(request):
    ip = get_client_ip(request)
    access_token = '6702a2080d373d'

    url = f"""https://ipinfo.io/{ip}/json?token={access_token}"""
    response = requests.get(url)
    data = response.json()

    city = data.get('city', 'Unknown')

    visitor_name = request.GET.get('visitor_name', 'Guest')
    greeting = f"Hello, {visitor_name}!"

    temperature = get_temperature(city)
    if temperature is not None:
        greeting_with_temp = f"""{greeting}, the temperature is {
            temperature} degrees Celsius in {city}"""
    else:
        greeting_with_temp = f"""{
            greeting}, but we couldn't retrieve the temperature for {city}"""

    return JsonResponse({
        'client_ip': ip,
        'location': city,
        'greeting': greeting_with_temp
    })
