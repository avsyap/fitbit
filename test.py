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
    
    return heart_rate_df

START_DATE = '2018-01-20'
END_DATE = '2018-01-31'  
DATES = pd.date_range(start=START_DATE, end=END_DATE).tolist()
DATES = [date.strftime('%Y-%m-%d') for date in DATES]
    
heart_rate_dfs = []
for date in DATES:
    heart_rate_dfs.append(get_heart_rate(auth2_client, date))

heart_rate_df = pd.concat(heart_rate_dfs, axis=0, ignore_index=True)
FILEPATH = './data/' + 'heart_rate ' + START_DATE + ' to ' + END_DATE + '.csv'
heart_rate_df.to_csv(FILEPATH, index=False)