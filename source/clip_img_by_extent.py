import arcpy
import pandas as pd 
import os

def get_extent_from_csv (extent_csv):
	df_extent = pd.read_csv(extent_csv)	

	bot_lat = df_extent['bot_lat'].values
	top_lat = df_extent['top_lat'].values
	left_long = df_extent['left_long'].values
	right_long = df.extent['right_long'].values

	return bot_lat, top_lat, left_long, right_long

def clip_by_extent(bot_lat, top_lat, left_long, right_long):
	