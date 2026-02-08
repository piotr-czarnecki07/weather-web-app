from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from dotenv import dotenv_values
import redis
import json
import requests

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))

def city(requset, city: str):
    if not city.isalpha():
        return HttpResponseRedirect('/notfound')

    config = dotenv_values('.env')
    r = redis.Redis(
        host=config.get('DB_ENDPOINT'),
        port=config.get('DB_PORT'),
        username=config.get('DB_USERNAME'),
        password=config.get('DB_PASSWORD'),
        decode_responses=False,
    )

    city = city.title()
    cache = r.get(city)

    if cache is not None:
        weather = json.loads(cache)

        location = weather.get('location')
        current = weather.get('current')
        forecast = weather.get('forecast').get('forecastday') # array of 5 days with weather data for each day
    else:
        params = {
            'key': config.get('API_KEY'),
            'q': city,
            'days': 5,
            'aqi': 'no',
            'alerts': 'no'
        }

        response = requests.get(config.get('API_URL')+'forecast.json', params=params)
        if 200 <= response.status_code < 300:
            weather = response.json()
            location = weather.get('location')
            current = weather.get('current')
            forecast = weather.get('forecast').get('forecastday')

            for day in range(len(forecast)):
                forecast[day]['day_num'] = day + 1

            r.set(city, json.dumps(weather))
            r.expire(city, 3600) # weather data expires after an hour
            r.close()
        else:
            return HttpResponseRedirect('/notfound')

    for key, value in current.items():
        if type(current[key]) is float:
            current[key] = int(value)

    for forecastday in forecast:
        forecastday['day']['avgtemp_c'] = int(forecastday['day']['avgtemp_c'])
        forecastday['day']['avgtemp_f'] = int(forecastday['day']['avgtemp_f'])

    template = loader.get_template('city.html')
    return HttpResponse(template.render(request=requset, context={'location': location, 'current': current, 'forecast': forecast}))

def atDay(request, city: str, day: int):
    if day > 5 or day < 1:
        return HttpResponseRedirect('/notfound')

    config = dotenv_values('.env')
    r = redis.Redis(
        host=config.get('DB_ENDPOINT'),
        port=config.get('DB_PORT'),
        username=config.get('DB_USERNAME'),
        password=config.get('DB_PASSWORD'),
        decode_responses=False,
    )

    cache = r.get(city)
    r.close()

    if cache is not None:
        weather = json.loads(cache)
        forecast = weather.get('forecast').get('forecastday')

        for forecastday in forecast:
            if forecastday.get('day_num') == day:
                daydata = forecastday
                break
    else:
        return HttpResponseBadRequest('Cache expired')

    for key, value in daydata['day'].items():
        if type(daydata['day'][key]) is float:
            daydata['day'][key] = int(value)

    template = loader.get_template('atDay.html')
    return HttpResponse(template.render(request=request, context={'daydata': daydata, 'city': city}))