# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:59:17 2020

@author: chick
"""


from utils.utilize_masking import *
import os

SHP_FILE = r"I:\My Drive\Height-regression\CG_building\corrected_building_height_shapefile\footprint_height_reprojected-polygon.shp"
EXT_DIST = [0, 25, 50, 100] 
NUM_OF_POLYGON = 1160
LIST_POLYGON = getMask (SHP_FILE)
BASE_DIR = r"D:\height-estimation"

for extdist in [EXT_DIST[1]]:
    print ("{}m".format(extdist))
    for index in range (0, NUM_OF_POLYGON):
        try:
            img_path = os.path.join(BASE_DIR, "raw_data\cg_{}m\{}\my_new_task_combined\my_new_task.jpg".format(extdist, index))
                
            img = rasterio.open(img_path)
        
            mask1 = getIndexMask(LIST_POLYGON[index], img, False, True)
            mask2 = getIndexMask(LIST_POLYGON[index], img, True, False)
            
            path_mask1 = os.path.join(BASE_DIR, "mask1\cg_{}m\{}.png".format(extdist, index))
            path_mask2 = os.path.join(BASE_DIR, "mask2\cg_{}m\{}.png".format(extdist, index))

            cv.imwrite(path_mask1, mask1)
            cv.imwrite(path_mask2, mask2)
        except:
            pass
# =============================================================================
#         cp (img_path, os.path.join(BASE_DIR, "image\cg_{}m\{}.jpg".format(extdist, index)))
# =============================================================================
        
        print (index)