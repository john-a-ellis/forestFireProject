from flask import Flask, render_template, jsonify, send_file, request
# from ForestFireVSCode import process_data, generate_plots
from FireWithWeather_Viz import make_weather_and_fire_animation
import datetime

app = Flask(__name__)

# @app.route('/')
# def index():
#     # Process data and generate plots
#     data = process_data()
#     plot_html = generate_plots(data)

#     return render_template('index.html', plot=plot_html)

# @app.route('/data/<year>')
# def get_data(year):
#     # Process data for the selected year (you need to implement this logic)
#     # Sample response data for testing
#     response_data = {
#         'years': [1960, 1970, 1980, 1990, 2000, 2010, 2020],
#         'total_sq_km': [150, 200, 180, 190, 210, 220, 230],
#         'count_of_fires': [60, 70, 75, 85, 90, 95, 100],
#         'causes_values': [30, 40, 25, 25],
#         'causes_labels': ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
#     }
#     return jsonify(response_data)

"""
Create a new route to generate a weather/fire animation.
Accepts a start and end date in the form YYYY-MM-DD.
"""
@app.get("/data/weather-animation")
def get_weather_animation():
    start_date_param = request.args.get("startdate")
    end_date_param = request.args.get("enddate")

    start_date = datetime.datetime.strptime(start_date_param, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_param, "%Y-%m-%d")

    make_weather_and_fire_animation(start_date, end_date)
    
    return send_file("resources/animation.gif", mimetype="image/animation")

if __name__ == '__main__':
    app.run(debug=True)
