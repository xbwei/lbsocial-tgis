'''
Created on Dec 21, 2014

This script support the calculate place social tool in ArcGIS
It will take the selected places' records, and calculate the network measures of the selected places.

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

logger = logging.getLogger('CulcateLSocial')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('CulcateLSocial.log')
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

# Script arguments
Feature_Set = arcpy.GetParameterAsText(0)


places = arcpy.GetParameterAsText(1)

display = arcpy.GetParameter(2)




try:
    
    selectedfeatures = arcpy.SelectLayerByLocation_management(places, "COMPLETELY_WITHIN", Feature_Set, "", "NEW_SELECTION")
    
    cursor = arcpy.SearchCursor(places)
    connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo') # put your database name, user name and password
    activity_cursor = connection.cursor()

    nxg = nx.Graph()
    num_act = 0
    people = []
    user_date_list = []
    placelist=[]
    for row in cursor:
        try:
            placelist.append(row.getValue("placename"))
            activity_cursor.execute('select userid,fromuserid,participant,time,placeid from demo.activity_demo where placeid =' +"'"+ row.getValue("placeid")+"'")
            activity_records = activity_cursor.fetchall()
            
            for activity_record in activity_records:

                user_date_list.append(activity_record[0]+activity_record[3][:10]+activity_record[4])
                num_act = num_act +1        
                people = [tag['id'] for tag in activity_record[2]]
                people.append(activity_record[0])
                people.append(activity_record[1])

                unique_people = list(set(people))
                    
                for people1 in unique_people:
                    for people2 in unique_people:
                        if people1 <> people2:
                            nxg.add_edge(people1,people2)
            

        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            arcpy.AddError( ''.join('!! ' + line for line in lines))  
            logger.info(''.join('!! ' + line for line in lines) )
        
    num_visit = len(set(user_date_list))
    # remove duplicated edges
    nxg=nx.Graph(nxg)
    num_node = nxg.number_of_nodes()
 
 
    num_clique,density,avg_clu  = AnalyzeData.CalculateSocial(nxg,num_node)
 
     
    arcpy.AddMessage("--------" )
    arcpy.AddMessage("number of places: " + str(len(placelist)))

    arcpy.AddMessage("number of visits: " + str(num_visit))
    arcpy.AddMessage("number of activities: " + str(num_act))
    arcpy.AddMessage("number of nodes: " + str(num_node))
    arcpy.AddMessage("number of cliques: " + str(num_clique))
    arcpy.AddMessage("density of network: " + str(density))
    arcpy.AddMessage("average clustering coefficient: " + str(avg_clu))
    arcpy.AddMessage("place names: ")
    for place in placelist:
        try:
            arcpy.AddMessage('\t' + str(place).encode('ascii','ignore'))
        except UnicodeEncodeError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            arcpy.AddWarning('\tcan not display special name')  
            logger.info(''.join('!! ' + line for line in lines) )
            continue
        except :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            arcpy.AddError( ''.join('!! ' + line for line in lines))  
            logger.info(''.join('!! ' + line for line in lines) )
             
    if display:
        pos=nx.spring_layout(nxg)
        nx.draw(nxg,pos)
        nx.draw_networkx_labels(nxg,pos,font_size=20,font_family='sans-serif')
        plt.show()
    

    connection.close()            

except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    arcpy.AddError( ''.join('!! ' + line for line in lines))  
    logger.info(''.join('!! ' + line for line in lines) )