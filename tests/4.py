import json
import json_fix

class Test(dict):
    def __json__(self):
        return 99

with open("tests/test4_1.json", "w") as f:
    json.dump([Test()], f)

with open("tests/test4_2.json", "w") as f:
    json.dump(Test(), f)

with open("tests/test4_3.json", 'w') as the_file:
    the_file.write(str(json.dumps([Test()])))

with open("tests/test4_4.json", 'w') as the_file:
    the_file.write(str(json.dumps(Test())))