import json
from json import JSONEncoder
from os.path import join, dirname
import json_fix

# same file, or different file
class YOUR_CLASS:
    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return self.__dict__
        return "a built-in object that is natually json-able"

result = [ 1, 2, YOUR_CLASS() ]
__dirname__ = dirname(__file__)
with open(join(__dirname__, '3.json'), 'w') as outfile:
    json.dump(result, outfile)