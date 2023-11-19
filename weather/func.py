import asyncio
import aiohttp
from geopy.geocoders import Nominatim

def get_params(city, date_from, date_to):
    """Generating params for weather API"""
    dates = []

    geolocator = Nominatim(user_agent="weather_bot")

    location = geolocator.geocode(city)

    params = {"latitude": location.latitude,
              "longitude": location.longitude,
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto"}

    for year in range(2020, 2023):
        advanced_params = {"start_date": f"{year}-{date_from}",
                           "end_date": f"{year}-{date_to}"}
        advanced_params.update(params)
        dates.append(advanced_params)

    return dates

async def fetch_result(session, params):
    """Creates json file with weather values"""
    async with session.get('https://archive-api.open-meteo.com/v1/archive', params=params) as result:
        return await result.json()
async def get_request(all_params):

    """Creates asynchronous requests"""
    async with aiohttp.ClientSession() as session:
        requests = [fetch_result(session, params) for params in all_params]
        result = await asyncio.gather(*requests, return_exceptions=False)

        return result


def get_max_value(params):
    """Sorts json file and return max value"""
    max_values_list = []
    for maximum in params["daily"]['temperature_2m_max']:
        max_values_list.append(maximum)
    return max(max_values_list)


def get_min_value(params):
    """Sorts json file and return min value"""
    min_values_list = []
    for minimum in params["daily"]['temperature_2m_min']:
        min_values_list.append(minimum)
    return min(min_values_list)

def get_average_value(params):
    """Sorts json file and return average value"""
    average_values_list = []
    for average in params["daily"]['temperature_2m_min']:
        average_values_list.append(average)
    return sum(average_values_list) // len(average_values_list)

async def get_values(city, date_from, date_to):
        """Makes lists with all values and sorts it"""
        minimum = []
        maximum = []
        average = []
        values = await get_request(get_params(city, date_from, date_to))
        for value in values:

            minimum.append(round(get_min_value(value)))
            maximum.append(round(get_max_value(value)))
            average.append(round(get_average_value(value)))

        return f"Температура в эти дни от {min(minimum)} до {max(maximum)}\nСредняя температура примерно:{sum(average) // len(average)}"