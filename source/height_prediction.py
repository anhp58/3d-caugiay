# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:27:44 2020

@author: chick
"""



from extraction_and_training import prediction, load_model
from const import *

import os
import pickle
import glob
import numpy as np

import geopandas as gpd

def writeShp (shp_path, data):
    shapefile = gpd.read_file(shp_path)
    shapefile["height"] = data
    shapefile.to_file(shp_path)

img_index = "5.3"
shp_path = r"I:\My Drive\3D-Caugiay\roi\new\corrected_shp\{}.shp".format(img_index)

base_dir = r"I:\My Drive\3D-Caugiay"
base_dir_in_img = r"I:\My Drive\3D-Caugiay\small_image_in\{}".format(img_index)
base_dir_out_img = r"I:\My Drive\3D-Caugiay\small_image_out\{}".format(img_index)

img_in_list = glob.glob(os.path.join(base_dir_in_img, "*.png"))
img_out_list = glob.glob(os.path.join(base_dir_out_img, "*.png"))

kmeans1 = load_model(os.path.join(BASE_DIR, r"model\kmeans1.sav"))
kmeans2 = load_model(os.path.join(BASE_DIR, r"model\kmeans1.sav"))
regr = load_model(os.path.join(BASE_DIR, r"model\regr.sav"))

descriptor1 = SURF
descriptor2 = SURF

# 1 = out, 2 = in

y_reg, histo_list_test = prediction (img_out_list, base_dir_out_img,
                                     img_in_list, base_dir_in_img,
                                     kmeans1, kmeans2,
                                     descriptor1, descriptor2, regr)
writeShp (shp_path, np.asarray(y_reg))
np.savetxt(os.path.join(base_dir, r"height\{}.csv".format(img_index)),
           np.asarray(y_reg),
           delimiter=","
    )