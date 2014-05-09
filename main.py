#!/usr/bin/env python

import boto.rds
import mysql.connector
import os
import cleaner
import datetime

def get_connection():
  conn = boto.rds.connect_to_region(
    os.getenv('JWS_AWS_RDS_REGION'), 
    aws_access_key_id=os.getenv('JWS_AWS_ACCESS_KEY_ID'), 
    aws_secret_access_key=os.getenv('JWS_AWS_SECRET_ACCESS_KEY')
    )
  dbinstance = conn.get_all_dbinstances(os.getenv('JWS_AWS_RDS_DBINSTANCE'))
  conn = boto.rds.connect_to_region(
    os.getenv('JWS_AWS_RDS_REGION'), 
    os.getenv('JWS_AWS_ACCESS_KEY_ID'), 
    os.getenv('JWS_AWS_SECRET_ACCESS_KEY')
  )
  dbinstance = conn.get_all_dbinstances(os.getenv('JWS_AWS_RDS_DBINSTANCE'))

  #red = dbinstance[0]
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
  with open('sample.csv','r') as data:
    for each_line in data:
      values = each_line.split(',')
      #for i in range(len(values)):
      #  print(str(i+1) + ". " + str(values[i]))
      #print("")  
except IOError as err:
  print("An error! " + str(err))

#print("---> ENV VAR 1: " + str(ENV))
if __name__ == "__main__":
  obj = cleaner.DictCleaner(make='"hon"da"',year=2004)
  assert obj.make == 'honda'
  assert obj.year == 2004

  lobj = cleaner.ListCleaner(['"Burglary"', 2222, "111 Lakeshore", 37.783749, -122.2323, "2013-09-14 02:20:00"])
  assert lobj.crime == 'Burglary'
  assert lobj.beat == 2222
  assert lobj.address == "111 Lakeshore"
  assert lobj.lat == 37.783749
  assert lobj.lon == -122.2323
  assert lobj.datetime == datetime.datetime.strptime("2013-09-14 02:20:00","%Y-%m-%d %H:%M:%S")
  
