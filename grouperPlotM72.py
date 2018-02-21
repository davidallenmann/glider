import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplekml

# user changeable variables
# import files
gpsFile = 'M72_Jun2017/M72gps.csv'
dataFile = 'M72_Jun2017/M72_RedGrouper.csv'
tagFile = 'M72_Jun2017/M72_VMT.csv'

# output files
mergeFile = 'M72_Jun2017/M72_merge.csv'
kmlFile = 'M72_Jun2017/M72_RedGrouper.kml'
kmlGlider = 'M72_Jun2017/M72gps.kml'

# Time zone offset for red grouper file
# if time in UTC, offsetHours = 0
offsetHours = 0


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
df = df.interpolate()


# read in grouper data
df2 = pd.read_csv(dataFile, sep=',', usecols=[1, 2])
df2.index = pd.to_datetime(df2[df2.columns[0]])
df2.index = df2.index + pd.DateOffset(hours=offsetHours)
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


# Summary stats
print("Sounds: ")
print(df2.sum())

# # Glider and sound plot
# plt.scatter(df_join.Longitude, df_join.Latitude, c='c')
# plt.scatter(df_join.Longitude, df_join.Latitude, c='r', s=df_join['sounds'] * 50)
# plt.show()

# plot with tag data
# limit time range
df5 = df_join.loc['2017-05-19 15:53':'2017-06-05 14:36']
plt.scatter(df5.Longitude, df5.Latitude, c='c')
plt.scatter(df5.Longitude, df5.Latitude, marker='v', c='b', s=df5['tagCount'] * 20)
plt.scatter(df5.Longitude, df5.Latitude, c='r', s=df5['sounds'] * 20)
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

start_date = '2017-06-03 03:45:58'
end_date = '2017-06-03 05:03:48'
print(df2.dropna()[start_date : end_date])
print(sum(df2.dropna()[start_date : end_date].sounds))

start_date = '2017-06-04 18:23:13'
end_date = '2017-06-04 18:36:48'
print(df2.dropna()[start_date : end_date])
print(sum(df2.dropna()[start_date : end_date].sounds))

start_date = '2017-06-04 21:26:54'
end_date = '2017-06-04 22:10:26'
print(df2.dropna()[start_date : end_date])
print(sum(df2.dropna()[start_date : end_date].sounds))