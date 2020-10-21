# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:39:23 2020

@author: chick
"""

import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping
import numpy as np
import os
import statistics


def getMask(shp_path):
    """ Extract polygon from shapfile """
    shapefile = gpd.read_file(shp_path)
    polygons = shapefile.geometry.values
    
    return polygons
def writeShp (shp_path, data):
    shapefile = gpd.read_file(shp_path)
    shapefile["color"] = data
    shapefile.to_file(shp_path)
    
def getRasterioImage (img_path):
    
    return rasterio.open(img_path, "r")

def getPixelsByBuilding (polygon, rasterio_image):
    
    mapping_polygon = [mapping(polygon)]   
    building_contained_img, transform = mask(rasterio_image, mapping_polygon, crop=True, all_touched=True )
    
    return building_contained_img

def averageWindow (window):
    
    flat_window = window.flat
    flat_array = [ flat_window[i] for i in range (0, len(flat_window) ) ]
    avg_value = statistics.mean(flat_array)
    
    return avg_value

def aqiMapToColor (aq_index):
    
    if 5.15 <= aq_index and aq_index < 13.9:
        return 1
    elif 13.9 <= aq_index and aq_index < 18.6:
        return 2
    elif 18.6 <= aq_index and aq_index < 22.9:
        return 3
    elif 22.9 <= aq_index and aq_index < 26.6:
        return 4
    elif 26.6 <= aq_index and aq_index < 29.6:
        return 5
    elif 29.6 <= aq_index and aq_index < 35.5:
        return 6
    elif 35.5 <= aq_index and aq_index < 61.9:
        return 7
    elif 61.9 <= aq_index and aq_index < 103:
        return 8

id_scene = "combined_reproject2"
base_dir = r"G:\My Drive\3D-Caugiay"
img_path = os.path.join(base_dir, r"onkk\21072020-20h.tif")
shp_path = os.path.join(base_dir, r"roi\new\corrected_shp_reproject\{}.shp".format(id_scene))  

polygons = getMask(shp_path)
rasterio_image = getRasterioImage (img_path)

air_quality_list = []
color_list = []

for index in range (0, len(polygons)):
    
    window = getPixelsByBuilding(polygons[index], rasterio_image )
    avg_pixel = averageWindow (window)
    color = aqiMapToColor(avg_pixel)
    air_quality_list.append(avg_pixel)
    color_list.append(color)
    
# =============================================================================
# np.savetxt(os.path.join(base_dir, r"air_quality\color_{}.csv".format(id_scene)),
#            color_list,
#            delimiter=",",
#            fmt='%s'
#     )
# =============================================================================
#writeShp (shp_path, color_list)