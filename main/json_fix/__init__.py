import json
from json import JSONEncoder

# 
# one-time
#    monkey-patch the json dumper
#    this makes external calls to `import json` never know the difference
#    the object will just auto-serialize
# 

# check to make sure this only runs once
if not hasattr(JSONEncoder, "original_default"):
    from collections import OrderedDict
    
    json.override_table = OrderedDict() # this allows for adding serializers to classes you didnt define yourself
    json.fallback_table = OrderedDict() # this allows for adding generic methods like using str(obj) or obj.__dict__
    # 
    # add patch for __json__
    # 
    def wrapped_default(self, obj):
        # 
        # first check the override_table
        # 
        for each_checker in reversed(json.override_table.keys()):
            type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
            callable_check_matches = not isinstance(each_checker, type) and callable(each_checker) and each_checker(obj)
            if type_matches or callable_check_matches:
                custom_converter_function = json.override_table[each_checker]
                output = custom_converter_function(obj)
                return output
        
        # 
        # then check the __json__ method
        # 
        if hasattr(obj.__class__, "__json__"):
            getattr(obj.__class__, "__json__", wrapped_default.default)(obj)
        
        # 
        # then check the fallback_table
        # 
        for each_checker in reversed(json.fallback_table.keys()):
            type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
            callable_check_matches = not isinstance(each_checker, type) and callable(each_checker) and each_checker(obj)
            if type_matches or callable_check_matches:
                custom_converter_function = json.fallback_table[each_checker]
                output = custom_converter_function(obj)
                return output
        return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)

    wrapped_default.default = JSONEncoder().default
    # apply the patch
    JSONEncoder.original_default = JSONEncoder.default
    JSONEncoder.default = wrapped_default

def fix_it(): pass # to support the old interface 