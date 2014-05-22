import json
import datetime

class DictCleaner:
  def __init__(self, **kwargs):
    new_dict = {}
    for item in kwargs.keys():
      new_dict[item] = self.sanitize(kwargs[item])    
    self.load_attribute_values(new_dict)

  def load_attribute_values(self, adict):
    string_only_json = json.dumps(adict) # only string values; no ints
    self.__dict__.update(json.loads(string_only_json)) # make them methods

  def sanitize(self, value):
    if isinstance(value, str):
      return value.strip().replace('"', '')   
    #elif isinstance(value, float): 
    else:
      return value

class ListCleaner:
  def __init__(self, args):
    clean_list = []
    for item in args:
      if isinstance(item, str):
        clean_list.append(item.replace('"', ''))
      else:  
        clean_list.append(item)
    #print("---> ListCleaner init: " + str(clean_list))
    self.case_number = clean_list[0]
    self.crime = clean_list[1]
    self.datetime = self.to_datetime(clean_list[2])
    self.crime_type = clean_list[5]

    self.beat = clean_list[6]
    self.address = clean_list[8]
    self.city = clean_list[9]
    self.lat = clean_list[10]
    self.lon = clean_list[11]
    self.accuracy = clean_list[12]
    self.url = clean_list[13]
    
  def remove_quotes(self, value):
    if isinstance(value, str):
      return value.strip().replace('"', '')   
    else:
      return value    

  def to_datetime(self, value):
    try:
      return datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
    except ValueError as err:
      print("Date to string failed. " + str(err))
      return ""

  def data_as_tuple(self):
    return (self.case_number, self.crime, self.datetime, self.crime_type, 
      self.beat, self.address, self.city, self.lat, 
      self.lon, self.accuracy, self.url, 0, datetime.datetime.now(),
      datetime.datetime.now())

  def insert_statement(self):
    return "INSERT INTO raw_crimes (case_number, description, timestamp, crime_type, \
      beat, address_description, zip, latitude, longitude, accuracy, url, \
      processed, created_at, updated_at) \
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
   