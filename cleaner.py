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
    #print("---> DictCleaner 1: " + str(string_only_json))
    #print("---> DictCleaner 2: " + str(self))
    #print("---> DictCleaner 3: " + str(type(self.__dict__)))

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
    print("---> ListCleaner init: " + str(clean_list))

    self.crime = clean_list[0]
    self.beat = clean_list[1]
    self.address = clean_list[2]
    self.lat = clean_list[3]
    self.lon = clean_list[4]
    self.datetime = self.to_datetime(clean_list[5])

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

   