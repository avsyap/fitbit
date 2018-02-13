# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:58:56 2018

@author: user
"""

import pandas as pd
from scipy.stats import ttest_ind


df = pd.read_csv('./data/heart_rate 2018-01-20 to 2018-02-13.csv')
df.set_index(pd.DatetimeIndex(df["Timestamp"]), inplace=True)
df = df.between_time("07:00","00:00")

no_date = df[df['onDate?'] == 0]['Heart Rate'].as_matrix()
date = df[df['onDate?'] == 1]['Heart Rate'].as_matrix()

t, p = ttest_ind(no_date, date, equal_var=False)
print(t)
print(p)