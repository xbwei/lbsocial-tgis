'''
Created on Dec 21, 2014

This script supports the spatial-temporal cluster tool in ArcGIS.

It will take the selected activities and identify the spatial-temporal clusters with the pysal library. 

The database name, database admin name, table names are manually typed. you need to change them based on your system settings.


'''
import arcpy
import logging
import traceback
import sys


from arcpy import env
import psycopg2

import time
import numpy as np

import pysal
import datetime
# Set environment settings


'''
handle log
'''

logger = logging.getLogger('STActivity')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('STActivity.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s9 - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


Feature_Set = arcpy.GetParameterAsText(0)
activities = arcpy.GetParameterAsText(1)
delta = arcpy.GetParameterAsText(2)
tau = arcpy.GetParameterAsText(3)


'''
calculate spatial-temporal cluster
'''
try:
    # Process: Select Layer By Location
    selectedfeatures = arcpy.SelectLayerByLocation_management(activities, "COMPLETELY_WITHIN", Feature_Set, "", "NEW_SELECTION")
    
    cursor = arcpy.SearchCursor(activities)
    connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo') # put your database name, user name and password
            
    s_cords= []
    t_cords=[]
    arcpy.AddMessage("Activity ID:")
    num_arcitivty = 0
    for row in cursor:
        arcpy.AddMessage("\t" + str(row.getValue("activityid")))
        num_arcitivty = num_arcitivty +1
        try:
            activity_cursor = connection.cursor()
            activity_cursor.execute('select ST_X(location),ST_Y(location),time from demo.activity_demo where activityid =' +"'"+ row.getValue("activityid")+"'")
            activity_cursor = activity_cursor.fetchall()
            for record in activity_cursor:
# 
                s_cord = [record[0],record[1]]
 
                s_cords.append(s_cord)
 
                record_time = datetime.datetime(int(record[2][:4]),int(record[2][5:7]),int(record[2][8:10]),int(record[2][11:13]),int(record[2][14:16]))
 
                time_delta = datetime.datetime.now()-record_time
 
                t_cord = [time_delta.days,1.0]
                   
                t_cords.append(t_cord)
# 
#         #         
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            arcpy.AddError( ''.join('!! ' + line for line in lines))  
            logger.info(''.join('!! ' + line for line in lines) )
         
    s_cords = np.asanyarray(s_cords)
    t_cords = np.asarray(t_cords)
   
    connection.close()
  
    np.random.seed(100)
 
     
    knox_result = pysal.spatial_dynamics.interaction.knox(s_cords,t_cords,delta=float(delta),tau=float(tau),permutations=99)

    arcpy.AddMessage("--------")
    arcpy.AddMessage('number of activities: ' +str(num_arcitivty))
    arcpy.AddMessage("--------")
    arcpy.AddMessage("Knox test")
    arcpy.AddMessage("\t number of interactions: " + str(knox_result['stat']))
    arcpy.AddMessage("\t p value: " + str(knox_result['pvalue'][0]))


except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    arcpy.AddError( ''.join('!! ' + line for line in lines))  
    logger.info(''.join('!! ' + line for line in lines) )