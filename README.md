# What is this?

A patch to the buildit python `json` object that allows classes to specify how they should be serialized.

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
from json_fix import fix_it
fix_it() # only needs to be done once per runtime, NOT per-file

# same file, or different file
class YOUR_CLASS:
    def __json_dumps__(self, **options):
        # `options` will be same as the options given to json.dump()
        #     which currently are: (skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw))
        
        # YOUR CUSTOM CODE HERE
        #    you probably just want to do:
        #        return json.dumps(self.__dict__, **options)
        
        return "some kinda string"

```