import pandas as pd
import numpy as np
from datetime import timedelta, datetime



# data visualization
import plotly.graph_objs as go
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

# change text color
import colorama
from colorama import Fore, Style

# IPython
from IPython.display import IFrame


#from getdata import GET_csse_covid_19_daily_reports,GET_csse_covid_19_time_series,GET_shanghai_data

# get data
#latest_data_global,prev_data_global,latest_data_us,prev_data_us = GET_csse_covid_19_daily_reports()
#ts_confirmed_us,ts_confirmed_global,ts_deaths_us,ts_deaths_global,ts_recovered_global = GET_csse_covid_19_time_series()
#ts_shanghai_covid = GET_shanghai_data(plot=False)  # 这里包含近10天的上海无症状新增趋势！


def ts_process_CHINA(china_data,clip = False):
    
    loc_data = china_data[['Province/State','Lat','Long']]
    loc_data = china_data[china_data['Province/State'] != 'Unknown']
    
    china_data = china_data[china_data['Country/Region'] == 'China']
    china_data = china_data.set_index('Province/State').drop(['Country/Region', 'Lat','Long'], axis = 1)
    
    if clip:
        china_data = china_data.diff(axis=1).fillna({china_data.columns[0]:china_data[china_data.columns[0]]},downcast = 'infer').clip(lower=0)
    else:
        china_data = china_data.diff(axis=1).fillna({china_data.columns[0]:china_data[china_data.columns[0]]},downcast = 'infer')
        
    china_data = china_data.sort_values(by = china_data.columns[-1],ascending=False)
    china_data = china_data.dropna().drop('Unknown').T
    china_data.index = pd.to_datetime(china_data.index)
    china_data.columns.name = ''
    
    sorted_provinces = china_data.columns
    
    return china_data, loc_data, sorted_provinces;


def ts_process_US(us_data, death = False, clip = False):
    
    loc_data = us_data[['UID','FIPS','Admin2','Province_State','Lat','Long_']]
    us_data = us_data.drop(['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Lat', 'Long_', 'Country_Region', 'Combined_Key'], axis = 1)
    us_data = us_data.groupby('Province_State').sum()
    
    if death:
        population = us_data['Population']
        us_data = us_data.drop('Population',axis=1)
    
    if clip:
        us_data = us_data.diff(axis = 1).fillna({us_data.columns[0]:us_data[us_data.columns[0]]}, downcast = 'infer').clip(lower = 0)
        
    else:
        us_data = us_data.diff(axis = 1).fillna({us_data.columns[0]:us_data[us_data.columns[0]]}, downcast = 'infer')
        
    us_data = us_data.dropna()
    us_data = us_data.sort_values(us_data.columns[-1], ascending = False).T
    us_data.index = pd.to_datetime(us_data.index)
    us_data.columns.name = ''
    
    sorted_state = us_data.columns
    
    if death:
        return us_data,loc_data,sorted_state,population
    return us_data, loc_data, sorted_state;


def daily_process(daily_data, country = 'China'):
    
    if country == 'China':
        daily_data = daily_data[daily_data['Country_Region'] == 'China']
        daily_data = daily_data.set_index(daily_data['Province_State']).drop('Unknown')
    
    elif country == 'US':
        daily_data = daily_data.set_index(daily_data['Province_State'])
        
    daily_data_processed = daily_data[['Province_State','Last_Update','Confirmed','Deaths','Incident_Rate','Case_Fatality_Ratio']]
    
    daily_data_processed.index.name = ''
    
    return daily_data_processed;



#ts_confirmed_CHINA_incre, loc_data_CHINA, sorted_provinces = ts_process_CHINA(ts_confirmed_global,clip=False)
#ts_deaths_CHINA_incre, _, _ = ts_process_CHINA(ts_deaths_global,clip=False)
#ts_recovered_CHINA_incre, _, _ = ts_process_CHINA(ts_recovered_global,clip=False)

#ts_confirmed_US_incre,loc_data_us,sorted_state = ts_process_US(ts_confirmed_us,clip=False)
#ts_deaths_US_incre,_,_,population = ts_process_US(ts_deaths_us,death = True,clip=False)

#latest_data_CHINA = daily_process(latest_data_global, country = 'China')
#prev_data_CHINA = daily_process(prev_data_global, country = 'China')
#latest_data_US = daily_process(latest_data_us, country = 'US')
#prev_data_US = daily_process(prev_data_us, country = 'US')

    