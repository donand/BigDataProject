# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:00:28 2017

@author: Riccardo
"""
import os
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

json_tmp = []
file_path = os.getcwd() + '\\Data\\fuorisalone_2016_socialnetwork_MDWRecordedData\\'
flist = [fname for fname in os.listdir(file_path) if fname.endswith('.rdf')]
for fname in flist:
    tmp = open(file_path + fname, encoding="UTF-8")
    g = Graph().parse(data=tmp.read())
    json_tmp.append(g.serialize(format='json-ld', indent=4))
    tmp.close()

#out = open(os.getcwd() + '\\Data\\social_data.json', 'w')
#out.writelines(str(json_tmp))
out.close()