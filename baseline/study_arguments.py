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
from annotated_data import *
from feature import *




discourseFileCollection=loadModel("processedData/annotatedData")


def completeChunk(posList,wordList):
	start=False
	end=False
	if(posList[0]==0 or wordList[posList[0]-1].chunkNum!=wordList[posList[0]].chunkNum):
		start=True
	if(posList[-1]==len(wordList)-1 or wordList[posList[-1]+1].chunkNum!=wordList[posList[-1]].chunkNum):
		end=True
	return (start,end)
def convertPostList(posList,wordList):
	span=""
	for pos in posList:
		span=span+" " + wordList[pos]
	return span[1:]
def print_span(posList,wordList):
	for pos in posList:
		print wordList[pos].word,wordList[pos].chunkNum,
	print ""

for discourseFileInst in discourseFileCollection:
	print "-"*60
	relationList=discourseFileInst.relationList
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList
	for relation in relationList:
		if(relation.relationType!="Explicit"):
			continue
		print relation.relationType
		print "Arg1",relation.arg1List
		print "conn",relation.connList
		print "Arg2",relation.arg2List
		complete=completeChunk(relation.arg2List,wordList)
		print complete
		if(not complete[1]):
			print_span(relation.arg2List,wordList)
			print_span(sentenceList[wordList[relation.arg2List[0]].sentenceNum].wordNumList,wordList)
