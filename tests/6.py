import json
from json import JSONEncoder
from os.path import join
import json_fix

# same file, or different file
class YOUR_CLASS(dict):
    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return self.__dict__
        return "a built-in object that is natually json-able"

result = [ 1, 2, YOUR_CLASS() ]
with open("tests/test6.json", 'w') as the_file:
    the_file.write(f'''json.dumps(result) = {json.dumps(result)}''')