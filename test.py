# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:00:28 2017

@author: Riccardo
"""
import os
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

json_tmp = []
flist = [fname for fname in os.listdir('C:\Users\Riccardo\Desktop\RecordedData') if fname.endswith('.rdf')]
for fname in flist:
    tmp = open(fname)
    g = Graph().parse(data=tmp.read())
    json_tmp.append(g.serialize(format='json-ld', indent=4))
