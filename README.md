# What is this?

A pip module that lets you define a `__json__` method, that works like `toJSON` from JavaScript.<br>
(e.g. it magically gets called whenever someone does `json.dumps(your_object)`)

From a technical perspective, this module is a safe, backwards-compatible, reversable patch to the built-in python `json` object that allows classes to specify how they should be serialized.

# Why?

Because sometimes someone eles's code (e.g. a pip module) tries to serialize your object, like
```python
import json
json.dumps(list_containing_your_object)
```
And you'd have to fork their code to make it not throw an error.

# How do I use this tool?

`pip install json-fix`

```python
import json_fix # import this any time (any where) before the JSON.dumps gets called

# same file, or different file
class YOUR_CLASS:
    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return self.__dict__
        return "a built-in object that is natually json-able"
```

# How do I change how imported classes (numpy array, dataframe, etc) are jsonified?

There's 2 ways; the aggressive `override_table` or the more collaboration-friendly `fallback_table`. Note: some really powerful stuff can be done safely with the fallback table!

## Override Table

**CAUTION!**
- The override table has such a high priority it will let you change how built in objects are serialized.
- Even if a class defines a `.__json__()` method, the `json.override_table` will take priority.
- The order of keys matters a lot. The last entry takes the highest priority (this lets us override pip modules even if they try using the override table).


The override table is a dictionary.
It has "check functions" as keys, and jsonifiers as values. 

```python
import json_fix # import this before the JSON.dumps gets called
import json
import pandas as pd

SomeClassYouDidntDefine = pd.DataFrame

# create a boolean function for identifying the class
check_func = lambda obj: isinstance(obj, SomeClassYouDidntDefine)
# then assign it to a function that does the converting
json.override_table[check_func] = lambda obj_of_that_class: json.loads(obj_of_that_class.to_json())

json.dumps([ 1, 2, SomeClassYouDidntDefine() ], indent=2) # dumps as expected
```

## Fallback Table

If you want **all python classes to be jsonable by default**, we can easily do that with the fallback table. The logic is `if notthing in override table, and no .__json__ method, then check the fallback table`. 

```python
import json_fix # import this before the JSON.dumps gets called
import json

# a checker for custom objects
checker = lambda obj: hasattr(obj, "__dict__")
# use the __dict__ when they don't specify a __json__ method 
json.fallback_table[checker] = lambda obj_with_dict: obj_with_dict.__dict__

class SomeClass:
    def __init__(self):
        self.thing = 10

json.dumps([ 1, 2, SomeClass() ], indent=2) # dumps as expected
```

Like the override table, the most recently-added checker will have the highest priority. 
