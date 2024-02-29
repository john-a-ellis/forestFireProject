from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # Sample data for the bar and line charts
    data = {'Year': [1960, 1970, 1980, 1990, 2000, 2010, 2020],
            'Total Sq Km': [100, 150, 130, 170, 200, 180, 190],
            'Count of Fires': [50, 60, 55, 70, 80, 75, 85]}
    df = pd.DataFrame(data)

    # Creating the bar chart
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df['Year'], y=df['Total Sq Km'], name='Total Sq Km Burned', marker_color='blue', opacity=0.5))

    # Creating the line chart
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=df['Year'], y=df['Count of Fires'], name='Count of Fires', mode='lines+markers', yaxis='y2', marker=dict(color='red')))

    # Update layout for the line chart
    fig_line.update_layout(yaxis2=dict(title='Count of Fires', overlaying='y', side='right', showgrid=False, showline=True, linecolor='red'),
                           barmode='group')

    # Convert the bar and line plots to HTML
    plot_html_bar = fig_bar.to_html(include_plotlyjs='cdn')
    plot_html_line = fig_line.to_html(include_plotlyjs='cdn')

    # Sample data for the heatmap
    np.random.seed(0)
    data_heatmap = np.random.rand(10, 10)

    # Creating the heatmap
    fig_heatmap = go.Figure()
    fig_heatmap.add_trace(go.Heatmap(z=data_heatmap, colorscale='Viridis'))

    # Convert the heatmap plot to HTML
    plot_html_heatmap = fig_heatmap.to_html(include_plotlyjs='cdn')

    # Sample data for the pie chart
    causes = ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
    counts = [25, 35, 20, 20]

    # Creating the pie chart
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=causes, values=counts, textinfo='percent+label', insidetextorientation='radial'))

    # Convert the pie chart to HTML
    plot_html_pie = fig_pie.to_html(include_plotlyjs='cdn')

    # Render the template with all the plots
    # Render the template with all the plots
return render_template('index.html', plot_bar=plot_html_bar, plot_line=plot_html_line, plot_heatmap=plot_html_heatmap, plot_pie=plot_html_pie)


if __name__ == '__main__':
    app.run(debug=True)
