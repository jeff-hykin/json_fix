# What is this?

A patch to the built-in python `json` object that allows classes to specify how they should be serialized.

# Why?

Because sometimes external code uses something like
```
import json
json.dumps(list_containing_your_object)
```
And it simply throws an error no matter how you customize your object

# How do I use this?

`pip install json-fix`

```python
import json_fix # import this before the JSON.dumps gets called

# same file, or different file
class YOUR_CLASS:
    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return self.__dict__
        return "a built-in object that is natually json-able"
```

If you want control over classes that are defined externally (datetime, numpy.array, tensor, etc), use the override_table
```python
import json_fix # import this before the JSON.dumps gets called
import json
import pandas as pd

SomeClassYouDidntDefine = pd.DataFrame

# create a boolean function for identifying the class
class_checker = lambda obj: isinstance(obj, SomeClassYouDidntDefine)
# then assign it to a function that does the converting
json.override_table[class_checker] = lambda obj_of_that_class: json.loads(obj_of_that_class.to_json())

json.dumps([ 1, 2, SomeClassYouDidntDefine() ], indent=2)
```
