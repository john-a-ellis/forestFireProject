import pymongo
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import geopandas as gpd
import requests
from matplotlib import pyplot as plt
import imageio.v2 as imageio
import pymongo


# Connecting to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["forestFireProject_db"]
collection = db["ForestFirePoints"]
cursor = collection.find()
data = list(cursor)
firepoint_df = pd.DataFrame(data)
fire_point_data_M_gdf = gpd.GeoDataFrame(data,geometry=gpd.points_from_xy(firepoint_df.LONGITUDE, firepoint_df.LATITUDE),crs='EPSG:4617')

# Querying the data for the 'YEAR' and 'Sqr_Kilometers' fields
pipeline = [
    {"$match": {"YEAR": {"$gte": 1960, "$lte": 2021}}},
    {"$group": {"_id": "$YEAR", "total_sq_km": {"$sum": "$Sqr_Kilometers"}, "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]
results = list(collection.aggregate(pipeline))

# Sample data
data = {'Year': [1960, 1970, 1980, 1990, 2000, 2010, 2020],
        'Total Sq Km': [100, 150, 130, 170, 200, 180, 190],
        'Count of Fires': [50, 60, 55, 70, 80, 75, 85]}
df = pd.DataFrame(data)

# Sample data for protection zones
data_protzone = {'_id': ['Inside Protection Zones', 'Outside Protection Zones'],
                 'fire_count': [100, 150]}  # Example fire counts inside and outside protection zones
df_protzone = pd.DataFrame(data_protzone)

# Creating the bar chart
fig = go.Figure()
fig.add_trace(go.Bar(x=df['Year'], y=df['Total Sq Km'], name='Total Sq Km Burned', marker_color='blue', opacity=0.5))

# Creating the line chart
fig.add_trace(go.Scatter(x=df['Year'], y=df['Count of Fires'], name='Count of Fires', mode='lines+markers', yaxis='y2', marker=dict(color='red')))

# Create a pie chart
causes = ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
counts = [25, 35, 20, 20]
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
fig.add_trace(go.Pie(labels=causes, values=counts, name='Primary Causes of Wildfires', marker=dict(colors=colors)))

# Create the area chart
fig.add_trace(go.Scatter(x=df['Year'], y=df['Total Sq Km'], fill='tozeroy', name='Cumulative Sq Km Burned'))

# Creating a comparison chart for Protection Zones
fig.add_trace(go.Bar(name='Inside Protection Zones', x=df_protzone['_id'], y=df_protzone['fire_count']))

# Create a seasonal scatter plot
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
fire_counts = [150, 200, 180, 120]  # Example counts of fires per season
fig.add_trace(go.Scatter(x=seasons, y=fire_counts, mode='markers', name='Seasonal Fires', marker_color='skyblue'))


# Creating a line chart for top 5 and bottom 5 years
def create_top_bottom_line_chart(top_5_years, bottom_5_years):
    # Create traces for line plot
    trace_top = go.Scatter(
        x=top_5_years['YEAR'],
        y=top_5_years['Fire_Counts'],
        name='Top 5 Years',
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(color='blue', size=8)
    )

    trace_bottom = go.Scatter(
        x=bottom_5_years['YEAR'],
        y=bottom_5_years['Fire_Counts'],
        name='Bottom 5 Years',
        mode='lines+markers',
        line=dict(color='orange', width=2),
        marker=dict(color='orange', size=8)
    )
    
    # Create layout
    layout = go.Layout(
        title='Line Graph of Fire Counts for Top 5 and Bottom 5 Years',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Fire Counts'),
        showlegend=True
    )

    # Create figure
    fig = go.Figure(data=[trace_top, trace_bottom], layout=layout)

    return fig

# Usage example
top_5_years_data = {'YEAR': [2010, 2011, 2012, 2013, 2014], 'Fire_Counts': [500, 600, 700, 800, 900]}
bottom_5_years_data = {'YEAR': [1960, 1961, 1962, 1963, 1964], 'Fire_Counts': [100, 200, 300, 400, 500]}

top_5_years_df = pd.DataFrame(top_5_years_data)
bottom_5_years_df = pd.DataFrame(bottom_5_years_data)

# Create the line chart
line_chart = create_top_bottom_line_chart(top_5_years_df, bottom_5_years_df)



#weather data




# Update layout
fig.update_layout(title='Wildfire Data Analysis',
                  xaxis_title='Year',
                  yaxis_title='Square Kilometers Burned',
                  yaxis2=dict(title='Count of Fires', overlaying='y', side='right', showgrid=False, showline=True, linecolor='red'),
                  barmode='group')



# Print the column names
print(df.columns)

# Print the HTML code for the plots
print(fig.to_html(include_plotlyjs='cdn'))