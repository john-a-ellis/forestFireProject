#!/usr/bin/env python
# coding: utf-8

# importing depedencies
import pandas as pd
import geopandas as gpd
import folium
import json
import vincent
from altair import Chart
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime
from folium.plugins import HeatMap

# Create an instance of MongoClient
mongo = MongoClient(port=27017)

db = mongo['forestFireProject_db']

def genMap(mapYear, mapMonth):
    myMonth = int(mapMonth)
    myYear = int(mapYear)
    # import data

    #set some data variables for filtering
    # myMonth = 8
    # myYear = 2018
    WaterfromDate = datetime(myYear-1, myMonth + 1, 1)
    WaterfromDate=WaterfromDate.strftime('%Y-%m-%d')
    WatertoDate = datetime(myYear+1, myMonth,1)
    WatertoDate=WatertoDate.strftime('%Y-%m-%d %H:%M')

    FirefromDate = datetime(myYear, myMonth, 1)
    FirefromDate= FirefromDate.strftime('%Y-%m-%d')
    # fromDate = pd.Timestamp(fromDate)
    FiretoDate = datetime(myYear, myMonth+1,1)
    FiretoDate=FiretoDate.strftime('%Y-%m-%d %H:%M')

    # import shape file defining Canadian water regions
    WaterRegions_gdf = gpd.read_file('../Fire_and_Water/resources/Drainage_regions_Regions_de_drainage.shp')

    #create some user friendly column names for presentation
    WaterRegions_gdf.rename(columns = {'DR_Name':'Drainage Regions', 'ODA_Name':'Ocean Drainage Areas'}, inplace = True)

    #step through the mongodb collections, convert the mongodb _id to str so it can be serialized by Geopandas and store the collection in a Dictionary 
    #dataframes for further processing.
    myCollectionsList = db.list_collection_names()
    myDataFrameDict = {}
    query = {}
    for collections in myCollectionsList:
        thisCollection = db[collections]
        if collections == 'ForestFirePoints':
            query = {"REP_DATE":{'$gte':FirefromDate,
                                '$lte':FiretoDate}}
        
            # query = {'$and':[{"YEAR":fireMonth},{"MONTH":fireYear}]}
        elif collections == 'WaterSampleData':
            query = {"DATE_TIME_HEURE":{'$gte':WaterfromDate,
                                        '$lte':WatertoDate}}
        
        myDocList = list(thisCollection.find(query))
        for document in myDocList:
            document['_id'] = str(document['_id'])
        thisDataFrame = pd.DataFrame(myDocList)
        query = {}
        myDataFrameDict[collections + '_df']=thisDataFrame

    #Slicing out superflous columns.
    myDataFrameDict['WaterSampleData_df']=myDataFrameDict['WaterSampleData_df'].iloc[:,:13]

    #merge SampleData and the Watersites for plotting
    WaterSampleData_df = myDataFrameDict['WaterSampleData_df']
    WaterCombinedData_df =  pd.merge(WaterSampleData_df, myDataFrameDict['WaterSites_df'], how='inner', on='SITE_NO')

    #define geometry columns 
    # myDataFrameDict["WaterSites_df"]['geometry'] = gpd.points_from_xy(myDataFrameDict["WaterSites_df"]['LONGITUDE'], myDataFrameDict["WaterSites_df"]['LATITUDE'])
    WaterCombinedData_df['geometry'] = gpd.points_from_xy(WaterCombinedData_df['LONGITUDE'],WaterCombinedData_df['LATITUDE'])
    myDataFrameDict["ForestFirePoints_df"]['geometry'] = gpd.points_from_xy(myDataFrameDict["ForestFirePoints_df"]['LONGITUDE'], myDataFrameDict["ForestFirePoints_df"]['LATITUDE'])

    #convert the df's to a gdf's
    FirePoint_gdf =  gpd.GeoDataFrame(myDataFrameDict["ForestFirePoints_df"],geometry='geometry')
    FirePoint_gdf.set_crs(epsg=4617, inplace=True)
    WaterCombinedData_gdf = gpd.GeoDataFrame(WaterCombinedData_df, geometry='geometry')
    WaterCombinedData_gdf.set_crs(epsg=4617, inplace=True)

    #lets reduce the WaterSites we're plotting to the west
    fromSites = WaterCombinedData_gdf['SITE_NO'].unique()
    popSites = []
    for site in fromSites:
        # if site[:2] in ['BC', 'AL', 'SA']:
        popSites.append(site)

    #get our popup data for our choosen sites

    staging_gdf = WaterCombinedData_gdf.loc[(WaterCombinedData_gdf['SITE_NO'].isin(popSites) & WaterCombinedData_gdf['VARIABLE'].isin(['ARSENIC TOTAL','CADMIUM TOTAL', 'LEAD TOTAL']))]
    # staging_gdf = WaterCombinedData_gdf.loc[(WaterCombinedData_gdf['VARIABLE'].isin(['ARSENIC TOTAL','CADMIUM TOTAL', 'LEAD TOTAL']))]

    # create a list of sites with a list of VARIABLES we want to plot
    PlotWaterData_gdf = staging_gdf[['SITE_NO','DATE_TIME_HEURE','VALUE_VALEUR', 'VARIABLE', 'geometry']].copy()

    sitePlotData_gdf = staging_gdf[['SITE_NO','SITE_NAME','LATITUDE','LONGITUDE', 'geometry']].copy()
    sitePlotData_gdf.drop_duplicates(inplace = True)

    # find the limits of the data
    maxlat = FirePoint_gdf['LATITUDE'].max()
    minlat = FirePoint_gdf['LATITUDE'].min()
    maxlng = FirePoint_gdf['LONGITUDE'].max()
    minlng = FirePoint_gdf['LONGITUDE'].min()

    myMap = WaterRegions_gdf[['Ocean Drainage Areas', 'Drainage Regions', 'geometry']].explore(column = 'Ocean Drainage Areas',
                                    name = "Drainage Areas", 
                                    overlay = False, 
                                    cmap = 'Accent', 
                                    zoom_start = 4,
                                    zoom_on_click=False,
                                    min_lat=minlat,
                                    max_lat=maxlat,
                                    min_lon=minlng,
                                    max_lon=maxlng,
                                    tooltip = False,
                                    attr = "https://open.canada.ca/en/open-government-licence-canada",
                                    popup = ['Ocean Drainage Areas', 'Drainage Regions'])


    #create a heat map based on the size of the fire
    HeatMap(FirePoint_gdf[['LATITUDE', 'LONGITUDE', 'SIZE_HA']], name='Forest Fire Density', overlay = True, show=False).add_to(myMap)

    #create a feature layer for the forest fire daa.
    folium.GeoJson(FirePoint_gdf,
                name = "Forest Fires", 
                marker = folium.Marker(icon=folium.Icon(icon='fire', color='red')),
                popup=folium.GeoJsonPopup(fields = ['FID', 'FIRENAME', 'SIZE_HA', 'MORE_INFO']),
                show = False,
                overlay = True,    
                ).add_to(myMap)


    #Create a Feature Group for each water monitoring site.
    WaterSiteFG = folium.FeatureGroup(name="Water Data Sites", show=False).add_to(myMap)
    for i, row in sitePlotData_gdf.iterrows():
        #create the chart for the values we are plotting for each site.
        circle = (
            Chart(PlotWaterData_gdf.loc[PlotWaterData_gdf['SITE_NO'] == row['SITE_NO']])
            .mark_circle()
            .encode(
                x="DATE_TIME_HEURE",
                y="VALUE_VALEUR",
                color="VARIABLE",
                size="VALUE_VALEUR"
            )
        )
        title= ("Heavy Metal Concentrations")
        
        vega_lite=folium.VegaLite(
            circle,
            width="100%",
            height="100%",
    
        
        )
        #add the chart to a Marker and add that marker to a feature group for plotting.
        mylat = row['LATITUDE']
        mylng = row['LONGITUDE']

        loc = [mylat, mylng]
        myMarker = folium.Marker(loc, icon=folium.Icon(icon='cloud', color='green'))
        myToolTip = folium.Tooltip(f"Site: {row['SITE_NO']},\\n Site Name:{row['SITE_NAME']}") 
        myPopUp = folium.Popup()
        vega_lite.add_to(myPopUp)
        myPopUp.add_to(myMarker)
        myToolTip.add_to(myMarker)
        myMarker.add_to(WaterSiteFG)
        


    folium.TileLayer("OpenStreetMap").add_to(myMap)
    folium.LayerControl().add_to(myMap)

    return myMap




