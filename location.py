import requests
from geopy.geocoders import Nominatim

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return response.get("city")

loc = Nominatim(user_agent="GetLoc")

getLoc = loc.geocode(get_location())

Location = getLoc.address
Latitude = getLoc.latitude
Longitude = getLoc.longitude

# print(Location)
# print(get_location())
# print(Longitude)
# print(Latitude)
