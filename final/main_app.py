import datetime
from data_process import EqData
import glob
from plot_data import PlotData

# get user input - tkinter
start_year = 2024
start_month = 4
start_day = 26

end_year = 2024
end_month = 5
end_day = 26

start_date = datetime.datetime(start_year, start_month, start_day)
end_date = datetime.datetime(end_year, end_month, end_day)

# download the data - Selenium


# processing the data - pandas
folder_path = 'data/'
earthquake_data_df = EqData('data/', start_date, end_date)

# plot the data - matplotlib & flask
plot_data = PlotData(earthquake_data_df.combined_data,start_date,end_date)
plot_data.run()