# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:30:22 2020

@author: chick
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from shutil import copy as cp
from sklearn.model_selection import train_test_split

NUM_OF_BIN = 50
BASE_DIR = r"D:\height-estimation"
ORG_FOLDER = r"mask2\cg_25m"
CSV_FILE = "../data/csv_polygon/lat_long_0m.csv"

def toCSV (lat_long_list, mycsv):
	import csv

	with open(mycsv, 'wb') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    for row in lat_long_list:
	    	wr.writerow(row)

def get_range (csvfile):
    
    df = pd.read_csv(csvfile)
    heights = df['height'].values
    bins = plt.hist(heights, bins = NUM_OF_BIN) 
    print (bins)
    return heights, bins[1] # index 1 for the threshold list in histogram

def get_sub_range (heights, bins):
    
    count_element = 0 # for checking total number of elements
    
    list_sub_index = []
    list_height = []
    
    for index in range (0, NUM_OF_BIN):
        
        sub_index_tmp, = np.where( (heights >= bins[index]) 
                                  & (heights < bins[index+1]) ) # get file name
        
        height_tmp = heights[ (heights >= bins[index]) 
                                   & (heights < bins[index+1])] # get height value
        
        count_element += len(sub_index_tmp) # for checking total number of elements
        
        list_sub_index.append(sub_index_tmp)
        list_height.append(height_tmp)
    
    return list_sub_index, list_height, count_element

def drop_outlier (list_sub_index, list_heights):
    
    # 5 number of sample which is considered as outlier
    list_heights = [height for height in list_heights if len(height) > 5]
    list_sub_index = [sub_index for sub_index in list_sub_index if len (sub_index) > 5]
    
    return list_heights, list_sub_index
    

def train_test_shuffle (list_sub_index, list_heights):
    
    list_Xtrain = []
    list_Xtest = []
    list_Ytrain = []
    list_Ytest = []
    
    for X, y in zip(list_sub_index, list_height):
        
        y_train, y_test, X_train, X_test = train_test_split(
            X, y, test_size=0.3, random_state=42)
        
        list_Xtrain.append(X_train)
        list_Xtest.append(X_test)
        list_Ytrain.append(y_train)
        list_Ytest.append(y_test)
    
    return list_Ytrain, list_Ytest, list_Xtrain, list_Xtest

def sampling (list_X, list_y, target_dir):
    
    for sub_list_X, sub_list_y in zip (list_X, list_y):
        for X in sub_list_X:
            cp (
                os.path.join(BASE_DIR, ORG_FOLDER, "{}.png".format(X)),
                os.path.join(BASE_DIR, target_dir, "{}.png".format(X))
                )
        
#main
heights, bins = get_range (CSV_FILE)
list_sub_index, list_height, count_element = get_sub_range (heights, bins)
list_sub_index, list_height = drop_outlier(list_sub_index, list_height)
list_Ytrain, list_Ytest, list_Xtrain, list_Xtest = train_test_shuffle(list_sub_index, list_height)

flat_Ytrain = np.asarray([item for sublist in list_Ytrain for item in sublist])
flat_Ytest = np.asarray([item for sublist in list_Ytest for item in sublist])

train_dir = r"train\mask2\cg_25m"
test_dir = r"test\mask2\cg_25m"

# =============================================================================
# np.savetxt(os.path.join(BASE_DIR, train_dir, "height.csv"), flat_Ytrain, delimiter=",")
# np.savetxt(os.path.join(BASE_DIR, test_dir, "height.csv"), flat_Ytest, delimiter=",")
# =============================================================================

# =============================================================================
# sampling (list_Xtrain, list_Ytrain, train_dir)
# sampling (list_Xtest, list_Ytest, test_dir)
# =============================================================================


    