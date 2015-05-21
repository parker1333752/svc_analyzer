import json

a = [1,2,3,4]
b = json.dumps(a)
print type(b)
print repr(b)

c = json.loads(b)
print type(c)
print repr(c)
