'''
Created on Dec 12, 2014
This script provides basic functions for the other tools.
The database name, database admin name, table names are manually typed. you need to change them based on your system settings.

'''

import networkx as nx
import matplotlib.pyplot as plt
import psycopg2

import logging
import traceback
import sys

import pysal
import datetime
# import pyproj



import arcpy
'''
handle log
'''

logger = logging.getLogger('analyzedata')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('analyze.log')
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



def CreateSocial(records):
    '''
    create social network for selected records
    '''
    try:
        nxg = nx.Graph()
        num_act = 0
        people = []
        user_date_list = []
        for record in records:

            user_date_list.append(record[0]+record[3][:10]+record[4])
            num_act = num_act +1        

            people = [tag_user_id['id']
                      for tag_user_id in record[2]]
            people.append(record[0])
            people.append(record[1])
            unique_people = list(set(people))
            
            for people1 in unique_people:
                for people2 in unique_people:
                    if people1 <> people2:
                        nxg.add_edge(people1,people2)

        num_visit = len(set(user_date_list))
        # remove parallel edges        
        nxg=nx.Graph(nxg)
        num_node = nxg.number_of_nodes()


        
        return nxg,num_visit,num_act,num_node
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  # Log it or whatever here
        logger.info(''.join('!! ' + line for line in lines) )

def CalculateSocial(nxg,num_node):
    '''
    calculate network measures for an input network
    '''
    try:
        if num_node > 0:

            density = nx.density(nxg)
            cliques = [c for c in nx.find_cliques(nxg)]
            num_clique = len(cliques)
            avg_clu = nx.average_clustering(nxg)

        else:
            density = 0.0
            num_clique = 0
            avg_clu = 0.0
    #         
        return num_clique,density,avg_clu 
    
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )
        
def VisualizeSocial(nxg):
    '''
    visualize the input network, display the network in python or ArcGIS
    
    '''
    try:
        pos=nx.spring_layout(nxg)
        nx.draw(nxg,pos)
        nx.draw_networkx_labels(nxg,pos,font_size=20,font_family='sans-serif')

        plt.show()

    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )
        

def CalculateDistance(people_record):
    '''
    calculate total travel distance for each input user
    '''
    try:
        connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo') # change this to your database name, user name and password
        location_cursor = connection.cursor()
        geod = pyproj.Geod(ellps = 'WGS84')
        location_cursor.execute('select latitude,longitude from demo.activity_demo where user_id =' +"'"+ people_record+"'"+ "and latitude >-999 and create_time <> 'None'" + 'order by create_time')
        location_records = location_cursor.fetchall()
        sum_dis = 0.0
        i = 0
        for location_record in location_records:
            if (i == 0):
                current_dis = 0.0
                x1 = None
                y1 = None
            else:
                x2 = location_record[0]
                y2 = location_record[1]
                try:
                    angle1,angle2,current_dis = geod.inv(x1,y1,
                                                     x2,y2) 
                except:
                    print x1,y1
                    print x2,y2
                    current_dis = 0.0
                    continue

            sum_dis = sum_dis + current_dis
            i = i +1
            x1 = location_record[0]
            y1 = location_record[1]
        return sum_dis

    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )

        
