import pandas as pd
import glob

# Class to process the data
class EqData:
    __slots__ = '_combined_data', 'start_date', 'end_date'
    
    def __init__(self, folder_path, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        # List all the .csv file in the folder
        file_list = glob.glob(folder_path + '*.csv')
           
        # Create a list to hold the dataframes
        dfs = []

        # Read every csv file as DataFrame and add it to the list (dfs)
        for filename in file_list:
            dfs.append(self.__open_eq_file(filename))

        # Combine the all the DataFrame in the list
        combined_df = pd.concat(dfs)

        # Rename the column from Orgin date to Origin date
        combined_df = combined_df.rename(columns={'Orgin date': 'Origin date'})
        
        # Convert the 'Origin date' and 'Date' columns to datetime format,
        # convert the 'Magnitude' columns to numeric format,
        # so that the data will be plotted properly
        combined_df['Origin date'] = pd.to_datetime(combined_df['Origin date'])
        combined_df['Magnitude'] = pd.to_numeric(combined_df['Magnitude'])
        combined_df['Date'] = pd.to_datetime(combined_df['Origin date'].dt.date)

        # Extract the year and month from the date
        combined_df['Year'] = combined_df['Date'].dt.year
        combined_df['Month'] = combined_df['Date'].dt.month

        # Sort the data
        combined_df = combined_df.sort_values(by=['Origin date'])

        # Filter the data
        combined_df = combined_df[(combined_df['Date']>=start_date) & (combined_df['Date']<=end_date)] 

        self._combined_data = combined_df

    # Helper function to extract the data to DataFrame
    def __open_eq_file(self, filename):
        # Read the csv into DataFrame
        df = pd.read_csv(filename, header=None, names=[
            'No.',
            'Orgin date',
            'Longitude(E)',
            'Latitude(N)',
            'Magnitude',
            'Depth',
            'Location',
            'Location_details_1',
            'Location_details_2',
        ])

        # Delete the first row (column name)
        df = df.drop(index=0).reset_index(drop=True)
        return df
    
    @property
    def combined_data(self):
        return self._combined_data
