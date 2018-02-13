# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:44:38 2018

@author: user
"""

import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime as dt
from config import CLIENT_ID, CLIENT_SECRET


#Establish connection to Fitbit API
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


def get_heart_rate(auth2_client, date, granularity='1sec'):
    """
    Query intraday time series given date
    granularity: 1sec or 1min
    """
    
    heart_rate_raw = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level=granularity)

    time_list = []
    val_list = []
    date_list = []
    
    for i in heart_rate_raw['activities-heart-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
        date_list.append(date)
    
    heart_rate_df = pd.DataFrame({'Date': date_list,'Heart Rate':val_list,'Time':time_list})
    heart_rate_df['Timestamp'] = pd.to_datetime(heart_rate_df['Date'] + ' ' + heart_rate_df['Time'])
    heart_rate_df = heart_rate_df[['Timestamp','Heart Rate']]
    
    return heart_rate_df


START_DATE = '2018-01-20'
END_DATE = '2018-02-13'  
DATES = pd.date_range(start=START_DATE, end=END_DATE).tolist()
DATES = [date.strftime('%Y-%m-%d') for date in DATES]
    
heart_rate_dfs = []
for date in DATES:
    heart_rate_dfs.append(get_heart_rate(auth2_client, date))

#Concatenate individual heart_rate_dfs for each date into one big df
heart_rate_df = pd.concat(heart_rate_dfs, axis=0, ignore_index=True)

#Label each reading as 0 (not on date) or 1 (on date)
DATE_RANGES = pd.read_csv('./data/date_times.csv')
DATE_RANGES['Start'] = pd.to_datetime(DATE_RANGES['Start'])
DATE_RANGES['End'] = pd.to_datetime(DATE_RANGES['End'])

heart_rate_df['onDate?'] = 0
for i in range(len(DATE_RANGES)):
    start = pd.to_datetime(DATE_RANGES['Start'][i])
    end = pd.to_datetime(DATE_RANGES['End'][i])
    
    mask = (pd.to_datetime(heart_rate_df['Timestamp']) >= start) & (pd.to_datetime(heart_rate_df['Timestamp']) <= end)
    heart_rate_df['onDate?'] = heart_rate_df['onDate?'].where(~mask, other=1)

#Save to CSV
FILEPATH = './data/' + 'heart_rate ' + START_DATE + ' to ' + END_DATE + '.csv'
heart_rate_df.to_csv(FILEPATH, index=False)