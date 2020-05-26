from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from gpsblinker import GpsBlinker
import requests
import json
import urllib.request

class GpsHelper():
    has_centered_map = False

    def run(self):
        # Get a reference to GpsBlinker, then call blink()
        gps_blinker = App.get_running_app().root.homepage.map.ids.blinker
        # Start blinking the GpsBlinker
        gps_blinker.blink()

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

        # Configure GPS
        if platform == 'android' or platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)

        else:
            key = '58a2cf7603d503df29b6ed36d4d0a919'
            send_url = 'http://api.ipstack.com/check?access_key=' + key
            j = json.loads(urllib.request.urlopen(send_url).read())
            lat = j['latitude']
            lon = j['longitude']
            self.update_blinker_position(lat=lat, lon=lon)

    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat'] #App.get_running_app().user_info.lat 
        my_lon = kwargs['lon'] #App.get_running_app().user_info.lon
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position
        gps_blinker = App.get_running_app().root.homepage.map.ids.blinker
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon
        App.get_running_app().user_info.lat = my_lat
        App.get_running_app().user_info.lon = my_lon

        # Center map on gps
        if not self.has_centered_map:
            map = App.get_running_app().root.homepage.map
            map.center_on(my_lat, my_lon)
            self.has_centered_map = True


    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()