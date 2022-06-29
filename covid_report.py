from getdata import GET_csse_covid_19_daily_reports, GET_csse_covid_19_time_series, GET_shanghai_data
from data_processing import ts_process_US, ts_process_CHINA, daily_process
from covid_visualization import negincre_report, dataQC, plot_ts_trend, Decompose_CHINA, Decompose_US

# get data
latest_data_global,prev_data_global,latest_data_us,prev_data_us = GET_csse_covid_19_daily_reports()
ts_confirmed_us,ts_confirmed_global,ts_deaths_us,ts_deaths_global,ts_recovered_global = GET_csse_covid_19_time_series()
ts_shanghai_covid = GET_shanghai_data(plot = True) 


# data processing
ts_confirmed_CHINA_incre, loc_data_CHINA, sorted_provinces = ts_process_CHINA(ts_confirmed_global,clip=False)
ts_deaths_CHINA_incre, _, _ = ts_process_CHINA(ts_deaths_global,clip=False)
ts_recovered_CHINA_incre, _, _ = ts_process_CHINA(ts_recovered_global,clip=False)

ts_confirmed_US_incre,loc_data_us,sorted_state = ts_process_US(ts_confirmed_us,clip=False)
ts_deaths_US_incre,_,_,population = ts_process_US(ts_deaths_us,death = True,clip=False)

latest_data_CHINA = daily_process(latest_data_global, country = 'China')
prev_data_CHINA = daily_process(prev_data_global, country = 'China')
latest_data_US = daily_process(latest_data_us, country = 'US')
prev_data_US = daily_process(prev_data_us, country = 'US')


# visualization
Decompose_US(
    ts_confirmed_US_incre,
    latest_data_US,
    prev_data_US,
    start='2020-03-01',
    end='2022-06-01',
    ma = [7,30],
    method = '新增',             # method = '累计'
    specify = 'California',        # specify = 'Shanghai' specify = 'All' specify = None
    verbose = 1,
    kind = '确诊'
)

Decompose_US(
    ts_deaths_US_incre,
    latest_data_US,
    prev_data_US,
    start='2020-03-01',
    end='2022-06-01',
    ma = [7,30],
    method = '新增',             # method = '累计'
    specify = 'California',        # specify = 'Shanghai' specify = 'All' specify = None
    verbose = 1,
    kind = '死亡'
)


Decompose_CHINA(
    ts_confirmed_CHINA_incre,
    latest_data_CHINA,
    prev_data_CHINA,
    start='2020-03-01',
    end='2022-06-01',
    ma = [7,30],
    method = '新增',              # method = '累计'
    specify = 'Shanghai',         # specify = 'Shanghai' specify = 'All' specify = None
    verbose = 1,
    kind = '确诊'
)
