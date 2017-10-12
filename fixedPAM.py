import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplekml

# user changeable variables
# import files
dataFile = '/w/loggerhead/glider/detections_auto.csv'

# read in grouper data
df = pd.read_csv(dataFile, sep=',', usecols=[1, 2])
df.columns=['dt', 'calls']
df.index = pd.to_datetime(df.dt)

df['callsFiltered'] = df.calls * (df.calls<10)


#df2.index = pd.date_range(start='20160408T12:00', periods=len(df2), freq='20T')

# df2.index = df2.index + pd.DateOffset(hours=4)
#df2 = df2.drop(df2.columns[0], axis=1)
df = df.sort_index()

# resample  minute bins
df2 = df.resample('1D').mean()
df2.callsFiltered = df2.callsFiltered

ax = df2.callsFiltered.plot()
ax.set_ylabel('Daily Mean Calls/Min')
plt.show()

grouped = df2.groupby(df2.index.hour)
meanCallsPerHour = grouped.callsFiltered.mean()
stdCallsPerHour = grouped.callsFiltered.std()

ax = meanCallsPerHour.plot()
ax.set_ylabel('Mean Calls Per Hour')
ax.set_xlabel('Hour of Day')
plt.show()

