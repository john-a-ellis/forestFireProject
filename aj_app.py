# Dependencies
from FireWithWeather_Viz import make_weather_and_fire_animation
from FireWithWater import genMap
import datetime
from flask import Flask, render_template, jsonify, send_file, request, url_for

app = Flask(__name__)
"""
Create a new route to generate a weather/fire animation.
Accepts a start and end date in the form YYYY-MM-DD.
"""
@app.get("/")
def index():
    return render_template('aj_index.html')
    
@app.get("/map")
def get_Map():
    date_param = request.args.get("date")
    breakDate = date_param.split("-")
    myYear = breakDate[0]
    myMonth= breakDate[1]
    myMap = genMap(myYear, myMonth)
    return myMap.get_root().render()


@app.get("/weather-animation")
def get_weather_animation():
    start_date_param = request.args.get("startdate")
    end_date_param = request.args.get("enddate")

    start_date = datetime.datetime.strptime(start_date_param, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_param, "%Y-%m-%d")
    breakDate = start_date_param.split("-")
    myYear = breakDate[0]
    myMonth= breakDate[1]
    
    make_weather_and_fire_animation(start_date, end_date)
    myMap = genMap(myYear, myMonth)
    myMap.save('static/FireWithWater.html')
    # render_template("FireWithWater.html")
    send_file("static/animation.gif", mimetype="image/animation")
    return render_template('aj_index.html')

if __name__ == '__main__':
    app.run(debug=True)
