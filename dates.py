
from geopy.geocoders import Nominatim
import grequests

#
# def get_params(city, start, end):
#     # функция для создания словаря
#     dates = []
#     geolocator = Nominatim(user_agent="weather_bot")
#
#     location = geolocator.geocode("Moscow")
#
#     params = {"latitude": location.latitude,
#               "longitude": location.longitude,
#               "daily": ["temperature_2m_max", "temperature_2m_min"],
#               "timezone": "auto"}
#
#     # for year in range(2020, 2021):
#     #     params2 = {"start_date": f"{year}-{start}",
#     #                "end_date": f"{year}-{end}"}
#     #
#     #     params2.update(params)
#     #
#     #     dates.append(params2)
#
#     return params
#
#
# def get_request(par):
#     all_dates = []
#     session = grequests.Session()
#     for param in par:
#         # функция для обращения к сайту
#         weather_site = session.get("https://archive-api.open-meteo.com/v1/archive", params=param).json()
#
#         all_dates.append(weather_site)
#
#     return all_dates
#
# print(get_params("London", "01-01", "01-02"))
geolocator = Nominatim(user_agent="weather_bot")

location = geolocator.geocode("New York")

print(location.latitude, location.longitude)





