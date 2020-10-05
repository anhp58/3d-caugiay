# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:57:31 2020

@author: chick
"""


import os
import glob
#import shapefile
import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
# def extractHeight_shp(shpfile):
#     sf = shapefile.Reader(shpfile)
#     return [sf.record(i)['Height'] for i in range(0,len(sf.records())-1)]
# =============================================================================

def extractHeight_csv(csvfile):
    
    df = pd.read_csv(csvfile)
    height = df['height'].values
    return height

csvfile = "../data/csv_polygon/lat_long_0m.csv"
height = extractHeight_csv(csvfile)
bins = plt.hist(height, bins = 50)
plt.show()
# =============================================================================
# BASEDIR = 'I:\\My Drive\\Height-regression\\MS_building_height'
# os.chdir(BASEDIR)
# list_shp = glob.glob("{}\\*\\*.shp".format(BASEDIR))
# 
# height = []
# for shp in list_shp:
#     test = extractHeight(shp)
#     height = height + test
#     state = shp.split("\\")[-2]
#     print (state)
# 
# plt.hist(height, bins = 100)
# plt.show()
# =============================================================================
