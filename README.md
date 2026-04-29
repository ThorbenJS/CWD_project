# Finnish coastal weather data combined with ship AIS location info
### A little project where the point was to find out if weather data from finnish coastal waters could be mapped to ship AIS location data of ships that are moving within finnish coastal waters.

## /src/ais_data_reciever_api.py
The point of this script was to establish some kind of proof of concept that I could get ship AIS location data from Digitraffic.fi's API and run that data directly into a query to the Finnish Metereology Institutes (FMI) API.
This worked quite well since coordinated of a ship could be directly inserted into a query that queries FMIs HARMONIE weather model and gives a forecast on those precise coordinates.

## /src/sanity_check.py
To check the viability of the forecast data (if it's any good so to say), I had to manually collect forecast data for every hour. Since the model is updated every 6 hours and I do not know when it is updated, this seemed 
to be the only option to reliably get the most up to date forecast for every hour.

So the script queries forecast data from 42 different coordinates/locations which represent th 42 weather stations, and loads it into a PostgreSQL database. When I query the historical observation data from those same 42 weather stations and compare them
to the forecasts at those same locations I will get somewhat of a picture of how much error is to be expected when getting forecast data from a ship's location.

## /src/error_calculations.ipynb
This is a notebook I made for the purpose of doing some small data analysis concerning the observation and forecast data. In this notebook I calculate the MAE (Mean Absolute Error) for every parameter of the forecasts
and observations. 

## sääasemat.txt
A list of the weather stations that were used. I handpicked these staions by looking at a map and seeing if a station was coastal or not. Every station has a name, fmisid and coordinates listed in this file.
