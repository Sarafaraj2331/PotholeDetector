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

# print(Location, Latitude, Longitude)

# print(getLoc.address)

# print("Latitude = ", getLoc.latitude, "\n")
# print("Longitude = ", getLoc.longitude)



# import geocoder
# import datetime
# import pymongo

# client = pymongo.MongoClient('mongodb://localhost:5000/')
# time1 = datetime.datetime.now().strftime('%d-%m-%Y')

# def loc():
#     g = geocoder.ip('me')
#     return g.latlng

# def record():
#     try:
#         time2 = datetime.datetime.now().strftime(' %H-%M-%S')
#         l = loc()
#         lat, long = l[0], l[1]
#         mydb = client["Data"]
#         inf = mydb.pothole
#         for rec in inf.find():
#             if lat not in rec['latitude']:
#                 rd = {'date': time1, 'time': time2, 'latitude': lat, 'longitude': long}
#         inf.insert_one(rd)
#     except:
#         pass
