#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
import codecs
sys.setdefaultencoding("utf-8")

import re
# import ssf
from util import *
from bs4 import BeautifulSoup


class Node():
	def __init__(self,node_name,node_relation,node_parent):
		self.nodeName=node_name
		self.nodeRelation=node_relation
		self.nodeParent=node_parent
		self.childList=[]
		self.nodeLevel=-1
		self.chunkNum=-1
	def addChild(self,child):
		self.childList.append(child)
	def getChunkName(self,node_name):
		i=len(node_name)
		while (node_name[i-1]>="0" and node_name[i-1]<="9"):
			i-=1
#		print "qwe",node_name,node_name[:i]
		return node_name[:i]


class Sentence():
	def __init__(self,sentence_num):
#		print "-"*30,"adding sentence"
		self.sentenceNum=sentence_num
		self.chunkList=[]
		self.wordNumList=[]
		self.nodeDict={}
		self.rootNode=[]
		return
	def addChunk(self,chunk):
#		print "-"*30,"adding chunk"
		self.chunkList.append(chunk)
	def addWord(self,word):
#		print "-"*30,"adding word to sentence"
		self.wordNumList.append(word)
	def addNode(self,node):
		self.nodeDict[node.nodeName]=node
	def addChunkNumToNode(self,node_name,chunk_num):
		self.nodeDict[node_name].chunkNum=chunk_num

class Chunk():
	def __init__(self,tag,node_name,features_set,sentenceNum,chunk_num):
#		print "-"*30,"new chunk with tag - %s and f = %s"%(tag,features_string)
		self.chunkTag=tag
		self.chunkNum=chunk_num
		self.nodeName=node_name
		self.featureSet=features_set
		self.wordNumList=[]
		self.sentenceNum=sentenceNum
	def addWord(self,word):
#		print "-"*30,"adding word to chunk"
		self.wordNumList.append(word)
class Word():
	def __init__(self,word,tag,features_string,extra_features,sentenceNum,chunkNum):
#		print "-"*30,"new word- %s with tag - %s and f = %s"%(word,tag,features_string)
		self.wordTag=tag;
		self.word=word.decode("utf-8")
		self.featureSet=FeatureSet(features_string)
		self.extraFeatureSet=extra_features
		self.sentenceNum=sentenceNum
		self.chunkNum=chunkNum
		self.sense=None
		self.conn=False
		self.splitConn=False
		self.arg1=False
		self.arg2=False
		self.relationNum=None
		self.arg1Span=None
		self.arg2Span=None
class FeatureSet():
	def __init__(self,featureString):
		self.featureDict={}
		self.processFeatureString(featureString)
	def processFeatureString(self,featureString):
		featureSet=re.split(' ',featureString)
		featureSet=featureSet[1:]
		for feature in featureSet:
#			print feature
			feature=re.split('=',feature)
			key=feature[0]
			value=re.split('\"',feature[1])[1]
#			print key,"=",value
			self.featureDict[key]=value

def extractExtraSSF(filePath):
	filePath=filePath.replace("/ssf/","/ssf_1/")
	print filePath
	if not fileExists(filePath) :
		print "No file found"
		return None
	fileFD=codecs.open(filePath,"r",encoding="utf-8")
	data=fileFD.read()
	fileFD.close()
	beautData = BeautifulSoup(data)
	sentenceList=beautData.find_all('sentence')
	sList=[]
	for sentence in sentenceList:
		content=sentence.renderContents()
		lines=re.split("\n",content)
	 	wList=[]
		for line in lines:
#			print line
			columns=line.split("\t")
			if(len(columns)<4):
				continue
			
			f=FeatureSet(columns[3])
#			try:
#				print "XXX",f.featureDict["af"]
#			except:
#				print "XXXhere"
			wList.append(f)
		sList.append(wList)
	return sList

			
def extractSSFannotations(filePath):
	filePath=filePath.replace("/raw/","/ssf/")
	if not fileExists(filePath) :
		print "No file found"
		return (None,None)
	extraInfoList=extractExtraSSF(filePath)
	if(extraInfoList==None):
		print "No file found"
		return (None,None)
	fileFD=codecs.open(filePath,"r",encoding="utf-8")
	data=fileFD.read()
	fileFD.close()
	beautData = BeautifulSoup(data)
	sentenceList=beautData.find_all('sentence')
	sentenceInstList=[]
	globalWordList=[]
	sentenceNum=0
	wordNum=0
	for sentence in sentenceList:
	 	extraSentenceInfo=extraInfoList[sentenceNum]
		sentenceInst=Sentence(sentenceNum)
		content=sentence.renderContents()
		lines=re.split("\n",content)
		chunkInst=None
		NodeInst=None
		wordInst=None
		chunkNum=-1
		skip=False
		wNum=0
		for line in lines:
			columns=line.split("\t")
#			print line,"--",len(columns)
			if(len(columns)<2): #useless line
				continue
			if(columns[1]=="(("): # new chunk
#				if("NULL" in columns[2]):
#					skip=True
#					continue
				chunkNum+=1
				featureSetInst=FeatureSet(columns[3])
				chunkInst=Chunk(columns[2],featureSetInst.featureDict["name"],featureSetInst,sentenceNum,chunkNum)
				try:
					nodeInst=Node(featureSetInst.featureDict["name"],featureSetInst.featureDict["drel"].split(":")[0],featureSetInst.featureDict["drel"].split(":")[1])
				except:
#					nodeInst=Node(featureSetInst.featureDict["name"],"None","None")
					try:
						nodeInst=Node(featureSetInst.featureDict["name"],featureSetInst.featureDict["dmrel"].split(":")[0],featureSetInst.featureDict["dmrel"].split(":")[1])
						print "dmrel got"
					except:
						nodeInst=Node(featureSetInst.featureDict["name"],"None","None")
						print "dmrel not got",featureSetInst.featureDict
#					print "hohoh",line
			elif(columns[1]=="))"):
				sentenceInst.addNode(nodeInst)
			  	if(len(chunkInst.wordNumList)!=0):
					sentenceInst.addChunk(chunkInst)
					sentenceInst.addChunkNumToNode(nodeInst.nodeName,chunkInst.chunkNum)
				else:
					print "found file with empty chunk !!!",filePath
					chunkNum-=1
			else:
			  	if(columns[1]=="NULL"):
					continue
				try:
					extraWordInfo=extraSentenceInfo[wNum]
				except:
				 	print "Could not match intrachunk and interchunk SSF annotations !!!"
				 	print columns[1],columns[2],wordNum
				 	exit()
				wordInst=Word(columns[1],columns[2],columns[3],extraWordInfo,sentenceNum,chunkNum)
				chunkInst.addWord(wordNum)
				sentenceInst.addWord(wordNum)
				globalWordList.append(wordInst)
				wordNum+=1
				wNum+=1
#		print "final stats",len(SSFSentenceInst.wordList),len(SSFSentenceInst.chunkList)
		sentenceInstList.append(sentenceInst)
		sentenceNum+=1
	return (sentenceInstList,globalWordList)

