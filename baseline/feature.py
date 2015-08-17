#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import numpy
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from letter import *


class Feature():
	def __init__(self,word_dictionary_path,tag_path,chunk_path,discourse_file,global_word_list,sentence_list,conn=None):
		self.discourseFile=discourse_file
		self.wordDictionary=self.loadSet(word_dictionary_path,["First","Last"])
		self.tagSet=self.loadSet(tag_path,["First","Last"])
		self.chunkSet=self.loadSet(chunk_path,["First","Last","Null"])
		self.categorySet=self.loadSet("./lists/category.list")
		self.dependencySet=self.loadSet("./lists/dependencySet.list",["Null","None"])
		self.genderSet=self.loadSet("./lists/gender.list")
		self.numberSet=self.loadSet("./lists/gender.list")
		self.personSet=self.loadSet("./lists/person.list")
		self.caseSet=self.loadSet("./lists/case.list")
		self.featureVector=[]
		self.classLabel=None
		self.globalWordList=global_word_list
		self.sentenceList=sentence_list
		if(conn!=None and isinstance(conn[0],int)):
			self.connective=""
			for i in conn:
				self.connective=self.connective+" "+self.globalWordList[i].word
			self.connective=self.connective[1:]
			self.conn=conn
		elif(conn!=None and isinstance(conn[0],list)):
			self.connective=""
			for i in conn:
				for j in i:
					self.connective=self.connective+" "+self.globalWordList[j].word
			self.connective=self.connective[1:]
			self.conn=conn
		print len(self.tagSet)
		print len(self.chunkSet)
	def loadSet(self,filePath,extra=[]):
		Set=[]
		fileFD=codecs.open(filePath,"r",encoding="utf-8")
		for line in fileFD.readlines():
			line=line.split()
			for word in line:
				Set.append(word)
		Set.extend(extra)
		return Set
	def wordFeature(self,wordList):
		print "wordfeature"
		words=[]
		for word in wordList:
			word=self.globalWordList[word].word
			words.append(word)
		feature=self.markItemsinList(words,self.wordDictionary)
		print feature
		return feature
	def wordNeighbor(self,wordList,offSet):
		print "wordNeighbor"
		words=[]
		if(offSet<0):
			if(wordList[0]+offSet<0):
				words.append("First")
			else:
				words.append(self.globalWordList[wordList[0]+offSet].word)
		else:
			if(wordList[-1]+offSet>=len(self.globalWordList)):
				words.append("Last")
			else:
			 	words.append(self.globalWordList[wordList[-1]+offSet].word)
		feature=self.markItemsinList(words,self.wordDictionary)
		print feature
		return feature
	def tagFeature(self,wordList):
		print "tagfeature"
		tagList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print word.wordTag,
			tagList.append(word.wordTag)
		print ""
		feature=self.markItemsinList(tagList,self.tagSet)
		print feature
		return feature
	def tagNeighbor(self,wordList,offSet):
		print "tagNeighbor"
		tagList=[]
		if(offSet<0):
			if(wordList[0]+offSet<0):
				tagList.append("First")
			else:
				tagList.append(self.globalWordList[wordList[0]+offSet].word)
		else:
			if(wordList[-1]+offSet>=len(self.globalWordList)):
				tagList.append("Last")
			else:
			 	tagList.append(self.globalWordList[wordList[-1]+offSet].word)
		feature=self.markItemsinList(tagList,self.tagSet)
		print feature
		return feature
	def chunkFeature(self,wordList):
		print "chunkfeature"
		chunkList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print self.getChunkInfo(word,0).chunkTag,
			chunkList.append(self.getChunkInfo(word,0).chunkTag)
		print ""
		feature=self.markItemsinList(chunkList,self.chunkSet)
		print feature
	def chunkNeighbor(self,wordList,offSet):
		print "chunkNeighbor",offSet
		chunkList=[]
		if(offSet<0):
			try:
				chunkList.append(self.getChunkInfo(self.globalWordList[wordList[0]],offSet).chunkTag)
			except AttributeError:
				chunkList.append("First")
		else:
			try:
				chunkList.append(self.getChunkInfo(self.globalWordList[wordList[-1]],offSet).chunkTag)
			except AttributeError:
				chunkList.append("Last")
		print chunkList
		feature=self.markItemsinList(chunkList,self.chunkSet)
	def tamFeature(self,wordList):
		print "tamFeature"
	def chunkSeqFeature(self,chunkSeq):
		print "ChunkSeqFeature",len(chunkSeq)
		if(len(chunkSeq)>20):
			print "ahem chunk"
		for i in range(0,20):
			if(i<len(chunkSeq)):
				print chunkSeq[i].chunkTag,
				feature=self.markItemsinList([chunkSeq[i].chunkTag],self.chunkSet)
			else:
				feature=self.markItemsinList(["Null"],self.chunkSet)
		print ""
	def dependencySeqFeature(self,dependencySeq):
		print "dependencySeqFeature",len(dependencySeq)
		if(len(dependencySeq)>80):
			print "ahem depen"
		for i in range(0,20):
			if(i<len(dependencySeq)):
				if(dependencySeq[i] not in self.dependencySet):
					print "aaaaaaa"
				print dependencySeq[i],
				feature=self.markItemsinList([dependencySeq[i]],self.dependencySet)
			else:
				feature=self.markItemsinList(["Null"],self.dependencySet)
		print ""

	def markItemsinList(self,List,Set):
		feature=[]
		for item in Set:
			if(item in List):
				feature.append(1)
			else:
				feature.append(0)
		self.featureVector.extend(feature)
		return feature
	def getChunkInfo(self,word,offSet):
		sentence=self.sentenceList[word.sentenceNum]
		if(word.chunkNum+offSet>=0 and word.chunkNum+offSet<len(sentence.chunkList)):
			chunk=sentence.chunkList[word.chunkNum+offSet]
		else:
			chunk=None
		return chunk

	def aurFeature(self,conn):
		if(self.globalWordList[conn[0]].word != u'\u0914\u0930'):
			self.featureVector.append(0)
			return [0]
		chunkNum=0
                before=False
                after=False
                middle=False
		sentence=self.discourseFile.sentenceList[self.globalWordList[conn[0]].sentenceNum]
                for chunk in sentence.chunkList:
                        if(chunk.chunkTag[:2]=="VG"):
                                if(middle==False):
                                        before=True
                                else:
                                        after=True
                        for word in chunk.wordNumList:
                                if(self.discourseFile.globalWordList[word].word==u'\u0914\u0930'):
                                        middle=True
                        chunkNum+=1
		if(before and after):
			self.featureVector.append(1)
			return [1]
		self.featureVector.append(0)
		return [0]

	def setClassLabel(self,label):
		self.classLabel=label

class featureDesc():
	def __init__(self,raw_filename,sentence_num,description,class_label,identity):
		self.rawFileName=raw_filename
		self.sentenceNum=sentence_num
		self.description=description
		self.classLabel=class_label
		self.classifiedAs=""
		self.attrList=["rawFileName","sentenceNum","description","classLabel","classifiedAs"]
		self.ID=identity
	def addDescription(self,desc):
		self.description=self.description+"\n"+desc
	def addAttr(self,attr_name,attr_value):
		setattr(self,attr_name,attr_value)
		self.attrList.append(attr_name)
	def printFeatureDesc(self,FD,ignore_print=[]):
		ignore_print.append("sentenceNum")
		ignore_print.append("rawFileName")
		ignore_print.append("description")
		for attr in self.attrList:
			if(attr in ignore_print):
				continue
			FD.write(attr+" : "+str(getattr(self,attr))+"\n")
		return

def convertDataSet(featureCollection):
	data=[]
	labels=[]
	for feature in featureCollection:
		data.append(numpy.array(feature.featureVector))
		labels.append(feature.classLabel)
	labels=numpy.array(labels)
	data=numpy.array(data)
	return data,labels

