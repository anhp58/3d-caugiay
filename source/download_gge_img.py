# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:48:57 2020

@author: chick
"""


from utils import utilize_pywin
import pandas as pd
import os

EXT_DIST = [0, 25, 50, 100]
APP_DIR = "C:/allmapsoft/gsmd"
DOWNLOADER = 'downloader.exe'
COMBINER = 'combiner.exe'
APP_NAME_DOWNLOADER = 'Google Satellite Maps Downloader 8.329'
APP_NAME_COMBINER = 'Map Combiner'
TASK_FILE_NAME = "my_new_task.gmid"


for ext_dist in [EXT_DIST[1]]:

    print ("ext_dist {}m".format(ext_dist))
    POLYGON_CSV = "../data/csv_polygon/lat_long_{}m.csv".format(ext_dist)
    DATA_DIR = r"D:\height-estimation\raw_data\cg_{}m".format(ext_dist)
           
    df_polygon = pd.read_csv(POLYGON_CSV)
    
    bot_lat = df_polygon['bot_lat'].values
    top_lat = df_polygon['top_lat'].values
    left_long = df_polygon['left_long'].values 
    right_long = df_polygon['right_long'].values
    height = df_polygon['height'].values
    
    corrupt_index = 0
    for index, (bl, tl, ll, rl, h) in enumerate (zip(bot_lat, top_lat, left_long, right_long, height)):
        
        if index >= corrupt_index:
            print ("img_{}".format(index))
            img_folder = DATA_DIR + "\{}".format(index)
            #os.makedirs(img_folder)
            download_dict = {
                'app_dir': APP_DIR,
                'app_exe': DOWNLOADER,
                'app_name': APP_NAME_DOWNLOADER,
                'save_path': img_folder,
                'bottom_lat': bl,
                'top_lat': tl,
                'right_long': rl,
                'left_long': ll,
                'click_operation': 'Page right'
            }
                
            task_file = os.path.join(img_folder, TASK_FILE_NAME)
            
            combine_dict = {
                'app_dir': APP_DIR,
                'app_exe': COMBINER,
                'app_name': APP_NAME_COMBINER,
                'task_file': task_file
                }
            
            utilize_pywin.download(download_dict)
            utilize_pywin.combine (combine_dict)
# =============================================================================
#         else:
#             break
# =============================================================================
