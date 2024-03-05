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
fire_point_data_M_gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(firepoint_df.LONGITUDE, firepoint_df.LATITUDE), crs='EPSG:4617')

# Querying the data for the 'YEAR' and 'Sqr_Kilometers' fields
pipeline = [
    {"$match": {"YEAR": {"$gte": 1960, "$lte": 2021}}},
    {"$group": {"_id": "$YEAR", "total_sq_km": {"$sum": "$Sqr_Kilometers"}, "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]
results = list(collection.aggregate(pipeline))

#  data
data = {'Year': [1960, 1970, 1980, 1990, 2000, 2010, 2020],
        'Total Sq Km': [100, 150, 130, 170, 200, 180, 190],
        'Count of Fires': [50, 60, 55, 70, 80, 75, 85]}
df = pd.DataFrame(data)

#  data for protection zones
data_protzone = {'_id': ['Inside Protection Zones', 'Outside Protection Zones'],
                 'fire_count': [100, 150]}  # Example fire counts inside and outside protection zones
df_protzone = pd.DataFrame(data_protzone)

# Creating the bar chart
fig = go.Figure()
fig.add_trace(go.Bar(x=df['Year'], y=df['Total Sq Km'], name='Total Sq Km Burned', marker_color='blue', opacity=0.5))

# Creating the line chart
fig.add_trace(go.Scatter(x=df['Year'], y=df['Count of Fires'], name='Count of Fires', mode='lines+markers', yaxis='y2', marker=dict(color='red')))

# Update layout
fig.update_layout(title='Wildfire Data Analysis',
                  xaxis_title='Year',
                  yaxis_title='Square Kilometers Burned',
                  yaxis2=dict(title='Count of Fires', overlaying='y', side='right', showgrid=False, showline=True, linecolor='red'),
                  barmode='group')

# Print the column names
print(df.columns)

# Create the area chart
fig.add_trace(go.Scatter(x=df['Year'], y=df['Total Sq Km'], fill='tozeroy', name='Cumulative Sq Km Burned'))

# Creating a comparison chart for Protection Zones
fig.add_trace(go.Bar(name='Inside Protection Zones', x=df_protzone['_id'], y=df_protzone['fire_count']))

# Create a seasonal scatter plot
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
fire_counts = [150, 200, 180, 120]  # Example counts of fires per season
fig.add_trace(go.Scatter(x=seasons, y=fire_counts, mode='markers', name='Seasonal Fires', marker_color='skyblue'))


# Pie chart
# Aggregate data to get total size burned for each cause
pipeline_pie = [
    {"$group": {
        "_id": "$CAUSE",
        "total_size_ha": {"$sum": "$SIZE_HA"}
    }},
    {"$sort": {"total_size_ha": -1}}
]

results_pie = list(collection.aggregate(pipeline_pie))

# Convert results to a DataFrame
df_pie = pd.DataFrame(results_pie)

# Map causes to more readable labels
df_pie["_id"] = df_pie["_id"].map({
    "H": "Human",
    "H-PB": "Human (Prescribed)",
    "L": "Lightning",
    "U": "Unknown",
    "n/a": "Not Available"
})

# Create a pie chart
fig_pie = px.pie(df_pie, values='total_size_ha', names='_id', title='Distribution of Wildfire Causes (1960-2021)')

# Print the HTML code for the pie chart
print(fig_pie.to_html(include_plotlyjs='cdn'))

# Print the HTML code for the plots
print(fig.to_html(include_plotlyjs='cdn'))
