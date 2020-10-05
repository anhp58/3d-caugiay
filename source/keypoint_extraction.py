# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:21:00 2020

@author: chick
"""

import cv2 as cv
import numpy as np
import os
import glob
from sklearn.cluster import MiniBatchKMeans
from numpy import genfromtxt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

K = 1500

def bow_training (descriptor, detector):
    
    bow_trainer = cv.BOWKMeansTrainer(50)
    bow_trainer.add(np.float32(descriptor))
    vocab = bow_trainer.cluster().astype(descriptor.dtype)
    
    bow_descr = cv.BOWImgDescriptorExtractor(detector, cv.BFMatcher(cv.NORM_HAMMING))
    bow_descr.setVocabulary(vocab)
    
    return bow_descr

def clustering (des):
    
    k = K
    batch_size = 200
    init_size=3*k
    kmeans = MiniBatchKMeans(n_clusters=k, batch_size=batch_size, init_size=init_size, verbose=2).fit(des)
    
    return kmeans

def histogram (img_list, kmeans):
    
    histo_list = []
    for imgfile in img_list:
        
        img = cv.imread(imgfile)
        #gray = cv.cvtColor (img, cv.COLOR_BGR2GRAY)
        sift = cv.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(img, None)
        
        histo = np.zeros(K)
        
        
        if des is None:
            nkp = 1
            d = np.zeros((1, sift.descriptorSize()), np.float32) # no keypoint         
            idx = kmeans.predict([d[0]])
            histo[idx] += 1/nkp
        elif des is not None:
            nkp = np.size(kp)
            
            for d in des:
                idx = kmeans.predict([d])
                print (idx)
                histo[idx] += 1/nkp #normalized the histogram
            
        histo_list.append(histo)
        
    return histo_list

def desc_extraction (imglist, detector):
    
    des_list = []
    for imgfile in imglist:
        
        img = cv.imread(imgfile)
        
        detector = cv.xfeatures2d.SIFT_create()
        kp, des = detector.detectAndCompute(img, None)
        
        if des is None:
            no_kp = np.zeros((1, detector.descriptorSize()), np.float32)
            des_list.append(no_kp[0])
        elif des is not None:
            for d in des:
                if isinstance(np.float64(d), np.floating):
                    print (imgfile)
                des_list.append(d)
    
    return des_list

def sift_extraction (imgfile):
    
    img = cv.imread(imgfile)
    sift = cv.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(img, None)
    
    return des

def orb_extraction (imgfile):
    
    img = cv.imread(imgfile)
    orb = cv.ORB_create()
    kp = orb.detect(img,None)
    kp, des = orb.compute(img, kp)
    
    return des

def surf_extraction (imgfile):
    
    img = cv.imread(imgfile)
    surf = cv.xfeatures2d.SURF_create(400)
    kp, des = surf.detectAndCompute(img, None)
    
    return des
#main

BASE_DIR = r"D:\height-estimation"

BASE_TRAIN_IMG_DIR = os.path.join(BASE_DIR, r"{}\mask2\cg_25m".format("train"))
TRAIN_IMG_LIST = glob.glob(os.path.join(BASE_TRAIN_IMG_DIR, "*.png"))
