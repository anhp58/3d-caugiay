# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:35:10 2020

@author: chick
"""


import os
import glob
from numpy import genfromtxt
import cv2 as cv

BASE_DIR = r"D:\height-estimation"

BASE_TRAIN_IMG2_DIR = os.path.join(BASE_DIR, r"{}\mask{}\cg_25m".format("train", "2"))
TRAIN_IMG2_LIST = glob.glob(os.path.join(BASE_TRAIN_IMG2_DIR, "*.png"))

BASE_TRAIN_IMG1_DIR = os.path.join(BASE_DIR, r"{}\mask{}\cg_25m".format("train", "1"))
TRAIN_IMG1_LIST = glob.glob(os.path.join(BASE_TRAIN_IMG1_DIR, "*.png"))

BASE_TEST_IMG2_DIR = os.path.join(BASE_DIR, r"{}\mask{}\cg_25m".format("test", "2"))
TEST_IMG2_LIST = glob.glob(os.path.join(BASE_TEST_IMG2_DIR, "*.png"))

BASE_TEST_IMG1_DIR = os.path.join(BASE_DIR, r"{}\mask{}\cg_25m".format("test", "1"))
TEST_IMG1_LIST = glob.glob(os.path.join(BASE_TEST_IMG1_DIR, "*.png"))

y_train = genfromtxt(os.path.join(BASE_DIR, r"{}\height.csv".format("train")), delimiter=',')
y_test = genfromtxt(os.path.join(BASE_DIR, r"{}\height.csv".format("test")), delimiter=',')
K = 250
NUM_BINS = 50
EXTRA_DEG_25M = 0.00013

SIFT = cv.xfeatures2d.SIFT_create()
SURF = cv.xfeatures2d.SURF_create(425) # should pick a threshold between 300 and 500
ORB = cv.ORB_create()