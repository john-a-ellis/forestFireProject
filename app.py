import plotly.express as px
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    # Process data and generate plots
    data = process_data()
    plot_html = generate_plots(data)

    return render_template('index.html', plot=plot_html)
@app.route('/data<year')
def get_data(year):

    response_data = {
        'YEAR': [1995, 1979, 2014],
        'SIZE_HA': [1050000.0, 857600.0, 632984.1]
}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
