import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

range = pd.date_range('2015-01-01', '2015-12-31', freq='15min')
df = pd.DataFrame(index = range)

df['AmbientTemp'] = np.random.randint(low=12, high=30, size=len(df.index))
df['WortTemp'] = np.random.randint(low=18, high=24, size=len(df.index))
df['HeatOn'] = np.random.randint(low=0, high=2, size=len(df.index))
df['FridgeOn'] = np.random.randint(low=0, high=2, size=len(df.index))

print (df.head())

print()

weekly_summary = pd.DataFrame()
weekly_summary['AmbientTemp'] = df.AmbientTemp.resample('D').mean()
weekly_summary['WortTemp'] = df.WortTemp.resample('D').mean()
weekly_summary['HeatOn'] = df.HeatOn.resample('D').mean()
weekly_summary['FridgeOn'] = df.FridgeOn.resample('D').mean()

#weekly_summary = weekly_summary.truncate(before='2015-01-05', after='2015-12-27')
print(weekly_summary)

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(weekly_summary.index, weekly_summary['AmbientTemp'], 'g-')
ax2.plot(weekly_summary.index, weekly_summary['WortTemp'], 'b-')

ax1.set_xlabel('Date')
ax1.set_ylabel('AmbientTemp', color='g')
ax2.set_ylabel('WortTemp', color='b')

plt.show()
plt.rcParams['figure.figsize'] = 12,5