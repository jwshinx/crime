#!/usr/bin/env python

import boto.rds
import mysql.connector
import os
import cleaner
import datetime
import re
from csv import reader

def get_connection():
    conn = boto.rds.connect_to_region(
        os.getenv('JWS_AWS_RDS_REGION')
    )
    dbinstance = conn.get_all_dbinstances(os.getenv('JWS_AWS_RDS_DBINSTANCE'))
   
    cnx = mysql.connector.connect(
        user=os.getenv('JWS_AWS_RDS_DBINSTANCE_USER'), 
        password=os.getenv('JWS_AWS_RDS_DBINSTANCE_PASSWORD'), 
        database=os.getenv('JWS_AWS_RDS_DBINSTANCE_DATABASE'), 
        host=os.getenv('JWS_AWS_RDS_DBINSTANCE_HOST')
    )
    return cnx

def get_cursor():
    connection = get_connection()
    cursor = connection.cursor(buffered=True)  
    return cursor, connection

try:
    #app_dir = os.getcwd()
    app_dir = os.getenv('CRIME_PATH')
    with open(app_dir + '/log/zip_updater.log', 'a') as log_file:
        fmt = '%Y-%m-%d %H:%M:%S %Z'
        cnx = get_connection()
        cur = cnx.cursor(buffered=True)  
        cur2 = cnx.cursor(buffered=True)
        curr_time = datetime.datetime.now()
        log_file.write(str(curr_time.strftime(fmt)) + ' Start ' + '-'*55 + '\n')
        cur.execute("select id, case_number, zip, address_description \
            from raw_crimes \
            where address_description like '%%oakland 946%%' \
            and zip not like '%%9%%' limit 5")

        for (id, case_number, zip, address_description) in cur:
            temp_id = id
            #print("{}, {}, {} -- {}".format(id, case_number, zip, address_description))
            match = re.search(r'(\d){5}$', address_description)
            if match:
                zip_info = match.group(0)
                log_file.write(
                    "{} Zip info found {} {}. Zip updated to {}.\n".format(
                        str(curr_time.strftime(fmt)), 
                        id,
                        case_number, 
                        zip_info
                        )
                    ) 
                        
                cur2.execute("update raw_crimes \
                    set zip = %s where id = %s", (zip_info, temp_id))
            else:
               log_file.write(
                    "{} No zip found for {} {}\n".format(
                        str(curr_time.strftime(fmt)),
                        id,
                        case_number
                        )
                    )
        log_file.write(str(curr_time.strftime(fmt)) + ' End   ' + '-'*55 + '\n')
       
    cnx.commit()    
    cur.close()
    cur2.close()
    cnx.close()

except Exception, e:
    raise
else:
    pass
finally:
    pass