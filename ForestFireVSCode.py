import pymongo
import pandas as pd
import plotly.graph_objects as go

def process_data():
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
    return df

def generate_plots(data):
    # Creating the bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['Year'], y=data['Total Sq Km'], name='Total Sq Km Burned', marker_color='blue', opacity=0.5))

    # Creating the line chart
    fig.add_trace(go.Scatter(x=data['Year'], y=data['Count of Fires'], name='Count of Fires', mode='lines+markers', yaxis='y2', marker=dict(color='red')))

def generate_plots(data):
    # Creating the bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['Year'], y=data['Total Sq Km'], name='Total Sq Km Burned', marker_color='blue', opacity=0.5))

    # Creating the line chart
    fig.add_trace(go.Scatter(x=data['Year'], y=data['Count of Fires'], name='Count of Fires', mode='lines+markers', yaxis='y2', marker=dict(color='red')))

    # Create a pie chart
    causes = ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
    counts = [25, 35, 20, 20]
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    fig.add_trace(go.Pie(labels=causes, values=counts, name='Primary Causes of Wildfires', marker=dict(colors=colors)))

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

    # Return the HTML representation of the plot
    return fig.to_html(include_plotlyjs='cdn')

if __name__ == '__main__':
    data = process_data()
    plot_html = generate_plots(data)
    print(plot_html)


if __name__ == '__main__':
    data = process_data()
    print(data.columns)  # Print the column names
    plot_html = generate_plots(data)
    print(plot_html)
