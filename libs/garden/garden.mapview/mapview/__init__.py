# coding=utf-8
"""
MapView
=======

.. author:: Mathieu Virbel <mat@kivy.org>

MapView is a Kivy widget that display maps.
"""

__all__ = ["Coordinate", "Bbox", "MapView", "MapSource", "MapMarker",
           "MapLayer", "MarkerMapLayer", "MapMarkerPopup"]
__version__ = "0.2"

MIN_LATITUDE = -90.
MAX_LATITUDE = 90.
MIN_LONGITUDE = -180.
MAX_LONGITUDE = 180.
from kivy.utils import platform
from kivy.app import App
import os.path
if platform == 'ios': # Erik Sandberg fix 10/14/2018
    root_folder = App().user_data_dir
    CACHE_DIR = os.path.join(root_folder, 'cache')
    cache_folder = os.path.join(root_folder, 'cache')
    CACHE_DIR = cache_folder
    #CACHE_DIR = "Library/Caches"
else:
    CACHE_DIR = "cache"
try:
    # fix if used within garden
    import sys
    sys.modules['mapview'] = sys.modules['kivy.garden.mapview.mapview']
    del sys
except KeyError:
    pass

from mapview.types import Coordinate, Bbox
from mapview.source import MapSource
from mapview.view import MapView, MapMarker, MapLayer, MarkerMapLayer, \
    MapMarkerPopup
