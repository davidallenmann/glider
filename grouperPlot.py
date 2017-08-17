import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplekml

# user changeable variables
# import files
gpsFile = '/w/loggerhead/glider/M72/M72gps.csv'
dataFile = '/w/loggerhead/glider/M72/M72_RedGrouper.csv'
tagFile = '/w/loggerhead/glider/M72/M72_VMT.csv'

# output files
mergeFile = '/w/loggerhead/glider/M72/M72_merge.csv'
kmlFile = '/w/loggerhead/glider/M72/M72_RedGrouper.kml'
kmlGlider = '/w/loggerhead/glider/M72/M72gps.kml'

# read in and format GPS csv file
df = pd.read_csv(gpsFile, header=0, sep=',', names=['Date_Time', 'Latitude', 'Longitude'], dtype = {'Date_Time': str, 'Latitude': np.float64, 'Longitude': np.float64})

df = df.dropna()
df.index = pd.to_datetime(df.Date_Time)
# df = df.drop('Date', 1)
# df = df.drop('Time', 1)

df = df.drop('Date_Time', 1)
df = df.dropna()
df = df.sort_index()


# resample location to 1 minute intervals averaging lat and lon values
df = df.resample('1T').mean()


# read in grouper data
df2 = pd.read_csv(dataFile, sep=',', usecols=[1, 2])
df2.index = pd.to_datetime(df2[df2.columns[0]])
df2 = df2.drop(df2.columns[0], axis=1)
df2 = df2.sort_index()
# resample 1 minute bins
df2 = df2.resample('1T').sum()
df2.columns = ['sounds']


# read in VMT
df3 = pd.read_csv(tagFile, sep=',')
df3.index = pd.to_datetime(df3[df3.columns[0]])
df3 = df3.drop(df3.columns[0], axis=1)
df3 = df3.sort_index()

# bin VMT data into pings per minute (not unique)
df4 = df3.resample('1T').count()
df4.columns = ['tagCount']


# join dataframes
df_join = df.join(df2, how='outer')
df_join = df_join.join(df4, how='outer')

# df_join = df_join.dropna()

# plot
plt.scatter(df_join.Longitude, df_join.Latitude, c='c')
plt.scatter(df_join.Longitude, df_join.Latitude, marker='v', c='b', s=df_join['tagCount'] * 20)
plt.scatter(df_join.Longitude, df_join.Latitude, c='r', s=df_join['sounds'] * 20)
plt.show()

# export to csv
df_join.to_csv(mergeFile)

# export to kml
kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
# i is index ; row.Name row.lat row.lon row.count
for i, row in df_join.iterrows():
    pnt = kml.newpoint(name = "", description = "", coords=[(row.Longitude, row.Latitude)])
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
    pnt.style.iconstyle.scale = str(np.float(row[2])/1.4)

kml.save(kmlFile)

latlon = []
for i,row in df.iterrows():
    latlon.append((row.Longitude, row.Latitude, 0.0))

kml = simplekml.Kml()
ls = kml.newlinestring(name = "glider", description = "", coords=latlon)
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
kml.save(kmlGlider)

