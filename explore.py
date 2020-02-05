import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from enum import Enum
import os


class Fields(str, Enum):
    trade_time = 'trade_time'
    channel = 'channel'
    sale_value = 'sale_value'


fname = 't0_predict_data.csv'
data = pd.read_csv(fname, parse_dates=[Fields.trade_time])

channels = data.groupby(Fields.channel)

fig = plt.figure()
axes = fig.subplots(len(channels), 1)
for ax, (channel, df_channel) in zip(axes, channels):
    ax.set_title(channel)
    ax.xaxis_date()
    x_data = df_channel[Fields.trade_time].map(mdates.date2num)
    ax.plot(x_data, df_channel[Fields.sale_value])

os.makedirs('results', exist_ok=True)
fig.savefig('results/SalesByTime.pdf')




