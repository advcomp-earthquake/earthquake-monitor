import datetime
import glob
from plot_data import PlotData
import data_process
from pandas import read_csv, DataFrame

# get user input - tkinter
date_df = read_csv("C:\\Users\\HP\\Documents\\earthquake-monitor\\final\\final_data\\date.csv")

start_year = date_df.loc[0, 'start_year']
start_month = date_df.loc[0, 'start_month']
start_day = date_df.loc[0, 'start_day']

end_year = date_df.loc[0, 'end_year']
end_month = date_df.loc[0, 'end_month']
end_day = date_df.loc[0, 'end_day']

start_date = datetime.datetime(start_year, start_month, start_day)
end_date = datetime.datetime(end_year, end_month, end_day)

# processing the data - pandas
folder_path = 'test_data/'
earthquake_data_df = data_process.preprocess_data('test_data/', start_date, end_date)

# plot the data - matplotlib & flask
plot_data = PlotData(earthquake_data_df,start_date,end_date)
plot_data.run()