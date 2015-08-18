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
import os.path

def fileExists(filePath):
	return os.path.isfile(filePath)
def folderWalk(folderPath):
	import os
	fileList = []
	for dirPath , dirNames , fileNames in os.walk(folderPath) :
		for fileName in fileNames :
			fileList.append(os.path.join(dirPath , fileName))
	return fileList

def createDirectory(filePath):
	dirPath=os.path.dirname(filePath)
	print "here XXX",dirPath
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)
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
	fd=codecs.open(fileName,"r",encoding="utf-8")
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
	rawFD=codecs.open(filePath,"r",encoding="utf-8")
	annFD=codecs.open(filePath.replace("/raw/","/ann/"),"r",encoding="utf-8")
	[relationList , connTypeCounts, [explicitConnDict , implicitConnDict , altlexConnDict] , senseDict, connSenseIndex ] = processAnnFile( relationList , connTypeCounts , explicitConnDict, implicitConnDict , altlexConnDict, senseDict , connSenseIndex ,annFD , rawFD)
	writeResults(relationList,filePath)
	return relationList
	
def findIndexList(key,l):
	try:
		return l.index(key)
	except ValueError:
		return -1;

def getChunk(wordNum,wordList,sentenceList):
	return sentenceList[wordList[wordNum].sentenceNum].chunkList[wordList[wordNum].chunkNum]

def getChunkSeq(posList,wordList,sentenceList,unique=True):
	chunkSeq=[]
	prevChunkNum="No"
	for pos in posList:
		chunk=getChunk(pos,wordList,sentenceList)
		if(not unique or chunk.chunkTag!=prevChunkNum):
			chunkSeq.append(chunk)
			prevChunkNum=chunk.chunkTag
	print "checking",len(posList),len(chunkSeq)
	return chunkSeq

def getDependencySeq(posList,wordList,sentenceList,unique=True):
	chunkSeq=getChunkSeq(posList,wordList,sentenceList,unique)
	dependencySeq=[]
	for chunk in chunkSeq:
		nodeName=chunk.nodeName
		node=sentenceList[chunk.sentenceNum].nodeDict[nodeName]
		dependencySeq.append(node.nodeRelation)
	return dependencySeq

def getSpan(posList,wordList):
	span=""
	for pos in posList:
		span=span+" "+wordList[pos].word
	span=span[1:]
	return span
def writeResults(discourseRelationList,filePath):
	filePath=filePath.split("raw/")[1]
	filePath="output/"+filePath
	if not os.path.exists(os.path.dirname(filePath)):
		os.makedirs(os.path.dirname(filePath))
	outFD=codecs.open(filePath,"w",encoding="utf-8")
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
def exportModel(filePath,model):
	fileFD=codecs.open(filePath,"w",encoding="utf-8")
	pickle.dump(model,fileFD)
	fileFD.close()
def loadModel(filePath):
	fileFD=open(filePath,"rb")
	model=pickle.load(fileFD)
	fileFD.close()
	return model
def analyzeResults(goldFilePath,outputFilePath):
	print "hah"
