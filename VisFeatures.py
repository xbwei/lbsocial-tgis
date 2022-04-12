'''
Created on Dec 21, 2014

This script supports the visualize feature tool in the ArcGIS.

It will create a feature layer for the activites or places in ArcGIS.

The activity layer can be viewed in 2D and 3D.


The database name, database admin name, table names are manually typed. you need to change them based on your system settings.


'''
import arcpy
import logging
import traceback
import sys

from arcpy import env

# Set environment settings


'''
handle log
'''


logger = logging.getLogger('VisFeature')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('VisFeature.log')
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


inputtable = arcpy.GetParameterAsText(0)
layername = arcpy.GetParameterAsText(1)
x_field = arcpy.GetParameterAsText(2)
y_field = arcpy.GetParameterAsText(3)
z_field = arcpy.GetParameterAsText(4)
reference = arcpy.GetParameterAsText(5)
outfolder = arcpy.GetParameterAsText(6)



try:
    env.workspace = outfolder
    out_put_layer = outfolder + "\\"+layername+".lyr"

    outlayer = arcpy.MakeXYEventLayer_management(inputtable,x_field,y_field,layername,reference,z_field)

    arcpy.SaveToLayerFile_management(outlayer, out_put_layer)

    
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    arcpy.AddError( ''.join('!! ' + line for line in lines))  
    logger.info(''.join('!! ' + line for line in lines) )
