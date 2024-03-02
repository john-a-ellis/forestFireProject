import pymongo
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Connecting to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["forestFireProject_db"]
collection = db["ForestFirePoints"]

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

# Create a seasonal bar chart
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
fire_counts = [150, 200, 180, 120]  # Example counts of fires per season
fig.add_trace(go.Bar(x=seasons, y=fire_counts, name='Seasonal Fires', marker_color='skyblue'))


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
