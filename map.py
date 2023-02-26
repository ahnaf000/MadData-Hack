import math
import requests
import folium
import pandas as pd
from folium.plugins import HeatMap
import branca



#accident map
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
zipData = pd.read_csv('chiZip.csv')
merged = pd.read_csv('merged.csv')
folium.GeoJson("chicago.geojson").add_to(chicago_map)

heat_map = [[row['Lat'], row['Long'], math.log(row['Count'])] for index, row in merged.iterrows()]
HeatMap(heat_map,radius=30).add_to(chicago_map)

harshArea = merged[:15]
latitudes = list(harshArea['Lat'])
longitudes = list(harshArea['Long'])
labels = []
for index, row in harshArea.iterrows():
    label = "Zip code: {}, Crash Count: {}".format(row['zip_code'], row['Count'])
    labels.append(label)
    
# labels = list(latitudes,longitudes,"\n",harshArea['Count'])

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label,icon=folium.Icon(color="orange", icon="info-sign") ).add_to(chicago_map) 
      
    
# add incidents to map
#chicago_map.add_child(incidents)



#damage map
combine = pd.read_csv('combined.csv')
chicago_map2 = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
folium.GeoJson("chicago.geojson").add_to(chicago_map2)

damage_data = [[row['Lat'], row['Long'], (100000000*row['avg_weighted_cost'])] for index, row in combine.iterrows()]
HeatMap(damage_data,radius=30).add_to(chicago_map2)


chicago_map.save('accident.html')
chicago_map2.save('damage_cost.html')