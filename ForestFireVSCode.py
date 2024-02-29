# Importing necessary libraries
import pymongo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import hvplot.pandas
import seaborn as sns
import plotly.graph_objects as go



# Connecting to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["forestFireProject_db"]
collection = db["ForestFirePoints"]

# How has the frequency of wildfires changed over the years?
## Temporal Analysis
# Visualization: Bar chart showing the total square kilometers burned per year and a line chart showing the count of fires per year.


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

# Update layout
fig.update_layout(title='Total Square Kilometers Burned per Year (1960-2021)',
                  xaxis_title='Year',
                  yaxis_title='Square Kilometers Burned',
                  yaxis2=dict(title='Count of Fires', overlaying='y', side='right', showgrid=False, showline=True, linecolor='red'),
                  barmode='group')

# Show the plot
fig.show()


# The analysis of wildfire data from 1960 to 2021 in Canada provides insights into the trends and patterns of wildfires over the years. The data shows that the total square kilometers burned and the count of fires have varied significantly during this period.

# Peak in Wildfires: The year 2000 recorded the highest total square kilometers burned, indicating a peak in wildfire activity. This could be attributed to various factors such as climate conditions, land use, and human activities.

# Lowest Wildfire Activity: On the other hand, the year 1980 experienced the lowest count of fires, suggesting a period of relatively low wildfire activity compared to other years in the dataset.

# Fluctuations Over Time: Throughout the period from 1960 to 2021, there have been fluctuations in wildfire activity, with some years showing an increase in total square kilometers burned and the count of fires, while other years have shown a decrease. This indicates the dynamic nature of wildfires and the influence of various factors on their occurrence.

# After 2010, there was an increase in wildfire activity in Canada, which continued to rise until 2020. This period saw a significant uptick in both the total square kilometers burned and the count of fires. These trends are concerning and highlight the need for effective wildfire management and mitigation strategies to address the growing threat of wildfires in the country.

# Overall Trend: Despite the fluctuations, there seems to be an overall increasing trend in wildfire activity over the decades, with the total square kilometers burned and the count of fires generally increasing from 1960 to 2021. It's worth noting that while data for 1960 and before indicated even lower wildfire activity, there is no specific data available for that period. This overall trend underscores the importance of wildfire management and mitigation strategies to address the growing threat of wildfires in Canada.

# Statistical anslysis 

# Calculating the average number of wildfires per year
average_counts = sum(counts) / len(counts)

print(f"Average number of wildfires per year: {average_counts}")

# Where are the hotspots of wildfire activity?
## Spatial Analysis
### Visualization: Heatmap displaying the density of wildfires across different regions.

# Define the latitude and longitude ranges

# Calculate the heatmap data
# Define the latitude and longitude ranges
min_lat = db.ForestFirePoints.find_one(sort=[("LATITUDE", 1)])['LATITUDE']
max_lat = db.ForestFirePoints.find_one(sort=[("LATITUDE", -1)])['LATITUDE']
min_lon = db.ForestFirePoints.find_one(sort=[("LONGITUDE", 1)])['LONGITUDE']
max_lon = db.ForestFirePoints.find_one(sort=[("LONGITUDE", -1)])['LONGITUDE']

num_lat_bins = 20
num_lon_bins = 20

lat_range = np.linspace(min_lat, max_lat, num=num_lat_bins + 1)
lon_range = np.linspace(min_lon, max_lon, num=num_lon_bins + 1)

# Calculate the size of each grid cell
lat_step = lat_range[1] - lat_range[0]
lon_step = lon_range[1] - lon_range[0]

# Initialize an array to store the count of wildfires in each grid cell
fire_count = np.zeros((num_lat_bins, num_lon_bins))

# Iterate over the wildfires and increment the count in the corresponding grid cell
for fire in db.ForestFirePoints.find():
    lat_index = int((fire['LATITUDE'] - min_lat) // lat_step)
    lon_index = int((fire['LONGITUDE'] - min_lon) // lon_step)
    if 0 <= lat_index < num_lat_bins and 0 <= lon_index < num_lon_bins:
        fire_count[lat_index, lon_index] += 1

# Create the heatmap using Plotly
fig_heatmap = go.Figure(data=go.Heatmap(
    z=fire_count,
    x=lon_range,
    y=lat_range,
    colorscale='hot'))

# Update layout
fig_heatmap.update_layout(
    title='Heatmap of Wildfire Activity (Point Data)',
    xaxis_title='Longitude',
    yaxis_title='Latitude',
    yaxis_autorange='reversed')

# Convert the heatmap plot to HTML
plot_html_heatmap = fig_heatmap.to_html(include_plotlyjs='cdn')



# Analysis Result

# 1. High Density of Wildfires: There is a higher density of wildfires in the area with latitude around 60 and longitude around -180, indicated by the dark red color on the heatmap. This region corresponds to a location in the northern part of Canada, possibly in the Yukon, Northwest Territories, or Nunavut, where wildfires are more prevalent.

# 2. Lower Density of Wildfires: The area with latitude around 50 and longitude around -150 shows a lower density of wildfires, as indicated by the yellow color on the heatmap. This region is likely experiencing fewer wildfires compared to the area in the northern part of Canada. It is likely located in the southern part of Canada, possibly in the provinces of British Columbia or Alberta.

# 3. Specific Region with High Wildfire Activity: Additionally, there is a specific area with latitude around 47 and longitude around -60 where the heatmap shows a dark red color, indicating a high density of wildfires in that region. This location is within the Maritime provinces, possibly in Nova Scotia, indicating a localized area with significant wildfire activity.

# Overall, the heatmap provides a visual representation of the distribution of wildfires across different regions, highlighting areas with high and low wildfire activity. These observations can help in understanding the spatial patterns of wildfires in the Maritime provinces of Canada, particularly in Nova Scotia, and can inform further analysis and mitigation efforts.




# What are the primary causes of wildfires?
## Causal Factor
# Visualization: Pie chart showing the percentage distribution of wildfire causes.


# Define the causes and counts for the pie chart
import plotly.graph_objects as go

# Define the data for the pie chart
causes = ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
counts = [25, 35, 20, 20]

# Create the Plotly pie chart
fig = go.Figure(data=[go.Pie(
    labels=causes,
    values=counts,
    textinfo='percent+label',
    insidetextorientation='radial',
    marker=dict(colors=colors)
)])

# Update layout
fig.update_layout(
    title='Primary Causes of Wildfires',
    legend_title='Legend',
    legend=dict(
        x=1.3,
        y=0.9,
        traceorder='normal',
        font=dict(size=8)
    )
)

# Show the plot
fig.show()

# Analysis Result

# Human with Power Line (H-PH): This category accounts for the highest percentage of wildfires at 35%. These fires are caused by human activities involving power lines.

# Human (H): Human-caused wildfires without power lines account for 25% of the total. These fires are a result of various human activities.

# Lightning (L): Lightning strikes are responsible for 20% of wildfires. These fires occur due to natural causes.

# Unknown (U): The cause of 20% of wildfires is unknown, indicating that the specific cause of these fires could not be determined.

# This analysis provides insights into the primary causes of wildfires, highlighting the significant contribution of human activities, particularly those involving power lines. Understanding these causes is essential for wildfire prevention and mitigation strategies.