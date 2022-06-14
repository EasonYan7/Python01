import datetime

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

data = ts.get_hist_data('000002', start='2019-04-15', end='2021-04-20')
df1 = ts.get_realtime_quotes(['000002', '300015'])
df1 = df1[['code', 'name', 'price', 'bid', 'ask', 'time']]
data.to_csv('share.csv')

data = pd.read_csv('share.csv')
d = []
for i in range(len(data)):
    d.append(datetime.datetime.strptime(data['date'][i], '%Y-%m-%d'))
data['date'] = d
plt.plot(data['date'], data['close'], color='red', label='share')
plt.xticks(rotation=45)
plt.show()
