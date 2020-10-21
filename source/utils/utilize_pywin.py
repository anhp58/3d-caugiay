# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:46:09 2020

@author: chick
"""

from pywinauto import Application
import time
import os

def handle_bad_request(app):
    """To handle bad request when download image from app by loop checking.
        Args:
            app (object): Application object
        Returns:
            None
    """
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
    """ 1. Auto download image with provied lats and longs
        2. Check bad request and redownload
        3. Kill the app
        Args:
            input_dict (dict) contains:
                            app_name (string): application's name
                            save_path (string): path to save image
                            bottom_lat (double): bottom lat of the image
                            top_lat (double): top lat of the image
                            right_long (double): right long of the image
                            left_long (double): left long of the image
                            click_operation (void): click until reach the max zoom level
        Returns:
            app (object): application object
    """
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
    """ 1. Automatically combine small images to large one 
        2. Check bad request and redo
        3. Kill the app
        Args:
            input_dict (dict) contains:
                app_dir (string): dir of the combine.exe file
                app_exe (string): name of the exe file = combine.exe
                app_name (string): name of the application
                task_file (string): path to task file
        Returns:
            None
    """
        
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
    """ Zoom to max level
        Args:
            zoom_level (int): the max zoom level
            obj (obj): click object
        Returns:
            None
    """
    default_zoom = 13
    
    for x in range (zoom_level - default_zoom):
       obj.click()