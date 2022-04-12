'''
Created on Dec 21, 2014
This script support the calculate people social tool in ArcGIS
It will take the selected users' records, and calculate the network measures of the selected users.

The database name, database admin name, table names are manually typed. you need to change them based on your system settings.

'''
import arcpy
import logging
import traceback
import sys
import networkx as nx
import matplotlib.pyplot as plt

from arcpy import env
import psycopg2
import AnalyzeData

# Set environment settings


'''
handle log
'''

logger = logging.getLogger('CulcatePSocial')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('CulcatePSocial.log')
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

sql = arcpy.GetParameterAsText(1)
display = arcpy.GetParameter(2)

try:
    arcpy.AddMessage(sql)
    arcpy.AddMessage('select userid,username from people_demo where ' +str(sql))
    connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo') # put your database name, user name and password
    pepole_cursor = connection.cursor()

    

    pepole_cursor.execute('select userid,username from demo.people_demo where ' + str(sql))
    
    peole_records = pepole_cursor.fetchall()

    num_row = 0
    for people_record in peole_records:
        try:
            
            num_row = num_row + 1
            activity_cursor = connection.cursor()
                    
            activity_cursor.execute('select userid,fromuserid,participant,time,placeid from demo.activity_demo where userid =' +"'"+ people_record[0]+"'")
            activity_records = activity_cursor.fetchall()

            nxg,num_visit,num_act,num_node= AnalyzeData.CreateSocial(activity_records)
            num_clique,density,avg_clu  = AnalyzeData.CalculateSocial(nxg,num_node)
            
            sum_dis = AnalyzeData.CalculateDistance(people_record[0])
            
            arcpy.AddMessage("-------- " + str(num_row))
            arcpy.AddMessage("People ID: "+people_record[0])
            arcpy.AddMessage("number of visits: " + str(num_visit))
            arcpy.AddMessage("number of activities: " + str(num_act))
            arcpy.AddMessage("number of nodes: " + str(num_node))
            arcpy.AddMessage("number of cliques: " + str(num_clique))
            arcpy.AddMessage("density of network: " + str(density))

            arcpy.AddMessage("average clustering coefficient: " + str(avg_clu))
            
            if display:
                pos=nx.spring_layout(nxg)
                nx.draw(nxg,pos)
                nx.draw_networkx_labels(nxg,pos,font_size=20,font_family='sans-serif')
                plt.show()
            
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            arcpy.AddError(''.join('!! ' + line for line in lines) ) 
            logger.info(''.join('!! ' + line for line in lines) )
            
    connection.close()
    
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    arcpy.AddError( ''.join('!! ' + line for line in lines))  
    logger.info(''.join('!! ' + line for line in lines) )
