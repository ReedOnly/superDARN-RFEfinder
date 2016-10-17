from scipy import *
from davitpy.utils import *
import datetime as dt

lon=-45.6
lat=79.2
lonMlt, latMlt = coord_conv(lon, lat, 'mag', 'mlt',
                                    altitude=300.,
                                    date_time=dt.datetime(2012,3,12,0,56))
print lonMlt
print latMlt