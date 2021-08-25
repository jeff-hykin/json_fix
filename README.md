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
from json_fix import fix_it; fix_it() # only needs to be done once per runtime, NOT per-file

# same file, or different file
class YOUR_CLASS:
    def __json__(self):
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return self.__dict__
        return "a built-in object that is natually json-able"
```

If you want control over that are defined externally (datetime, numpy.array, tensor, etc), use the override_table
```python
from json_fix import fix_it; fix_it() # only needs to be done once per runtime, NOT per-file
import json
import pandas as pd

SomeClassYouDidntDefine = pd.DataFrame

# the key is a lambda checker, the value is the converter if the check==True
class_checker = lambda obj: isinstance(obj, SomeClassYouDidntDefine)
# the lambda here (the converter) needs to return a string
json.override_table[class_checker] = lambda obj_of_that_class: json.loads(obj_of_that_class.to_json())

json.dumps([ 1, 2, SomeClassYouDidntDefine() ], indent=2)
```