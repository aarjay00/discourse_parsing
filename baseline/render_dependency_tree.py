#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
#from identify_connectives import *
from annotated_data import *
"""
pydot example 1
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot # import pydot or you're not going to get anywhere my friend :D

# first you create a new graph, you do that with pydot.Dot()
graph = pydot.Dot(graph_type='graph')

# the idea here is not to cover how to represent the hierarchical data
# but rather how to graph it, so I'm not going to work on some fancy
# recursive function to traverse a multidimensional array...
# I'm going to hardcode stuff... sorry if that offends you

if len(sys.argv)<2:
	print "Please give location of proccessed data"
	exit()

dataLocation = sys.argv[1]

discourseFileCollection=loadModel(dataLocation)


def create_graph(currNode , nodeDict , graph):
#	print "\t"*nodeDict[currNode].nodeLevel,currNode
	for child in nodeDict[currNode].childList:
		edge = pydot.Edge(currNode,child , label=" "+nodeDict[child].nodeRelation+" ")
		graph.add_edge(edge)
	for child in nodeDict[currNode].childList:
		graph=create_graph(child,nodeDict,graph)
	return graph


for discourseFileInst in discourseFileCollection:
	print discourseFileInst.rawFileName
	rawFileName=discourseFileInst.rawFileName.split("/")
	filePath=""
	for part in rawFileName:
		if(part.startswith("Section") or filePath!="" ):
			filePath=filePath+part+"/"
	filePath="dependencyTreeGraph/"+filePath
	print filePath
	createDirectory(filePath)
	sentenceList=discourseFileInst.sentenceList
	for sentence in sentenceList:
		graph = pydot.Dot(graph_type='graph')
		rootNode=sentence.rootNode
		nodeDict=sentence.nodeDict
#		print rootNode
		for node in rootNode:
			graph=create_graph(node,nodeDict,graph)
			graph.write_png(filePath+str(sentence.sentenceNum)+".png")

# let's add the relationship between the king and vassals
for i in range(3):
    # we can get right into action by "drawing" edges between the nodes in our graph
    # we do not need to CREATE nodes, but if you want to give them some custom style
    # then I would recomend you to do so... let's cover that later
    # the pydot.Edge() constructor receives two parameters, a source node and a destination
    # node, they are just strings like you can see
    edge = pydot.Edge("king", "lord%d" % i)
    # and we obviosuly need to add the edge to our graph
    graph.add_edge(edge)

# now let us add some vassals
vassal_num = 0
for i in range(3):
    # we create new edges, now between our previous lords and the new vassals
    # let us create two vassals for each lord
    for j in range(2):
        edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
        graph.add_edge(edge)
        vassal_num += 1

# ok, we are set, let's save our graph into a file
graph.write_png('example1_graph.png')

# and we are done!
