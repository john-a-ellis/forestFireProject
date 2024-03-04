import datetime
import geopandas as gpd
import pandas as pd
import requests
from matplotlib import pyplot as plt
import imageio.v2 as imageio
import pymongo

# Connecting to the MongoDB database (i.e. loading the Fire_Point dataset through MongoDB into a variable)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["forestFireProject_db"]
collection = db["ForestFirePoints"]
cursor = collection.find()
data = list(cursor)
firepoint_df = pd.DataFrame(data)
fire_point_data_M_gdf = gpd.GeoDataFrame(data,geometry=gpd.points_from_xy(firepoint_df.LONGITUDE, firepoint_df.LATITUDE),crs='EPSG:4617')

def get_weather_for_day(date: datetime.datetime) -> gpd.GeoDataFrame:
  """
  Load weather data from all stations for a single day.
  """
    # Obtaining weather data through weather APIs 
  WEATHER_API_BASE = "https://api.weather.gc.ca"
  API = f"{WEATHER_API_BASE}/collections/climate-daily/items"

  date_start = date.__format__("%Y-%m-%d 00:00:00")
  date_end = date.__format__("%Y-%m-%d 11:59:59")

  result = requests.get(API, params={
    "datetime": f"{date_start}/{date_end}",
    "f": "json",
    "startindex": "0",
    "sortby": "LOCAL_YEAR,LOCAL_DAY",
    "limit": "5000"
  })

  data = result.json()
  features = data["features"]
  weather_df = gpd.GeoDataFrame.from_features(features)

  return weather_df

def get_fires_for_day(date: datetime.datetime) -> pd.DataFrame:
  """
  Get a subset of the fire points data for a single day.
  """
  df = fire_point_data_M_gdf[(fire_point_data_M_gdf["YEAR"] == date.year) & (fire_point_data_M_gdf["MONTH"] == date.month) & (fire_point_data_M_gdf["DAY"] == date.day)]
  return df

def make_weather_and_fire_animation(start_date, end_date):
  """
  Make an animation of weather and fire data over a range of dates.
  """
  images = []
  # Iterate through days in range.
  for i, date in enumerate(pd.date_range(start_date, end_date)):
    print(f"Processing date: {date}")

    weather_for_day_df = get_weather_for_day(date)
    fires_for_date_df = get_fires_for_day(date)

    # Create a plot with all weather data color coded from blue-red (relative temperatures)
    # Overlay with the forest fires for that day, in black.
    fig, ax = plt.subplots()
    plt.title(f"Weather Data Overlaying Wildfire Points' Data \n{date}\n\nHigh Temperatures = Red markers; Cool Temperatures = Blue markers; \nWildfires = Black markers")
    plt.xlabel("Longitude")
    plt.ylabel('Latitude')
    weather_for_day_df.plot("MEAN_TEMPERATURE", cmap="coolwarm", ax=ax)
    ax.scatter(fires_for_date_df["LONGITUDE"], fires_for_date_df["LATITUDE"], color="black", s=10)
    
    # Save frame of animation to animations folder.
    image_path = f"./resources/animation/{i}.png"
    plt.savefig(image_path)
    image_buffer = imageio.imread(image_path)
    images.append(image_buffer)
    
    plt.close()

    imageio.mimsave('./resources/animation.gif',images, fps = 2)
