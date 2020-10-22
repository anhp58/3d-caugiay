# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:45:45 2020

@author: chick
"""


import numpy as np
import cv2 as cv
import glob
import os
from sklearn.cluster import MiniBatchKMeans
from numpy import genfromtxt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pickle
from const import *

def sort_filename (img_list, base_img_dir):
    """Sort the file names
        Args:
            img_list (list): list of images
            base_img_dir (string): the image dir
        Returns:
            Sorted list of file names
    """
    
    img_id_list = [int(imgfile.split("\\")[-1][:-4]) for imgfile in img_list]
    sorted_filename = [ os.path.join(base_img_dir, "{}.png".format(str(img_id))) for img_id in sorted(img_id_list) ]
    
    return sorted_filename

def pca_sift (X):
    """
        Not used
    """
    
    from sklearn.decomposition import PCA
    pca = PCA()
    pca = pca.fit(X)
    
    return pca.transform(X)

def pca_sift_test (X):
    """
        Not used
    """
    from sklearn.decomposition import PCA
    
    pca = PCA()
    pca = pca.fit(X)
    
    return pca

def keypoint_extraction (img_list, descriptor):
    """Extract keypoint from image with provided descriptor
        Args:
            img_list (list): list of images
            descriptor (object): object descriptor
        Returns:
            dico (ndarray): feature ndarray
    """
    
    dico = []
    for imgfile in img_list:
        
        img = cv.imread(imgfile)
        kp, des = descriptor.detectAndCompute(img, None)
        
        if des is None:
            no_kp = np.zeros((1, descriptor.descriptorSize()), np.float32) #np.float32
            dico.append(no_kp[0])
            
        elif des is not None:
            for d in des:
                if isinstance(np.float64(d), np.floating):
                    print (imgfile)
                dico.append(d)
                
    return dico

def clustering (dico):
    """To cluster the input feature using MiniBatchKMeans
        Args:
            dico (array): the feature dataset
        Returns:
            kmeans (object): the kmeans model
    """
    
    k = K
    batch_size = 200
    init_size=3*k
    kmeans = MiniBatchKMeans(n_clusters=k, batch_size=batch_size, 
                             init_size=init_size, verbose=2).fit(dico)
    
    return kmeans

def histogram (img1_list, kmeans1, 
               img2_list, kmeans2, 
               descriptor1, descriptor2):
    """Calculate the keypoint and cluster each record to "word"
        Args:
            img1_list (list): list of images which are masked by the building polygon - "within dataset"
            kmeans1 (object): kmean model for the dataset within the polygon
            img2_list (list): list of images which are masked by the outside of the building polygon
            kmeans2 (object): kmean model for the dataset placed outside the polygon - "without dataset"
            descriptor1 (object): the descriptor for the "within" dataset
            descriptor2 (object): the descroptor for the "without" dataset
        Returns:
            histo_list (ndarray): bag of words feature
    """
    
    histo_list = []
    for imgfile1, imgfile2 in zip(img1_list, img2_list):
        
        img1 = cv.imread(imgfile1)
        img2 = cv.imread(imgfile2)
              
        kp1, des1 = descriptor1.detectAndCompute(img1, None)
        kp2, des2 = descriptor2.detectAndCompute(img2, None)
        
        histo1 = np.zeros(K)
        histo2 = np.zeros(K)
        
        
        if des1 is None: # des1
            nkp = 1
            d = np.zeros((1, descriptor1.descriptorSize()), np.float32) # no keypoint         
            idx = kmeans1.predict([d[0]])
            histo1[idx] += 1/nkp # histo 1
            
        elif des1 is not None: # des1
            
            nkp = np.size(kp1) #kp1
            
            for d in des1:
                idx = kmeans1.predict([d])
                histo1[idx] += 1/nkp #normalized the histogram      
                
        if des2 is None: #des2
            nkp = 1
            d = np.zeros((1, descriptor2.descriptorSize()), np.float32) # no keypoint         
            idx = kmeans2.predict([d[0]])
            histo2[idx] += 1/nkp # histo 1
            
        elif des2 is not None: #des2
            
            nkp = np.size(kp2) #kp2
            
            for d in des2:
                idx = kmeans2.predict([d])
                histo2[idx] += 1/nkp #normalized the histogram, histo 2
            
        histo_list.append(np.concatenate((histo1, histo2)))
    # return concatnate of object keypoint and focus keypoint 
    return histo_list

def regression_model (histo_list, y):
    """Train the regression model based on bag of word dataset
        Args:
            histo_list (array): feature array
            y (array): label array
        Returns:
            regr (object): regression model
    """
    
    X = np.array(histo_list)    
    regr = RandomForestRegressor(max_depth=700, random_state=50)
    regr.fit(X, y)
    
    return regr

def prediction (img1_list, base_img1_dir,
                img2_list, base_img2_dir,
                kmeans1, kmeans2,
                descriptor1, descriptor2, regr):
    """Inference the data based on the regression model
        Args:
            img1_list
            base_img1_dir
            img2_list
            base_img2_dir
            kmeans1
            base_img2_dir
            kmeans1
            kmeans2
            descriptor1
            descriptor2
            regr
        Returns:
            y_reg
            histo_list
    """
    
    sorted_filename1 = sort_filename (img1_list, base_img1_dir)
    sorted_filename2 = sort_filename (img2_list, base_img2_dir)
    
    histo_list = histogram (sorted_filename1, kmeans1,
                            sorted_filename2, kmeans2,
                            descriptor1, descriptor2)
    
    y_reg = regr.predict(histo_list)
    
    return y_reg, histo_list

def training (img1_list, base_img1_dir,
              img2_list, base_img2_dir,
              descriptor1, descriptor2, y_train):
    
    sorted_filename1 = sort_filename (img1_list, base_img1_dir)
    des1 = keypoint_extraction (sorted_filename1, descriptor1)
    
    sorted_filename2 = sort_filename (img2_list, base_img2_dir)
    des2 = keypoint_extraction (sorted_filename2, descriptor2)
    
    kmeans1 = clustering(des1)
    kmeans2 = clustering(des2)
    
    print ("kmeans1: {}".format(kmeans1))
    print ("kmeans2: {}".format(kmeans2))
    
    histo_list = histogram (sorted_filename1, kmeans1,
                            sorted_filename2, kmeans2,
                            descriptor1, descriptor2)
    regr = regression_model (histo_list, y_train)
    
    return kmeans1, kmeans2, regr, histo_list

def dump_model (model, filename):
    pickle.dump(model, open(filename, 'wb'))

def load_model (filename):
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

#main
descriptor1 = SURF
descriptor2 = SURF

# =============================================================================
# kmeans1, kmeans2, regr, histo_list_train = training (TRAIN_IMG1_LIST, BASE_TRAIN_IMG1_DIR,
#                                                      TRAIN_IMG2_LIST, BASE_TRAIN_IMG2_DIR,
#                                                      descriptor1, descriptor2,
#                                                      y_train)
# dump_model (kmeans1, os.path.join(BASE_DIR, r"model\kmeans1.sav"))
# dump_model (kmeans2, os.path.join(BASE_DIR, r"model\kmeans2.sav"))
# dump_model (regr, os.path.join(BASE_DIR, r"model\regr.sav"))
# 
# y_reg, histo_list_test = prediction (TEST_IMG1_LIST, BASE_TEST_IMG1_DIR,
#                                      TEST_IMG2_LIST, BASE_TEST_IMG2_DIR,
#                                      kmeans1, kmeans2,
#                                      descriptor1, descriptor2, regr)
# 
# print ("mae: {}".format(mean_absolute_error(y_test, y_reg)))
# =============================================================================
