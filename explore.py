import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from enum import Enum
import os
import datetime as dt


class Fields(str, Enum):
    trade_time = 'trade_time'
    channel = 'channel'
    sale_value = 'sale_value'
    bus_day = 'business_day'


fname = 't0_predict_data.csv'
data = pd.read_csv(fname, parse_dates=[Fields.trade_time])
data = data.sort_values(Fields.trade_time)

cutoff_time = dt.time(9, 30)
data[Fields.bus_day] = data[Fields.trade_time].map(lambda x: x.date() - dt.timedelta(int(x.time() < cutoff_time)))
channels = data.groupby(Fields.channel)

tot_sales_by_channel = []
for channel, df_channel in channels:
    tot_sales = df_channel.groupby(Fields.bus_day)[Fields.sale_value].sum()
    tot_sales_by_channel.append((channel, tot_sales))


fig1 = plt.figure(figsize=(60, 50))
axes = fig1.subplots(len(channels), 1, sharex=True)
for ax, (channel, df_channel) in zip(axes, channels):
    ax.set_title(channel)
    ax.xaxis_date()
    x_data = df_channel[Fields.trade_time].map(mdates.date2num)
    ax.plot(x_data, df_channel[Fields.sale_value])
    plt.yticks(fontsize=20)

plt.xticks(fontsize=20)
plt.tight_layout()
os.makedirs('results', exist_ok=True)
fig1.savefig('results/SalesByTime.pdf')


fig2 = plt.figure(figsize=(50, 50))
axes = fig2.subplots(len(tot_sales_by_channel), 1, sharex=True)
for ax, (channel, sr_tot_sales) in zip(axes, tot_sales_by_channel):
    ax.set_title(channel)
    ax.xaxis_date()
    x_data = sr_tot_sales.index.map(mdates.date2num)
    ax.plot(x_data, sr_tot_sales)
    plt.yticks(fontsize=20)

plt.xticks(fontsize=20)
plt.tight_layout()
os.makedirs('results', exist_ok=True)
fig2.savefig('results/SalesByDate.pdf')









