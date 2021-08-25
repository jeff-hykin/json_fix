def fix_it():
    # 
    # one-time
    #    monkey-patch the json dumper
    #    this makes external calls to `import json` never know the difference
    #    the object will just auto-serialize
    # 
    import json
    json.conversion_table = {} # this allows for adding serializers to classes you didnt define yourself
    json.fallback_table = {} # this allows for adding generic methods like using str(obj) or obj.__dict__
    json.original_dumps = json.dumps
    # create a new dump
    def json_dumps_wrapper(obj, **options):
        # extract the default argument so we can combine it with our own default argument
        default_argument = options.get("default", None)
        # create our own always-added default converter (wrapping the existing default argument if there is one)
        def default(obj):
            # 
            # first try the local override
            # 
            if callable(default_argument):
                try:
                    output = default_argument(obj, **options)
                    if type(output) == str:
                        return output
                except TypeError as error:
                    if error.startswith('Object of type ') and error.endswith('is not JSON serializable'):
                        pass
                    else:
                        raise error
            # 
            # then check the conversion_table
            # 
            for each_checker in reversed(json.conversion_table.keys()):
                type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
                callable_check_matches = callable(each_checker) and each_checker(obj)
                if type_matches or callable_check_matches:
                    custom_serial_function = json.conversion_table[each_checker]
                    output = custom_serial_function(obj)
                    if type(output) != str:
                        raise Exception(f'The in the json.conversion_table, a key ({each_checker}) matched a getting-dumped object {obj.__class__}, but the converter for that key {custom_serial_function} didnt return a string (and it needs to for serialization to work)')
                    return output
            
            # 
            # fallback on .__json_dumps__()
            # 
            if hasattr(obj, "__json_dumps__") and callable(obj.__json_dumps__):
                output = obj.__json_dumps__(**options)
                if type(output) != str:
                    raise Exception(f'The __json_dumps__() method for an {obj.__class__} object, didnt return a string. Please either edit the __json_dumps__() method to return a string, or (if you do not control the class) add key-value pair to json.conversion_table, for example:\n    json.conversion_table[{obj.__class__.__name__}] = lambda obj, **options: json.dumps(obj.__dict__, **options)')
                return output
            
            # 
            # fallback on regular json dumping
            # 
            err = None
            try:
                json.original_dumps(obj, **options)
            except TypeError as error:
                err = error
                if error.startswith('Object of type ') and error.endswith('is not JSON serializable'):
                    pass
                else:
                    raise error
            
            # 
            # fallback again using fallback_table (for default/generic custom-class behavor)
            # 
            for each_checker in reversed(json.fallback_table.keys()):
                type_matches = isinstance(each_checker, type) and isinstance(obj, each_checker)
                callable_check_matches = callable(each_checker) and each_checker(obj)
                if type_matches or callable_check_matches:
                    custom_serial_function = json.fallback_table[each_checker]
                    output = custom_serial_function(obj)
                    if type(output) != str:
                        raise Exception(f'The in the json.fallback_table, a key ({each_checker}) matched a getting-dumped object {obj.__class__}, but the converter for that key {custom_serial_function} didnt return a string (and it needs to for serialization to work)')
                    return output
            
            # throw error explaining why it cant be serialized
            raise TypeError(f"Object of {obj.__class__} (that is getting json serialized)\ndoesn't have a __json_dumps__(self, **options) method,\nand there is no entry in json.conversion_table\nex: json.conversion_table[ the_class ] = lambda obj, **options: str(obj)\nso the object currently can't be serialized")
        
        options["default"] = default
        return json.original_dumps(obj, **options)

    # overwrite the existing json.dumps for everyone
    json.dumps = json_dumps_wrapper
    # carry over the documentation for kwargs
    json.dumps.__doc__ = json.original_dumps.__doc__