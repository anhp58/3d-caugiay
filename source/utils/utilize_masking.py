# -*- coding: utf-8 -*-

"""
Created on Mon Jun 15 13:48:57 2020

@author: chick
"""

import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping
from shapely import geometry
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.ops import unary_union
import cv2 as cv
import numpy as np
from shutil import copy2 as cp
import os

EXTRA_DEG_25M = 0.00013

def getMask(shp_file):
    """Extract polygon from shapfile 
        Args:    
            shp_file (string): path to the shapefile
        Returns:
            polygons (list of object): list of polygon in the shapefile
    """
    shapefile = gpd.read_file(shp_file)
    polygons = shapefile.geometry.values
    return polygons

def getExtentFromPolygon (polygon, extra_deg):
    """1. Get extent of the polygon 
        2. Extent the polygon by an extra degree
        Args:
            polygon (object):
            extra_deg (double): extra degree for surounding object
        Returns: 
            poly (object): extent of the extent polygon with an extra degree
    """
    bounds = polygon.bounds
    
    bot_lat = bounds[1] - extra_deg
    top_lat = bounds[3] + extra_deg
    left_long = bounds[0] - extra_deg
    right_long = bounds[2] + extra_deg
    
    poly = geometry.Polygon([[left_long, top_lat],
                            [right_long, top_lat],
                            [right_long, bot_lat],
                            [left_long, bot_lat]])
    
    return poly

def fixInvalidPolygon (invalid_pol):
    """ Fix invalid polygon - self-intersecting polygon 
        Args:
            invalid_pol (object): invalid polygon
        Returns:
            fine_pol (object): fixed polygon
    """
    
    lr = invalid_pol.exterior
    ur = unary_union(lr)
    fine_pol = Polygon(ur)
    
    return fine_pol
    
    
def getIndexMask(polygon, image):
    """ Get index with mask polygon 
        Args:
            polygon (object): polygon that used to clip the image
            image (string): path to image
        Returns:
            in_img (arr): array of pixels within the polygon
            out_img (arr): array of the pixels outside the polygon
            
    """
    image = rasterio.open(image)
        
    ext_polygon = getExtentFromPolygon(polygon, EXTRA_DEG_25M)
    
    if polygon.is_valid is False:
        polygon = fixInvalidPolygon (polygon)
    out_polygon = (ext_polygon.symmetric_difference(polygon)).difference(polygon)
    
    
    #ext_polygon_mapping = [mapping(ext_polygon)]
    in_polygon_mapping = [mapping(polygon)]
    out_polygon_mapping = [mapping(out_polygon)]
    
    in_image, in_transform = mask(image, in_polygon_mapping, crop=True, invert=False)
    out_image, out_transform = mask(image, out_polygon_mapping, crop=True, invert=False)

    in_image = np.transpose(in_image)
    in_image = cv.cvtColor(in_image, cv.COLOR_BGR2RGB)
    out_image = np.transpose(out_image)
    out_image = cv.cvtColor(out_image, cv.COLOR_BGR2RGB)
    
    return in_image, out_image

id_img_list = ["5.3"]

for id_img in id_img_list:
    print (id_img)
    image = r"G:\My Drive\3D-Caugiay\image\tif\Caugiay{}.tif".format(id_img)
    shapefile = r"G:\My Drive\3D-Caugiay\roi\new\corrected_shp\{}.shp".format(id_img)
    base_folder_in = r"G:\My Drive\3D-Caugiay\small_image_in\{}".format(id_img)
    base_folder_out = r"G:\My Drive\3D-Caugiay\small_image_out\{}".format(id_img)

    polygons = getMask(shapefile)
    for index in range (0, len(polygons)):
        print (index)
        in_image, out_image = getIndexMask (polygons[index], image)
        cv.imwrite(os.path.join(base_folder_in, "{}.png".format(index)), in_image)
        cv.imwrite(os.path.join(base_folder_out, "{}.png".format(index)), out_image)