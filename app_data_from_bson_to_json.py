import bson
import json

with open('Data/fuorisalone_2016_anonymous_appdata/anon_db/event.bson', 'rb') as f:
    coll_raw = f.read()

a = bson.loads(coll_raw)
type(a)
print(a)

del a['_id']
json_array = json.dumps(a)
type(json_array)

out = open('Data/fuorisalone_2016_anonymous_appdata/anon_db/event.json', 'w')
out.writelines(json_array)