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
  fmt = '%Y-%m-%d %H:%M:%S %Z'
  cur, cnx = get_cursor()
  with open('logs/raw_crimes_inserter.log', 'a') as log_file:
    with open('data/crime-data.csv','r') as infile:
      data_reader = reader(infile, delimiter=',', quotechar='"')
      for row in data_reader:
        match = re.search(r'Case Number', row[0])
        if not match:
          obj = cleaner.ListCleaner(row)
          curr_time = datetime.datetime.now()
          log_file.write(str(curr_time.strftime(fmt)) + 
            str(obj.case_number) + ' : ' + str(obj.datetime) + '\n')
          cur.execute(obj.insert_statement(), obj.data_as_tuple())      
  cnx.commit()
  cur.close()
  cnx.close()
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
      "Saturday", "02:20", "BURGLARY", "20X", "90099", "1800 block of 28th Avenue",
      37.783749, -122.225523,
      "Street", "http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602"
    ])

  assert lobj.case_number == "13-047046"
  assert lobj.crime_type == 'BURGLARY'
  assert lobj.crime == "BURGLARY-FORCIBLE ENTRY"
  assert lobj.address == "1800 block of 28th Avenue"
  assert lobj.city == "90099"
  assert lobj.accuracy == "Street"
  assert lobj.beat == "20X"
  assert lobj.lat == 37.783749
  assert lobj.lon == -122.225523
  assert lobj.datetime == datetime.datetime.strptime("2013-09-14 02:20:00","%Y-%m-%d %H:%M:%S")
  assert lobj.url == "http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602"
  #assert lobj.data_as_tuple == \
  #('13-047046', 'BURGLARY-FORCIBLE ENTRY', datetime.datetime(2013, 9, 14, 2, 20), 'BURGLARY', '20X', '1800 block of 28th Avenue', ' Oakland 94601', '37.783749', '-122.225523', 'Street', 'http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602\n')
    #('13-047046', 'BURGLARY-FORCIBLE ENTRY',
    #datetime.datetime(2013, 9, 14, 2, 20),'BURGLARY','20X','1800 block of 28th Avenue',
    #' Oakland 94601','37.783749','-122.225523','Street',
    #'http://oakland.crimespotting.org/crime/2013-09-14/Burglary/278602\n')
  #print( str(lobj.data_as_tuple))
