import bson
import json

with open('Data\\fuorisalone_2016_anonymous_appdata\\event.bson', 'rb') as f:
    coll_raw = f.read()

a = bson.loads(coll_raw)
type(a)
print(a)

json_array = json.dumps(a)
del a['_id']

out = open('Data\\fuorisalone_2016_anonymous_appdata\\event.json', 'w')
out.writelines(json_array)