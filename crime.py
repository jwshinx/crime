class Crime:
  def __init__(self, **kwargs):
    #self.make_each_element_string(kwargs)
    print("---> Crime 0: " + str(kwargs))
    print("---> Crime 0.1: " + str(type(kwargs)))
    self.load_attribute_values(kwargs)

  def load_attribute_values(self, adict):
    string_only_json = json.dumps(adict) # only string values; no ints
    print("---> Crime 1: " + str(string_only_json))
    self.__dict__.update(json.loads(string_only_json)) # make them methods
    print("---> Crime 2: " + str(self))
    print("---> Crime 3: " + str(type(self.__dict__)))


