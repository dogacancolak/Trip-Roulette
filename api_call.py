import urllib.request
import json
import time


# BOSTON
# radius  = 10000
# lat = 42.359441   
# lon = -71.059767

# ISTANBUL
# radius  = 10000
# lat = 41.059995
# lon = 28.987315

location = str(lat) + ',' + str(lon)
key     = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'

endpoint =  'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
place_type = 'restaurant'

# max_price  = 2          # NOTE: adjust min_price as well?
                                                #&opennow
                                                # &maxprice={}
nav_request =  'location={}&radius={}&type={}&rankby=prominence&key={}'\
                .format(str(location), str(radius) , place_type, key)
# , str(max_price)

request = endpoint + nav_request
response = urllib.request.urlopen(request).read()
new_places = json.loads(response)

places = new_places

while "next_page_token" in new_places:

    next_page = new_places['next_page_token']
    time.sleep(1)

    new_request = request + '&pagetoken=' + next_page
    response = urllib.request.urlopen(new_request).read()
    new_places = json.loads(response)

    places["results"].extend(new_places["results"])

for p in places['results']:
    print("Name: ", p['name'])