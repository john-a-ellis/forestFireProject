from flask import Flask, render_template
from ForestFireVSCode import process_data, generate_plots

app = Flask(__name__)

@app.route('/')
def index():
    # Process data and generate plots
    data = process_data()
    plot_html = generate_plots(data)

    return render_template('index.html', plot=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
