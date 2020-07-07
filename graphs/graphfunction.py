import pandas as pd
import glob, os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import date

'''The Graph class is the base class that the Bar and Line graphs inherit.'''
class Graph:
    def __init__(self,graphType):
        self.graphType = graphType
        self.title = self.getTitle()
        self.xAxis = 'date'
        self.yAxis = self.getYAxis()
        self.data = self.combineCSV()

    def getDataPath(self):
        return f'../data/{self.graphType}_logs/*'

    def combineCSV(self):
        files = sorted(glob.glob(f'../data/{self.graphType}_logs/*'))[-8:-1]
        return pd.concat(map(pd.read_csv, files))

    def getYAxis(self):
        return 'time_opened_seconds' if self.graphType == 'open' else 'temperature_celsius'

    def getTitle(self):
        return "Duration of Open Refrigerator" if self.graphType == 'open' else "Temperature of Refrigerator"

    # The saveImage function saves .png images of the fig objects
    def saveImage(self,fig):
        if not os.path.exists("../report/images"):
            os.mkdir("../report/images")
        fig.write_image(f"../report/images/{self.graphType}Graph_{date.today().strftime('%Y_%m_%d')}.png")

# The LineGraph class creates the LineGraph object
class LineGraph(Graph):

    ''' The addOpenIndicator function merges the temperature data and the open data
        to find the times that the refrigerator was open and its corresponding
        temperature fluctuations.
    '''
    def addOpenIndicator(self):
        open_data = BarChart('open').data

        '''Since the data only is written when the refrigerator is shut,
            we find the time the refrigerator opens but using the open duration
            to find the time the refrigerator was intially opened'''
        open_data['startRange'] = pd.to_datetime(open_data['date']) - pd.to_timedelta(open_data['time_opened_seconds'], unit='s')
        del open_data['time_opened_seconds']

        # Create columns that have the start range and end range when opened
        open_data.columns = ['endRange', 'startRange']
        open_data = open_data[['startRange', 'endRange']]
        open_data['endRange'] = pd.to_datetime(open_data['endRange'])

        self.data['date'] = pd.to_datetime(self.data['date'])
        date = self.data['date']

        '''Merge the newly created start/emd range dataframe to
            find temperature fluctuations during htat interval'''
        df = pd.merge(open_data.assign(A=1), date.to_frame().assign(A=1), on='A')
        df = df.query('startRange <= date < endRange')['date']
        tmp_df = pd.DataFrame({'date': df.values, 'opened': 1})

        merged_df = self.data.merge(tmp_df, on='date', how='left')
        final = merged_df.fillna(0)
        final['opened'] = final['opened'].astype(int)
        self.data = final
        return self

    # The splitData function splits the data by when the refrigerator was opened to easily plot in graphs
    def splitData(self):
        self.data['temp_closed'] = np.where(self.data['opened']==0,self.data['temperature_celsius'],np.nan)
        self.data['temp_open'] = np.where(self.data['opened']!=0,self.data['temperature_celsius'],np.nan)
        del self.data["temperature_celsius"]
        del self.data["opened"]
        return self

    def makeLineGraph(self):
        fig = go.Figure()

        '''This trace creates the blue line in the
        figure to represent that the refrigerator is closed'''
        fig.add_trace(go.Scatter(x=self.data['date'],y=self.data['temp_closed'],
                                 mode='lines',
                                 name='closed'
                                 ))

        '''This trace creates the red line in the
        figure to represent that the refrigerator is open'''
        fig.add_trace(go.Scatter(x=self.data['date'], y=self.data['temp_open'],
                                 mode='lines',
                                 name='opened'
                                 ))
        fig.update_layout(
            # Line Graph Title preferences
            title={
                'text': "Temperature Changes in Refrigerator",
                'y': .85,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',

            },
            # Font preferences
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),

            # Legend options
            legend=dict(
                x=.84,
                y=.97,
                bgcolor='rgba(0,0,0,0)',
                font=dict(
                    family="sans-serif",
                    size=10,
                    color="black"
                )),
            xaxis_title='Date',
            yaxis_title='Degrees (°C)'
        )
        return fig

# The BarGChart class creates the bar chart object
class BarChart(Graph):
    def convertDatetimeToDate(self):
        self.data['tmp_date'] = pd.to_datetime(self.data['date'])
        self.data['day'] = self.data['tmp_date'].dt.date
        del self.data['tmp_date']
        self.data = self.data[['day', 'time_opened_seconds']]
        self.xAxis = 'day'
        self.data["open_count"] = 1
        return self

    # The groupByDay function groups data by day to find accumulated time opened.
    def groupByDay(self):
        self.data = self.data.groupby("day", as_index=False).agg({'time_opened_seconds': sum, 'open_count': 'count'})
        return self

    # The convertSecondsToMinutes function converts the 'time_opened_minutes' minute attribute to seconds.
    def convertSecondsToMinutes(self):
        self.data['time_opened_minutes'] = self.data['time_opened_seconds'] // 60
        del self.data['time_opened_seconds']
        return self

    def makeBarChart(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # The Bars in the Bar Chart figure (left y axis)
        fig.add_trace(
            go.Bar(
                x=self.data['day'],
                y=self.data['time_opened_minutes'],
                name = 'Minutes opened'),
            secondary_y=False)

        # The Scatter plot (line graph) in the Bar Chart figure (right y axis)
        fig.add_trace(
            go.Scatter(
                x=self.data['day'],
                y=self.data['open_count'],
                name = 'Number of Times Opened'),
            secondary_y=True)

        fig.update_layout(
            # Bar Chart Title preferences
            title={
                'text': "Refrigerator Openings Usage",
                'y': .9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',

            },
            # Font preferences
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),

            # Legend options
            legend=dict(
                x=0,
                y=1.1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(
                    family="sans-serif",
                    size=10,
                    color="black"
                ),
            orientation="h"),
        # xaxis_tickformat='%d %B %Y'
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Date")

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Cummulative Time Opened</b> (Minutes)", secondary_y=False,ticks="outside",
                         tickwidth=2, tickcolor='blue', ticklen=10, col=1,
                         title_font=dict(size=14, family='sans-serif', color='blue'))
        fig.update_yaxes(title_text="<b>Occurences</b> opened", secondary_y=True,ticks="outside",
                         tickwidth=2, tickcolor='crimson', ticklen=10, col=1,
                         title_font=dict(size=14, family='sans-serif', color='crimson'))

        return fig


