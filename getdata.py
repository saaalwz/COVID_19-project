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



def GET_csse_covid_19_time_series():
    
    print('loading CSSE COVID_19 TimeSeries...')
    path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'
    
    ts_confirmed_us = pd.read_csv(path + 'confirmed_US.csv')
    ts_confirmed_global = pd.read_csv(path + 'confirmed_global.csv')
    ts_deaths_us = pd.read_csv(path + 'deaths_US.csv')
    ts_deaths_global = pd.read_csv(path + 'deaths_global.csv')
    ts_recovered_global = pd.read_csv(path + 'recovered_global.csv')
    
    print('done')
    return ts_confirmed_us, ts_confirmed_global, ts_deaths_us, ts_deaths_global, ts_recovered_global


def GET_csse_covid_19_daily_reports():
    
    print('loading CSSE COVID_19 daily report...')
    
    #extract the latest date from time series from its last column and convert to M-D-Y format
    ts_confirmed_us = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
    latest = pd.to_datetime(ts_confirmed_us.columns[-1]).strftime('%m-%d-%Y')
    
    #the previous day from the latest date it the second last column
    previous = pd.to_datetime(ts_confirmed_us.columns[-2]).strftime('%m-%d-%Y')
    
    #use date to fetch the report of the exact day
    report_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports'
    
    latest_data_global = pd.read_csv(report_path+f'/{latest}.csv')
    prev_data_global = pd.read_csv(report_path+f'/{previous}.csv')
    latest_data_us = pd.read_csv(report_path+f'_us/{latest}.csv')
    prev_data_us = pd.read_csv(report_path+f'_us/{previous}.csv')
    
    print('done')
    return latest_data_global, prev_data_global, latest_data_us, prev_data_us
        



def GET_shanghai_data(plot = True, encoding = "UTF-8"):

    '''
    plot：是否画图，默认是否
    '''
    import re
    print('laoding and processing Shanghai COVID-19 data...')
    url = f'https://raw.githubusercontent.com/saaalwz/shanghai_covid_data/main/ts_shanghai_covid.csv'
    data = pd.read_csv(url,encoding = encoding)['detail']
    print('done')

    data = data[data.apply(lambda x: x.startswith('上海202'))].sort_values()
    data = data.apply(lambda x: re.sub(r'\（.*?\）', '', x))  # 取数字
    data = data.apply(lambda x: x.replace('无新增','0'))

    df_all = pd.DataFrame(map(np.ravel,data.apply(lambda x: re.findall(r"\d+",x)))).rename({
        0:'年',
        1:'月',
        2:'日',
        3:'新增本土确诊',
        4:'新增本土无症状'
    },axis=1).iloc[:,:5]
    df_all['日期'] = df_all['年'].map(str)+"/"+df_all['月'].map(str)+"/"+df_all['日'].map(str)
    df_all['日期'] = pd.to_datetime(df_all['日期'])

    df_all = df_all.set_index('日期').sort_index()
    df_all = df_all.astype('int32')
    df = df_all.iloc[:,3:5]

    if plot:
        fig, axes = plt.subplots(nrows=2, ncols=1,figsize = [10,5*2])
        df_2022 = df[df.index>'2022-01-01']
        for col,ax in zip(df_2022.columns,axes):
            ax.step(df_2022.index, df_2022[col], color = '#202124',linewidth = 2)
            ax.bar(df_2022.index, df_2022[col],alpha = .8)
            ax.vlines(x=pd.to_datetime("2022-04-01"), ymin=0, ymax=df[col].max(), linewidth=2, color = '#4b7ffc', linestyle = '--')
            ax.vlines(x=pd.to_datetime("2022-06-01"), ymin=0, ymax=df[col].max(), linewidth=2, color = '#4b7ffc', linestyle = '--')

            ax.hlines(y=df[col].max(), xmin=df_2022.index[0], xmax=df_2022.index[-1], linewidth=1, color = '#ff0000')
            ax.text(x = df_2022.index[0], s=df[col].max(),y = df[col].max(), color = 'black', fontsize = 14)
            ax.text(x = df_2022.index[0], s=f"max：date：{str(df.index[df[col].argmax()])} \nincreasement：{df[col].max()}",y = df[col].max()/2, color = '#ff0000', fontsize = 18)
            ax.text(x = df_2022.index[0], s=f"today：date：{str(df.index[-1])} \nincreasement：{df[col][-1]}",y = df[col].max()/4, color = '#ff0000', fontsize = 18)

            ax.text(x = pd.to_datetime("2022-03-15"), s="2022-4-1",y = df[col].max()*2/3, color = 'black', fontsize = 12)
            ax.text(x = pd.to_datetime("2022-05-15"), s="2022-6-1",y = df[col].max()*2/3, color = 'black', fontsize = 12)

            ax.set_xlabel('date')
            ax.set_ylabel(f'{col}increasement')
            ax.set_title(f'{col}time series plot',fontsize = 16)

        plt.tight_layout()
    plt.rcParams['font.family'] = 'Heiti TC'

    return df

    