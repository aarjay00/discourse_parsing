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

from os import listdir
from os.path import isfile, join
discourseFileCollection= [ dataLocation+str(f) for f in listdir(dataLocation) if isfile(join(dataLocation,f)) ]
discourseFileCollection=folderWalk(dataLocation)




def create_graph(currNode , nodeDict , graph,sentence,wordList):
#	print "\t"*nodeDict[currNode].nodeLevel,currNode
	for child in nodeDict[currNode].childList:
		vertexA=currNode+"_"+get_full_node_label(nodeDict[currNode],sentence,wordList)
		vertexB=child+"_"+get_full_node_label(nodeDict[child],sentence,wordList)
#		print vertexA,vertexB
		edge = pydot.Edge(vertexA,vertexB , label=" "+nodeDict[child].nodeRelation+" ")
#		print edge
		graph.add_edge(edge)
	for child in nodeDict[currNode].childList:
		graph=create_graph(child,nodeDict,graph,sentence,wordList)
	return graph

def get_full_node_label(node,sentence,wordList):
	chunkNum=node.chunkNum
	if(chunkNum==-1):
		return ""
	label=""
	chunk=sentence.chunkList[chunkNum]
	i=0
	for pos in chunk.wordNumList:
		label=label+"_"+wordList[pos].word
		i+=1
	label=label.replace(" ","")
	label=label.replace("/","")
	label=label.replace("?","")
	label=label.replace("'","")
	label=label.replace("\"","")
	label=label.replace(" ","")
	label=label.replace(":","")
	label=label.replace(";","")
	label=label.replace("(","")
	label=label.replace(")","")
	label=label.replace(",","")
	label=label.replace(".","")
	label=label.replace("-","")
	label=label.replace("\n","")
	label=label.replace("\r","")
#	print repr(label)
	return label

for discourseFileLocation in discourseFileCollection:
	discourseFileInst=loadModel(discourseFileLocation)
	print discourseFileInst.rawFileName
	rawFileName=discourseFileInst.rawFileName.split("/")
	filePath=""
	for part in rawFileName:
		if(part.startswith("Section") or filePath!="" ):
			filePath=filePath+part+"/"
	filePath="dependencyTreeGraph/"+filePath
	createDirectory(filePath)
	sentenceList=discourseFileInst.sentenceList
	wordList=discourseFileInst.globalWordList
	for sentence in sentenceList:
		graph = pydot.Dot(graph_type='graph')
		rootNode=sentence.rootNode
		nodeDict=sentence.nodeDict
		print rootNode
		for node in rootNode:
			print "creating"
			graph=create_graph(node,nodeDict,graph,sentence,wordList)
			graph.write_png(filePath+"/"+str(sentence.sentenceNum)+".png")
