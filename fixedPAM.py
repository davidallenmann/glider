import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import simplekml

# user changeable variables
# import files
dataFile = 'detections_auto.csv'

start_date = '2017-02-18 22:38:59'
end_date = '2017-02-18 23:40:59'

start_date = '2017-03-03 17:37:44'
end_date = '2017-03-03 18:52:36'

start_date = '2017-06-03 03:45:58'
end_date = '2017-06-03 05:03:48'

start_date = '2017-06-04 18:23:13'
end_date = '2017-06-04 18:36:48'

start_date = '2017-06-04 21:26:54'
end_date = '2017-06-04 22:10:26'
	
start_date = '2017-10-01 03:20:20'
end_date = '2017-10-01 04:48:47'

start_date = '2017-10-02 09:17:33'
end_date = '2017-10-02 10:46:33'



# read in grouper data
df = pd.read_csv(dataFile, sep=',', usecols=[1, 2])
df.columns=['dt', 'calls']
df.index = pd.to_datetime(df.dt)

df['callsFiltered'] = df.calls * (df.calls<10)

df[start_date : end_date]


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

