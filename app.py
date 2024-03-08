from flask import Flask, render_template, jsonify
from FireVSCode import process_data, generate_plots

app = Flask(__name__)

@app.route('/')
def index():
    # Process data and generate plots
    data = process_data()
    plot_html = generate_plots(data)

    return render_template('index.html', plot=plot_html)

@app.route('/data/<year>')
def get_data(year):
    # Process data for the selected year (you need to implement this logic)
    # Sample response data for testing
    response_data = {
        'years': [1960, 1970, 1980, 1990, 2000, 2010, 2020],
        'total_sq_km': [150, 200, 180, 190, 210, 220, 230],
        'count_of_fires': [60, 70, 75, 85, 90, 95, 100],
        'causes_values': [30, 40, 25, 25],
        'causes_labels': ['Human (H)', 'Human with Power Line (H-PH)', 'Unknown (U)', 'Lightning (L)']
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)