def UpdateEgoSocialNetwork():
    '''
    calculate social network measures for people, namely the peoplesocial table. 
    
    '''
    try:
        connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo')# change this to your database name, user name and password
        pepole_cursor = connection.cursor()
        pepolesocial_cursor = connection.cursor()
        
        
        pepole_cursor.execute('select id, name from demo.people_demo')
        peole_records = pepole_cursor.fetchall()
        
       
        for people_record in peole_records:
            try:
                activity_cursor = connection.cursor()
                        
                activity_cursor.execute('select user_id,from_user_id,tag_id,create_time,place_id from demo.activity_demo where user_id =' +"'"+ people_record[0]+"'"+ "and latitude >-999 and create_time <> 'None'")
                activity_records = activity_cursor.fetchall()

                nxg,num_visit,num_act,num_node= CreateSocial(activity_records)
                num_clique,density,avg_clu  = CalculateSocial(nxg,num_node)

                
                sum_dis = CalculateDistance(people_record[0])
               
                pepolesocial_cursor.execute('INSERT INTO demo.peoplesocial_demo (user_id,user_name,num_node,num_act,num_visit,num_clique,density,avg_clu,sum_dis)'
                                            ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                            [people_record[0],people_record[1],num_node,num_act,num_visit,num_clique,density,avg_clu,sum_dis])

            except psycopg2.IntegrityError:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  
                    logger.info(''.join('!! ' + line for line in lines) )
                    
            except :
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  
                    logger.info(''.join('!! ' + line for line in lines) )

            activity_cursor.close()
            connection.commit()
        pepolesocial_cursor.close
        pepole_cursor.close()
        connection.close()


    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )
        

def CreatePlaceSocial():
    '''
    calculate social network measures for each place, namely the placesocial table
    '''
    try:
        connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo')# change this to your database name, user name and password
        place_cursor = connection.cursor()
        placesocial_cursor = connection.cursor()
        
        
        place_cursor.execute('select placeid,placename from demo.place_demo')
        place_records = place_cursor.fetchall()

        for place_record in place_records:
            nxg = nx.Graph()
            try:
                activity_cursor = connection.cursor()
                        
                activity_cursor.execute('select userid,fromuserid,participant,time,placeid from demo.activity_demo where placeid =' +"'"+ place_record[0]+"'")
                activity_records = activity_cursor.fetchall()

                nxg,num_visit,num_act,num_node= CreateSocial(activity_records)

                num_clique,density,triangles,trans,avg_clu  = CalculateSocial(nxg,num_node)
                placesocial_cursor.execute('INSERT INTO demo.placesocial_demo (placeid,placename,'

                                           'num_node,num_act,num_visit,'
                                            'num_clique,density,triangles,trans,avg_clu)'
                                            ' VALUES(%s,%s,%s,'

                                            '%s,%s,%s,%s,%s,%s,%s)',
                                            (place_record[0],place_record[1],

                                             num_node,num_act,num_visit,
                                            num_clique,density,triangles,trans,avg_clu))

            except psycopg2.IntegrityError:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  
                    logger.info(''.join('!! ' + line for line in lines) )
    
                
            except :
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  
                    logger.info(''.join('!! ' + line for line in lines) )

    


            activity_cursor.close()
            connection.commit()
        placesocial_cursor.close
        place_cursor.close()
        connection.close()


    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )
        

def UpdateZ():
    '''
    calculate Z input activity table
    the z indicates the temporal distance from the activity date to the current time 
    '''
    try:
        connection = psycopg2.connect(dbname = 'postgis_25_sample', user = 'demo',password='demo')# change this to your database name, user name and password
        cursor = connection.cursor()
        activity_cursor = connection.cursor()
        
        activity_cursor.execute('select create_time,id from demo.activity_demo')

        activity_records = activity_cursor.fetchall()
        for activity_record in activity_records:
            if activity_record[0].strip()<> 'None':
                record_time = datetime.datetime(int(activity_record[0][:4]),int(activity_record[0][5:7]),int(activity_record[0][8:10]),int(activity_record[0][11:13]),int(activity_record[0][14:16]))
                time_delta = datetime.datetime.now()-record_time
                print time_delta.days

                
                cursor.execute('update demo.activity_demo set z = '+str(time_delta.days)+' where id = '+ "'"+activity_record[1]+"'")
    
            else:
                cursor.execute('update demo.activity_demo set z = '+str(-1)+' where id = '+ "'"+activity_record[1]+"'")
                
        connection.commit()
        cursor.close()
        activity_cursor.close()
        connection.close()
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print ''.join('!! ' + line for line in lines)  
        logger.info(''.join('!! ' + line for line in lines) )




