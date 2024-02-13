import json
import json_fix

class Test(dict):
    def __json__(self):
        return 99

with open("tests/test4.json", "w") as f:
    json.dump([Test()], f)

# print(f'''test4, pt3, should print and throw error''')
# print(json.dumps(Test()))

# print(f'''test4, pt4, should print and throw error''')
# print(json.dumps([Test()]))