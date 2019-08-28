import folium
import pandas as pd
import json

data_json = open("world.json", 'r', encoding='UTF-8').read()

#Read the Volcanoes.txt file into a dataframe
data = pd.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])

#Load the elevation data from the Volcanoes.txt file into a list
elevation = list(data["ELEV"])

#Function for color generator as per elevation
def color_generator(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <=3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location = [38.58, -99.09], zoom_start = 3.5, tiles = "Stamen Terrain")

#Creating a feature group instead of all the 62 elements in the volcanoes file
fgv = folium.FeatureGroup(name="Volcanoes")

#Looping through the latitudes and longitudes by zipping the coordinates
for lt, ln, el in zip(lat, lon, elevation):
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius = 4, popup = str(el) + " m",
    fill_color = color_generator(el), color = 'grey', fill_opacity = 1))

#Creating a feature group instead of all the elements in the World.json file
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data = data_json), style_function = lambda x: {'fillColor': 'yellow' if x['properties']
['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' })

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
