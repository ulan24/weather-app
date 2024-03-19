from django.shortcuts import render
from datetime import datetime, timedelta
import requests


def weather_ui(request):
    api_key = 'your_api_key'
    city = request.POST.get('city') 
    api_url = f'your_api_url'
    response = requests.get(api_url)
    
    weekdays_abrv = []
    winds = []
    temps = []
    humids = []
    precips = []
    descs = []
    next_dates = []
    grouped_forecast = {}


    # get the short form of next 5 days
    today = datetime.today()
    todays_day = datetime.now().strftime('%A')
    todays_date = datetime.now().strftime('%d %b %Y')
    current_date = datetime.now().date()
    current_timestamp = datetime.now().timestamp()

    for i in range(4):
        next_day = today + timedelta(days=i+1)
        day = next_day.strftime('%a')
        weekdays_abrv.append(day)

        next_date = today + timedelta(days=i+1)
        formatted_date = next_date.strftime("%d %b %Y")

        next_dates.append(formatted_date)   


    if request.method == 'POST':
        print(city)

    if response.status_code == 200:
        data = response.json()
        forecast_list = data['list']
        country = data['city']['country']

        if city == None and country == 'IT':
            city = 'Bishkek'
            country = 'KG'

        for entry in forecast_list:
            # Convert the timestamp to a datetime object
            timestamp = datetime.fromtimestamp(entry["dt"])

            # Get the date from the timestamp
            forecast_date = timestamp.date()


            # Check if the forecast date is already in the dictionary
            if forecast_date not in grouped_forecast:
                # If not, add a new entry with the date as the key and the entry as the value
                grouped_forecast[forecast_date] = entry
            else:
                # If the date is already in the dictionary, compare the time difference between current time and forecast time
                current_diff = abs(current_timestamp - entry['dt'])
                existing_diff = abs(current_timestamp - grouped_forecast[forecast_date]['dt'])
                
                # If the current entry has a closer time to the current time, update the entry in the dictionary
                if current_diff < existing_diff:
                    grouped_forecast[forecast_date] = entry
        
        unique_forecast = list(grouped_forecast.values())[:5]
        
        weather_description = forecast_list[0]['weather'][0]['main']

        print(weather_description)

        if 'Clear' == weather_description:
                background_image = 'clear.jpg'
        elif 'Clouds' == weather_description:
            background_image = 'clouds.jpg'
        elif 'Fog' == weather_description:
            background_image = 'fog.jpg'
        elif 'Rain' == weather_description:
            background_image = 'rain.jpg'
        else:
            background_image = 'snow.jpg'


        for forecast in unique_forecast:
            temperature = forecast['main']['temp']
            # weather_description = forecast['weather'][0]['main']
            rain_volume = forecast.get('rain', {}).get('1h', 0)  # Rain volume in the last hour (if available)
            snow_volume = forecast.get('snow', {}).get('1h', 0) 
            precipitation = rain_volume + snow_volume
            wind = forecast['wind']['speed']
            humidity = forecast['main']['humidity']

            temps.append(temperature)
            winds.append(wind)
            humids.append(humidity)
            precips.append(precipitation)
            descs.append(weather_description)


        forecast_data = zip(weekdays_abrv, temps[1:])
        city = city.capitalize()

        
        context = {
            'api_data': data,
            'today': today,
            'date': todays_date,
            'weekdays': weekdays_abrv,
            "winds": winds,
            "humids": humids,
            "precips": precips,
            "descs": descs,
            "temps": temps,
            "forecast_data": forecast_data,
            "next_dates": next_dates,
            "background_image": background_image,
            "city": city,
            "country": country,
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'error.html')


    return render(request, 'index.html')
