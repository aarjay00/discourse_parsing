#!/usr/bin/
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os 
import codecs

import  cPickle as pickle

import re
from extract_relations import *

def folderWalk(folderPath):
	import os
	fileList = []
	for dirPath , dirNames , fileNames in os.walk(folderPath) :
		for fileName in fileNames :
			fileList.append(os.path.join(dirPath , fileName))
	return fileList
def findAllOccurences(delimList,inputString):
	searchKey=""
	for delim in delimList:
		searchKey+="|"
		searchKey+=delim
	searchKey=searchKey[1:]
#	print searchKey
	return [m.start() for m in re.finditer(searchKey, inputString)]
def getDiscourseUnit(text,delimList):
	delimString=""
	for i in delimList:
		delimString+=i+" | "
	delimString=delimString[:len(delimString)-3]
	return re.split(delimString,text)
def loadConnList(fileName,split=False):
	fd=open(fileName,"r")
	connList=[]
	for conn in fd.readlines():
		conn=conn[:-1]
		if split:
			connList.append(tuple(conn.split("..")))
		else:
			connList.append(conn)
	return connList
def extractRelation(filePath):
	connTypeCounts = {'Explicit':0 , 'Implicit':0 ,'AltLex':0 , 'EntRel':0 , 'NoRel':0}
	senseDict = {}
	explicitConnDict = {}
	altlexConnDict = {}
	implicitConnDict = {}
	connSenseIndex = {}
	relationList=[]
	rawFD=open(filePath,"r")
	annFD=open(filePath.replace("/raw/","/ann/"),"r")
	[relationList , connTypeCounts, [explicitConnDict , implicitConnDict , altlexConnDict] , senseDict, connSenseIndex ] = processAnnFile( relationList , connTypeCounts , explicitConnDict, implicitConnDict , altlexConnDict, senseDict , connSenseIndex ,annFD , rawFD)
	writeResults(relationList,filePath)
	return relationList
	
def findIndexList(key,l):
	try:
		return l.index(key)
	except ValueError:
		return -1;
def writeResults(discourseRelationList,filePath):
	filePath=filePath.split("raw/")[1]
	filePath="output/"+filePath
	if not os.path.exists(os.path.dirname(filePath)):
		os.makedirs(os.path.dirname(filePath))
	outFD=open(filePath,"w")
	for discourseRelation in discourseRelationList:
		string=""
		if(discourseRelation.relationType=="Explicit"):
			string+=("Explicit|"+discourseRelation.connSpan+"|Wr|Comm|Null|Null||")
			string+=("|"+discourseRelation.sense+"||||||")
			string+=(discourseRelation.arg1Span+"|Inh|Null|Null|Null||")
			string+=(discourseRelation.arg2Span+"|Inh|Null|Null|Null||")
		elif(discourseRelation.relationType=="Implicit"):
			string+=("Implicit||Wr|Comm|Null|Null||")
			string+=(discourseRelation.conn+"|"+discourseRelation.sense+"||||||")
			string+=(discourseRelation.arg1Span+"|Inh|Null|Null|Null||")
			string+=(discourseRelation.arg2Span+"|Inh|Null|Null|Null||")
		elif(discourseRelation.relationType=="EntRel"):
			string+=("EntRel|||||||")
			string+=("|||||||")
			string+=(discourseRelation.arg1Span+"||||||")
			string+=(discourseRelation.arg2Span+"||||||")
		elif(discourseRelation.relationType=="NoRel"):
			string+=("NoRel|||||||")
			string+=("|||||||")
			string+=(discourseRelation.arg1Span+"||||||")
			string+=(discourseRelation.arg2Span+"||||||")
		outFD.write(string+"\n")
	outFD.close()
def analyzeResults(goldFilePath,outputFilePath):

