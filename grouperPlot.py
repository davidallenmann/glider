import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplekml

# user changeable variables
# import files
gpsFile = '/w/glider/M69gps.csv'
dataFile = '/w/glider/M69_RedGrouper.csv'

# output files
mergeFile = '/w/glider/M69_merge.csv'
kmlFile = '/w/glider/M69_RedGrouper.kml'
kmlGlider = '/w/glider/M69gps.kml'


# read in and format GPS csv file
df = pd.read_csv(gpsFile, sep=',', names=['date', 'time', 'lat', 'lon'], dtype = {'date': str, 'time': str, 'lat': np.float64, 'lon': np.float64})

df = df.dropna()
df.index = pd.to_datetime(df.date + df.time)
df = df.drop('date', 1)
df = df.drop('time', 1)
df.lat = pd.rolling_mean(df.lat, 5, center=True)
df.lon = pd.rolling_mean(df.lon, 5, center=True)
df = df.dropna()
df = df.sort_index()

# read in grouper data
df2 = pd.read_csv(dataFile, sep=',')
df2.index = df2[df2.columns[0]]
df2 = df2.sort_index()

# join dataframes
df_join = df.join(df2, how='outer')
df_join.lat = df_join.lat.interpolate()
df_join.lon = df_join.lon.interpolate()
df_join = df_join.dropna()


# export to csv
df_join.to_csv(mergeFile)

# export to kml
kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
# i is index ; row.Name row.lat row.lon row.count
for i, row in df_join.iterrows():
    pnt = kml.newpoint(name = "", description = "", coords=[(row.lon, row.lat)])
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
    pnt.style.iconstyle.scale = str(row[3]/1.4)

kml.save(kmlFile)

latlon = []
for i,row in df.iterrows():
    latlon.append((row.lon, row.lat, 0.0))

kml = simplekml.Kml()
ls = kml.newlinestring(name = "M69", description = "", coords=latlon)
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
kml.save(kmlGlider)

