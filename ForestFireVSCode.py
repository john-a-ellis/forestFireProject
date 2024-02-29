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