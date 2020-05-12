import urllib.request
import json
radius  = 300
lat = 42.359441
lon = -71.059767

location = str(lat) + ',' + str(lon)
key     = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'

endpoint =  'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
type = 'restaurant'
max_price  = 4          # NOTE: adjust min_price as well?
nav_request =  'location={}&radius={}&maxprice={}&opennow&type={}&key={}'\
                .format(str(location), str(radius), str(max_price), type, key)

request = endpoint + nav_request
response = urllib.request.urlopen(request).read()

locations = json.loads(response)

print(locations)