# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:46:09 2020

@author: chick
"""

from pywinauto import Application
import time
import os

def handle_bad_request(app):
    all_done = 1
    while all_done == 1:
        try:
            print (app.cpu_usage())
            if app.cpu_usage() == 0.0:
                time.sleep(0.5)
                break
            else:
                all_done = 1
        except:
            print("Testing...")
            time.sleep(0.5)

def download(input_dict):
    """ Auto download image with lat, long """
    
    os.chdir(input_dict["app_dir"])
    app = Application(backend="uia").start(input_dict["app_exe"])
    
    
    # app['Google Satellite Maps Downloader 8.02'].print_control_identifiers()
    app[input_dict["app_name"]].Edit7.set_text(input_dict["save_path"]) #save_path
    app[input_dict["app_name"]].Edit3.set_text(input_dict["bottom_lat"]) #bottom lat
    app[input_dict["app_name"]].Edit4.set_text(input_dict["top_lat"]) #top lat
    app[input_dict["app_name"]].Edit5.set_text(input_dict["right_long"]) #right long
    app[input_dict["app_name"]].Edit6.set_text(input_dict["left_long"]) #lef long
    click_zoom(21, app[input_dict["app_name"]][input_dict["click_operation"]]) #zooming
    app[input_dict["app_name"]].StartButton.click() #start
    
    # check bad request
    handle_bad_request(app)
            
    app.kill()
    return app
def combine (input_dict):

    """ Automatically combine small images to large one """
    os.chdir(input_dict["app_dir"])
    
    app = Application(backend="uia").start(input_dict["app_exe"])
    app[input_dict["app_name"]]["Edit2"].set_text(input_dict["task_file"]) # save_path
    #app[input_dict["app_name"]]['Create a  JPEG file '].click() #uncheck jpg download
    app[input_dict["app_name"]]['Create a  TIFF file '].click() #uncheck jpg download
    app[input_dict["app_name"]]['Create a  PNG file '].click() #uncheck jpg download
    app[input_dict["app_name"]].Combine.click() #combine
    
    # check bad request
    handle_bad_request(app)
    
    app.kill()


def click_zoom(zoom_level, obj):
    """ Zoom max level """
    default_zoom = 13
    
    for x in range (zoom_level - default_zoom):
       obj.click()