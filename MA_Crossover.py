# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 22:04:40 2021

@author: mnbah
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as data
from py5paisa.order import Order, OrderType, Exchange, bo_co_order
#import talib

#from datetime import datetime

'''# set start and end dates 
start = datetime.datetime(2020, 2, 1) 
end = datetime.datetime(2020, 2, 1) 
# extract the closing price data
ultratech_df = data.DataReader(['ULTRACEMCO.NS'], 'yahoo', start = start, end = end)['Close']
ultratech_df.columns = {'Close Price'}
ultratech_df.head(10)

ultratech_df['Close Price'].plot(figsize = (15, 8))
plt.grid()
plt.ylabel("Price in Rupees")
plt.show()'''

####----Step 1 ---- Login ---#####################

from py5paisa import FivePaisaClient
cred={
    "APP_NAME":"5P55182810",
    "APP_SOURCE":"6915",
    "USER_ID":"qlBZXPszu7a",
    "PASSWORD":"R0AsODgvV0F",
    "USER_KEY":"1N0gB2re3MuVhSiWD6d6DWL4uCECrR7w",
    "ENCRYPTION_KEY":"oeuqIeJ5jTFhT7rWze1Ndo2kwVRvLhLe"
    }

client = FivePaisaClient(email="mnbahmed786@gmail.com", passwd="Trade987", dob="19890226",cred=cred)
client.login()

####----Step 2 ---- Data Reading ---#################

df= client.historical_data('N','C',999920000,'5m','2021-08-16','2021-08-17')
#print(df) 
Close = df['Close']
#print(Close)


####----Step 3 ---- Moving Average Calculation ---#################

#df['recent_volume30'] = talib.MA(df['volume'], timeperiod = 30, matype=0)
#df['average_volume120'] = talib.MA(df['volume'], timeperiod = 120, matype=0)

df['1_SMA'] = df['Close'].rolling(window = 1, min_periods = 1).mean()
df['20_SMA'] = df['Close'].rolling(window = 20, min_periods = 1).mean()

df['1_SMA'].plot(color = 'r',label = '1-day SMA')
df['20_SMA'].plot(color = 'g',label = '20-day SMA')


####----Step 4 ---- Conditions for BUY/SELL ---###################

df['Signal']=np.where(df['1_SMA'] > df['20_SMA'], 1, 0)
df['Position']=df['Signal'].diff()

df['Signal']=np.where(df['Position'] == 1, df['Close'], np.NAN)
df['Signal']=np.where(df['Position'] == -1, df['Close'], np.NAN)

if( df[df['Position'] == 1] ):
    test_order=bo_co_order(scrip_code=47737,BuySell='B',Qty=0, LimitPriceInitialOrder=205,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=215.0,TriggerPriceForSL=203,ExchType='C',Exch='N',RequestType='P',AtMarket=False)
    client.bo_order(test_order)

####----Step 5 ---- Plot for BUY/SELL ---###################
plt.plot(df[df['Position'] == 1].index, 
         df['1_SMA'][df['Position'] == 1], 
         '^', markersize = 15, color = 'g', label = 'buy')
# plot ‘sell’ signals
plt.plot(df[df['Position'] == -1].index, 
         df['20_SMA'][df['Position'] == -1], 
         'v', markersize = 15, color = 'r', label = 'sell')

'''
start = datetime.datetime(2020, 2, 1) 
end = datetime.datetime(2020, 2, 1) 
ultratech_df = data.DataReader(['ULTRACEMCO.NS'], 'yahoo', start = start, end = end)['Close']

# create 20 days simple moving average column
ultratech_df['20_SMA'] = ultratech_df['Close Price'].rolling(window = 1, min_periods = 1).mean()
# create 50 days simple moving average column
ultratech_df['50_SMA'] = ultratech_df['Close Price'].rolling(window = 20, min_periods = 1).mean()
# display first few rows
#print(ultratech_df.head()) 

ultratech_df['Signal'] = 0.0
ultratech_df['Signal'] = np.where(ultratech_df['20_SMA'] > ultratech_df['50_SMA'], 1.0, 0.0)
ultratech_df['Position'] = ultratech_df['Signal'].diff()
# display first few rows
ultratech_df.head()

plt.figure(figsize = (20,10))
# plot close price, short-term and long-term moving averages 
ultratech_df['Close Price'].plot(color = 'k', label= 'Close Price') 
ultratech_df['20_SMA'].plot(color = 'b',label = '20-day SMA') 
ultratech_df['50_SMA'].plot(color = 'g', label = '50-day SMA')
# plot ‘buy’ signals
plt.plot(ultratech_df[ultratech_df['Position'] == 1].index, 
         ultratech_df['20_SMA'][ultratech_df['Position'] == 1], 
         '^', markersize = 15, color = 'g', label = 'buy')
# plot ‘sell’ signals
plt.plot(ultratech_df[ultratech_df['Position'] == -1].index, 
         ultratech_df['20_SMA'][ultratech_df['Position'] == -1], 
         'v', markersize = 15, color = 'r', label = 'sell')
plt.ylabel('Price in Rupees', fontsize = 15 )
plt.xlabel('Date', fontsize = 15 )
plt.title('ULTRACEMCO', fontsize = 20)
plt.legend()
plt.grid()
plt.show()
'''