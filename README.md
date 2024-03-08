# forestFireProject
Canadian Forest Fire Project 3 Team 4
## An overview of the project and its purpose:
To understand the nature & causes of wildfires and their impact on the environment using data between 1946 and 2021. 
Specifically, we based our research on finding answers to the following questions: 
a. What causes forest fires and does changes in environmental weather conditions (i.e. Temperature & Humidity) affect it?
b. How has the frequency and spatial distribution of wildfires in Canada changed overtime?
c. Does forest fire impact water quality?

Our findings are poised to benefit a wide array of stakeholders seeking effective forest fire prevention and mitigation strategies, such as Government agencies (i.e. CFS, CIFFC, NRCan), Environmental organizations, Climate change researchers, Policymakers, Insurance companies, Forestry Companies, Indigenous communities, and General public. 

The Jupyter Notebooks "Fire_Analysis", "Fireplotly", and "Fireplotlyfin" assess the situational aspects relating to wildfires by presenting graphs of the frequency and spatial distribution of wildfires, such as the Total Area Burned and Count of Fires (1950-2021); how has the frequency of wildfires changed over the years; fire occurrence inside and outside the protection zones; analysis of fire counts by year; as well as a temporal analysis of wildfire counts over seasons to identify patterns, trends and peaks. 
The Jupyter Notebooks "Fireplotlyfin", "Fire_With_Weather", and "Fireplotly" delve into investigating the salient causes of the wildfires, such as "Total Area Burned by Cause of Fire - 1950 - 1921", "Analysis of primary causes of wildfires", which identified lightning as the major cause.  Further, an animation of weather data overlaying wildfire occurrences identified high temperatures and low humidity as plausible root causes for the occurrence of climate conditions that produce lightning, thereby connecting the increasing occurrence of wildfires to global warming as a root cause. 
The Jupyter Notebook "FireWithWater" extensively evaluates the impact on the water quality, which helps us to understand the adverse effects on the landscape surrounding the burn area.
The Jupyter notebooks will be located in the main branch and / or in the respective branches. 

## Instructions on how to use and interact with the project:
The data included polygons (perimeter around the wildfire) and fire point (the centre point of the wildfire occurrence).  The team considered using MongoDB as an apt database given the GeoJson nature of the files. Further, the team considered using Geopandas, which has a lot of native options for using mapping data.  We believed GeoPandas would output HTML and Javascript. We were using the local instance of MongoDB on each team member's local computer, and hence worked towards reformatting / processing the GeoJson object files in the array format so that the data could be stored in MongoDB. To get the data back in a format that GeoPandas expected (i.e. as an object), used GeoPandas From_Feature method which enabled it to consume data.  Also used the geometry.simplify method to get around the very large size per document with the polygons. The dat was also cleaned / filtered (e.g. rows in the fire_point_data included locations showing Latitude and Longitude as 0 degrees). 

In terms of the technology stack, we used python libraries such as pymongo, pandas, geopandas, matplotlib / pyplot, plotly, datetime, requests, send_file, Flask, render_template, jsonify, imageio.v2, Folium, Vega-lite, pprint, JavaScript, CSS / bootstrap (jumbotron). 

## At least one paragraph summarizing efforts for ethical considerations made in the project: 
Data has been presented by providing proper attribution regarding the source of the data / quote.  
Further, data was downloaded from authentic and publicly available sources (please refer to the References section below for information on the sources). 
We endeavoured to keep the truth-telling robust by utilizing technology solutions in case the data was too large to download (e.g. >61 million records for the entire dataset comprising 950 Canada-wide weather stations gathering data since 
Ensuring that the team members had access to a consistent dataset.  Further, the teamd eliberated on the reseach approaches such as performing temporal and causal analysis that would be relevant in developing a consistent storyline for relevant stakeholders.  The presentation of data was supported with visualizations that were self-explanatory and showing the appropriate label, titles, etc. Finally, the analysis was performed in an in-depth and extensive manner in order to ensure that true and actionable insigghts are available to the various stakeholders.  

## References for the data source(s)
The resources folder contains the fire data (Source: http://cwfis.cfs.nrcan.gc.ca/ha/nfdb), water data (https://data-donnees.az.ec.gc.ca/data/substances/monitor/national-long-term-water-quality-monitoring-data/?lang=en), and weather data (Source: Environment Canada; URL: https://api.weather.gc.ca/collections/climate-daily/items). . 

## References for any code used that is not your own. 
ChatGPT and various technology websites such as stackoverflow, w3 utilized to review documentation for line of code.  

