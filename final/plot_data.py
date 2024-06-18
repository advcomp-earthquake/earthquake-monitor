import base64
from io import BytesIO

from flask import Flask, render_template

from matplotlib.figure import Figure
import pandas as pd

class PlotData:
    __slots__ = '_df', '_start_date', '_end_date',
    _title_size = 30
    _ticks_axis_size = 18

    def __init__(self, df, start_date, end_date):
        self._df = df
        self._start_date = start_date
        self._end_date = end_date

    def plot_figures(
        self,
        fig_title,
        x, 
        y, 
        title_size, 
        ticks_axis_size,
        plot_type = 'line',
        plot_dict=None, 
    ):
        # Generate the figure **without using pyplot**.
        fig = Figure(figsize=(15, 6))
        ax = fig.subplots()
        if(plot_type == 'dot'):
            ax.plot(
                x,
                y, 
                'o', 
                markersize=5
            )
        else:
            ax.plot(
                x,
                y,
            )
        
        ax.tick_params('x', labelsize=ticks_axis_size, labelrotation=22)
        ax.tick_params('y', labelsize=ticks_axis_size)

        
        ax.set_title(fig_title, fontsize=title_size)
        ax.set_xlabel('Date', fontsize=ticks_axis_size)
        ax.set_ylabel('Magnitude', fontsize=ticks_axis_size)

        fig.tight_layout()

        return fig
    
    def run(self):
        # create flask app
        app = Flask(__name__)

        @app.route("/")
        def home():
            # Generate the figure **without using pyplot**.
            title = 'Earthquake Magnitude Over Time'

            fig = self.plot_figures(
                title,
                self._df['Origin date'], 
                self._df['Magnitude'], 
                self._title_size,
                self._ticks_axis_size,
                'dot',
                {
                    'marker':'o', 
                    'markersize':5
                }
            )
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return render_template(
                'plot_page.html', 
                title=title, 
                image=data, 
                start_date=self._start_date, 
                end_date=self._end_date
            )

        @app.route("/max-per-day")
        def max_per_day():
            # Group the data by date and find the maximum magnitude for each date
            max_magnitude_per_day = self._df.groupby('Date')['Magnitude'].max()

            # Print the date and the highest magnitude for each day
            max_magnitude_per_day = pd.DataFrame(max_magnitude_per_day)
            max_magnitude_per_day

            full_date_range = pd.date_range(
                start=max_magnitude_per_day.index.min(), 
                end=max_magnitude_per_day.index.max()
            )
            max_magnitude_per_day = max_magnitude_per_day.reindex(full_date_range)
            max_magnitude_per_day
            max_magnitude_per_day['Magnitude'] = max_magnitude_per_day['Magnitude'].fillna(0)

            max_magnitude_per_day.reset_index(inplace=True)
            max_magnitude_per_day.head(100)

            # Generate the figure **without using pyplot**.
            title = 'Highest Earthquake Magnitude per Day Over Time'

            fig = self.plot_figures(
                title,
                max_magnitude_per_day['index'], 
                max_magnitude_per_day['Magnitude'],
                self._title_size,
                self._ticks_axis_size,
                'line',
            )
            # Save it to a temporary buffer.
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return render_template(
                'plot_page.html', 
                title=title, 
                image=data, 
                start_date=self._start_date.date(), 
                end_date=self._end_date.date()
            )

        app.run(debug=True)




