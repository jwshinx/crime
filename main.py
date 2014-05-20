#!/usr/bin/env python

import boto.rds
import mysql.connector
import os
import cleaner
import datetime
import re

"""
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
"""

try:
  with open('sample.csv','r') as data:
    for each_line in data:
      values = each_line.split(',')
      
      match = re.search(r'Case Number', values[0])
      if match:                      
        print 'found', match.group() ## 'found word:cat'
        print("")
      else:
        obj = cleaner.ListCleaner(values)
        print(str(obj.__dict__))
        print("")
      
        #for i in range(len(values)):
        #  print(str(i+1) + ". " + str(values[i]))
        #  print("")
      
    #cur, conn = get_cursor()
    #print(str(cur))
    #print(str(conn))
    #cur.close()
    #conn.close()
except IOError as err:
  print("An error! " + str(err))

#print("---> ENV VAR 1: " + str(ENV))
if __name__ == "__main__":
  obj = cleaner.DictCleaner(make='"hon"da"',year=2004)
  assert obj.make == 'honda'
  assert obj.year == 2004

  lobj = cleaner.ListCleaner(
    [
      "13-047046", "BURGLARY-FORCIBLE ENTRY", "2013-09-14 02:20:00",
      "Saturday", "02:20", "BURGLARY", "20X", "", "1800 block of 28th Avenue",
      "Oakland 94601", 37.783749, -122.225523,
      "Street", "http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602"
    ])

  assert lobj.case_number == "13-047046"
  assert lobj.crime_type == 'BURGLARY'
  assert lobj.crime == "BURGLARY-FORCIBLE ENTRY"
  assert lobj.city == "Oakland 94601"
  assert lobj.accuracy == "Street"
  assert lobj.beat == "20X"
  assert lobj.lat == 37.783749
  assert lobj.lon == -122.225523
  assert lobj.datetime == datetime.datetime.strptime("2013-09-14 02:20:00","%Y-%m-%d %H:%M:%S")
  assert lobj.url == "http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602"
