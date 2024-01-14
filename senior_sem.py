import numpy as np
from datetime import datetime
from scipy.constants import c
a = 6_378_137.00
e_sq =  6.69437999014 * 10**-3
def v(phi):
    """Make sure to convert to degrees first"""
    return a/np.sqrt(1-e_sq*np.sin(phi)**2)
def generate_transmission(lat,lon):
    time_of_transmission=np.datetime64(datetime.now())+np.timedelta64(np.random.randint(10**9),"ns")
    randlat= lat+np.random.randint(5)+np.random.rand()
    randlon=lon+np.random.randint(5)+np.random.rand()
    return randlat,randlon,time_of_transmission
def wgs_84_geo_to_cartes(lat,lon,alt):
    lat,lon=np.deg2rad([lat,lon])
    x=(v(lat)+alt)*np.cos(lat)*np.cos(lon)
    y=(v(lat)+alt)*np.cos(lat)*np.sin(lon)
    z=(v(lat)*(1-e_sq)+alt)*np.sin(lat)
    return x,y,z
def wgs_84_cartes_to_geo(x,y,z):
    phi = np.arctan(z/((1-e_sq)*np.sqrt(x**2 + y**2)))
    gamma = np.arctan(y/x)
    lat,lon=np.rad2deg([phi,gamma])
    
    return lat,lon
def cartes_tuple_distance(tuple1,tuple2):
    x1,y1,z1=tuple1
    x2,y2,z2=tuple2
    return np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
def generate_satellite(trans_tuple):
    lat,lon,time =trans_tuple
    randlat = lat+np.random.randint(40)+np.random.rand()
    randlon = lon+np.random.randint(40)+np.random.rand()
    alt = 50*10**6 + np.random.randint(10**6)
    dist = cartes_tuple_distance(wgs_84_geo_to_cartes(lat,lon,0),
                                 wgs_84_geo_to_cartes(randlat,randlon, alt))
    # return dist
    time_of_travel_rounded=np.timedelta64(int(np.round(dist/c,9)*10**9),"ns")
    time_of_arrival = time + time_of_travel_rounded
    return {"coords":wgs_84_geo_to_cartes(randlat,randlon, alt),"TOA":time_of_arrival}#,randlat,randlon