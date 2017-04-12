# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:00:28 2017

@author: Riccardo
"""
import os
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import json
from pyld import jsonld

json_tmp = []
file_path = os.getcwd() + '\\Data\\fuorisalone_2016_socialdata\\'
flist = [fname for fname in os.listdir(file_path) if fname.endswith('.rdf')]
for fname in flist[:100]:
    tmp = open(file_path + fname, encoding="UTF-8")
    g = Graph().parse(data=tmp.read())
    json_tmp.append(g.serialize(format='json-ld', indent=4))
    tmp.close()

#compacted = jsonld.compact(json_tmp)
#type(compacted)
#out = open(os.getcwd() + '\\Data\\social_data.json', 'w')
#s = unicode(json_tmp).encode('utf8')
#out.writelines(json_tmp)
#out.close()
'''
json_tmp
len(json_tmp)
type(json_tmp)
json_tmp[0]
type(json_tmp[0])
'''


out = open(os.getcwd() + '\\Data\\social_data.json', 'w')
#json.dumps(json_tmp, ensure_ascii = False)

s = json_tmp[0].decode('utf-8', "ignore")

out.writelines(s)
out.close()