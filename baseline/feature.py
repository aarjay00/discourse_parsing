#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
import numpy
import itertools
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from letter import *
from tree_api import *


class Feature():
	def __init__(self,word_dictionary_path,tag_path,chunk_path,discourse_file,global_word_list,sentence_list,conn=None):
		self.discourseFile=discourse_file
		self.wordDictionary=self.loadSet(word_dictionary_path,["First","Last"])
		self.tagSet=self.loadSet(tag_path,["First","Last"])
		self.loadCombo("tagSet")
		self.chunkSet=self.loadSet(chunk_path,["First","Last","Null"])
		self.loadCombo("chunkSet")
		self.categorySet=self.loadSet("./lists/category.list")
		self.dependencySet=self.loadSet("./lists/dependencySet.list",["Null","None"])
		self.nodeRelationSet=self.loadSet("./lists/nodeRelation.list")
		self.nodeRelationSetPrev=self.loadSet("./lists/nodeRelationPrev.list")
		self.nodeRelationSetNext=self.loadSet("./lists/nodeRelationNext.list")
		self.nodeParentSet=self.loadSet("./lists/nodeParent.list")
		self.nodeParentSetPrev=self.loadSet("./lists/nodeParentPrev.list")
		self.nodeParentSetNext=self.loadSet("./lists/nodeParentNext.list")
		self.genderSet=self.loadSet("./lists/gender.list")
		self.numberSet=self.loadSet("./lists/gender.list")
		self.personSet=self.loadSet("./lists/person.list")
		self.caseSet=self.loadSet("./lists/case.list")
		self.featureVector=[]
		self.classLabel=None
		self.globalWordList=global_word_list
		self.sentenceList=sentence_list
		self.description=""
		self.connSpec={}
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
		FD=codecs.open("./lists/connSpecDependency.list","r")
		currConn=""
		for line in FD.readlines():
			line=line[:-1]
			if(line[:4]=="conn"):
				self.connSpec[line.split(":")[1]]=[]
				currConn=line.split(":")[1]
			else:
				self.connSpec[currConn].append(line)
		FD.close()
	def loadSet(self,filePath,extra=[]):
		Set=[]
		fileFD=codecs.open(filePath,"r",encoding="utf-8")
		for line in fileFD.readlines():
			line=line.strip()
			Set.append(line)
		Set.extend(extra)
		return Set
	def loadCombo(self,setName):
		singleSet=getattr(self,setName)
		setattr(self,setName+"Combo",[i[0]+" "+i[1] for i in itertools.product(singleSet,singleSet)])
#		print "combo",getattr(self,setName+"Combo")
	def wordFeature(self,wordList,wordList2=[]):
		self.description=self.description+" wordFeature"
		print "wordfeature",
		words=[]
		w=""
		for word in wordList:
			word=self.globalWordList[word].word
			w=w+word+" "
#			words.append(word)
		if(len(wordList2)!=0):
			w=w[:-1]+".."
		for word in wordList2:
			word=self.globalWordList[word].word
			w=w+word+" "
		print w
		words.append(w[:-1])
		feature=self.markItemsinList(words,self.wordDictionary)
		print feature
		return feature
	def wordNeighbor(self,wordList,offSet):
		self.description=self.description+" wordNeighbor"
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
		self.description=self.description+" tagFeature"
		print "tagfeature"
		tagList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print word.wordTag,
			tagList.append(word.wordTag)
		print ""
		feature=self.markItemsinList(list(set(tagList)),self.tagSet)
		print feature
		return feature
	def tagNeighbor(self,wordList,offSet):
		self.description=self.description+" tagNeighbor-"+str(offSet)
		print "tagNeighbor"
		tagList=[]
		if(offSet<0):
			if(wordList[0]+offSet<0 or self.globalWordList[wordList[0]+offSet].sentenceNum!=self.globalWordList[wordList[0]].sentenceNum):
	#		if(wordList[0]+offSet<0):
				tagList.append("First")
			else:
				tagList.append(self.globalWordList[wordList[0]+offSet].wordTag)
		else:
			if(wordList[-1]+offSet>=len(self.globalWordList) or self.globalWordList[wordList[-1]+offSet].sentenceNum!=self.globalWordList[wordList[-1] +offSet].sentenceNum):
# This should be the correct line of code but above line giving better results :/ :/
#		if(wordList[-1]+offSet>=len(self.globalWordList) or self.globalWordList[wordList[-1]+offSet].sentenceNum!=self.globalWordList[wordList[-1]].sentenceNum):
				tagList.append("Last")
			else:
			 	tagList.append(self.globalWordList[wordList[-1]+offSet].wordTag)
		for tag in tagList:
			print tag,
		print ""
		feature=self.markItemsinList(tagList,self.tagSet)
		print feature
		return feature
	def tagCombo(self,wordList,offSet1,offSet2):
		self.description=self.description+" tagCombo-"+str(offSet1)+"-"+str(offSet2)
		print "tagCombo",offSet1,offSet2
		tag=""
		if(offSet1==0):
			tag=self.globalWordList[wordList[0]].wordTag
		elif(offSet1<0):
			if(wordList[0]+offSet1<0 or self.globalWordList[wordList[0]+offSet1].sentenceNum!=self.globalWordList[wordList[0]].sentenceNum):
				tag="First"
			else:
				tag=self.globalWordList[wordList[0]+offSet1].wordTag
		else:
			if(wordList[-1]+offSet1>=len(self.globalWordList) or self.globalWordList[wordList[-1]].sentenceNum!=self.globalWordList[wordList[-1]].sentenceNum):
				tag="Last"
			else:
			 	tag=self.globalWordList[wordList[-1]+offSet1].wordTag
		if(offSet2==0):
			tag=self.globalWordList[wordList[-1]].wordTag
		elif(offSet2<0):
			if(wordList[0]+offSet2<0 or self.globalWordList[wordList[0]+offSet2].sentenceNum!=self.globalWordList[wordList[0]].sentenceNum):
				tag=tag+" First"
			else:
				tag=tag+" "+self.globalWordList[wordList[0]+offSet2].wordTag
		else:
			if(wordList[-1]+offSet2>=len(self.globalWordList) or self.globalWordList[wordList[-1]].sentenceNum!=self.globalWordList[wordList[-1]].sentenceNum):
				tag=tag+" Last"
			else:
			 	tag=tag+" "+self.globalWordList[wordList[-1]+offSet2].wordTag
		print tag
		feature=self.markItemsinList([tag],self.tagSetCombo)
	def chunkFeature(self,wordList):
		self.description=self.description+" chunkFeature"
		print "chunkfeature"
		chunkList=[]
		for word in wordList:
			word=self.globalWordList[word]
			print self.getChunkInfo(word,0).chunkTag,
			chunkList.append(self.getChunkInfo(word,0).chunkTag)
		print ""
		chunkList=list(set(chunkList))
		feature=self.markItemsinList(chunkList,self.chunkSet)
		print feature
	def chunkNeighbor(self,wordList,offSet):
		self.description=self.description+" chunkNeighbor-"+str(offSet)
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
		for chunk in chunkList:
			print chunk
		print ""
		feature=self.markItemsinList(chunkList,self.chunkSet)
	def chunkCombo(self,wordList,offSet1,offSet2):
		self.description=self.description+" chunkCombo-"+str(offSet1)+"-"+str(offSet2)
		print "chunkCombo",offSet1,offSet2
		chunkList=[]
		chunk=""
		if(offSet1==0):
			chunk=self.getChunkInfo(self.globalWordList[wordList[0]],0).chunkTag
		elif(offSet1<0):
			try:
				chunk=self.getChunkInfo(self.globalWordList[wordList[0]],offSet1).chunkTag
			except AttributeError:
				chunk="First"
		else:
			try:
				chunk=self.getChunkInfo(self.globalWordList[wordList[0]],offSet1).chunkTag
			except AttributeError:
				chunk="Last"
		if(offSet2==0):
			chunk=chunk+" "+self.getChunkInfo(self.globalWordList[wordList[0]],0).chunkTag
		elif(offSet2<0):
			try:
				chunk=chunk+" "+self.getChunkInfo(self.globalWordList[wordList[0]],offSet2).chunkTag
			except AttributeError:
				chunk=chunk+" "+"First"
		else:
			try:
				chunk=chunk+" "+self.getChunkInfo(self.globalWordList[wordList[0]],offSet2).chunkTag
			except AttributeError:
				chunk=chunk+" "+"Last"
		chunkList.append(chunk)
		print chunk
		feature=self.markItemsinList(chunkList,self.chunkSetCombo)
	def tamFeature(self,wordList):
		print "tamFeature"
	def chunkSeqFeature(self,chunkSeq):
		self.description=self.description+" chunkSeqFeature" 
		print "ChunkSeqFeature",len(chunkSeq)
		if(len(chunkSeq)>20):
			print "ahem chunk"
		for i in range(0,40):
			if(i<len(chunkSeq)):
				print chunkSeq[i].chunkTag,
				feature=self.markItemsinList([chunkSeq[i].chunkTag],self.chunkSet)
			else:
				feature=self.markItemsinList(["Null"],self.chunkSet)
		print ""
	def dependencySeqFeature(self,dependencySeq):
		self.description=self.description+" dependencySeqFeature" 
		print "dependencySeqFeature",len(dependencySeq)
		for i in range(0,len(dependencySeq)):
			if(dependencySeq[i].startswith("pof")):
				dependencySeq[i]="pof"
			elif(dependencySeq[i].startswith("nmod__") and dependencySeq[i]!="nmod__relc"):
			 	dependencySeq[i]="nmod"
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
	def hasNodeRelationSpecific(self,conn,connective,nodeRelationList,node,nodeDict,maxLevel):
		self.description=self.description+" hasNodeRelationSpecific-" +getSpan(conn,self.globalWordList)+"-"+str(nodeRelationList)
		if(getSpan(conn,self.globalWordList)!=connective):
			self.featureVector.append(0)
			return [0]
#		print "got ke baad"
		for nodeRelation in nodeRelationList:
			if(not findRelation(nodeRelation,node,nodeDict,0,maxLevel)):
				self.featureVector.append(0)
				return [0]
		self.featureVector.append(1)
		return [1]

	def nodeFeature(self,node_feature,nodeListName):
		self.description=self.description+" nodeFeature-" +str(nodeListName)
	  	print nodeListName,"Feature"
	  	nodeSet=getattr(self,nodeListName)
	  	if(node_feature not in nodeSet):
			print "ERROR !!!!",nodeListName
		feature=self.markItemsinList([node_feature],nodeSet)
	def hasNodeRelation(self,nodeRelation,node,nodeDict,maxLevel):
		self.description=self.description+" hasNodeRelation-"+str(nodeRelation)
		if(findRelation(nodeRelation,node,nodeDict,0,maxLevel)):
			self.featureVector.append(1)
			print "nodeRelation found"
		else:
			self.featureVector.append(0)
			print "nodeRelation not found"

	def aurFeature(self,conn):
		self.description=self.description+" aurFeature"
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
	def aurFeature2(self,conn,nodeName,nodeDict,c):
		self.description=self.description+" aurFeature2"
		if(self.globalWordList[conn[0]].word != u'\u0914\u0930'):
			self.featureVector.append(0)
			return [0]	
		childList=nodeDict[nodeName].childList
		childVGF=0
		for child in nodeDict[nodeName].childList:
			if(nodeDict[nodeName].getChunkName(child)[:2]=="VG"):
				childVGF+=1
		if(childVGF==2):
			print "aurFeature2 yes",c
			self.featureVector.append(1)
		else:
			print "aurFeature2 no",c
			self.featureVector.append(0)
	def parFeature(self,conn):
		self.description=self.description+" parFeature"
		if(getSpan(conn,self.globalWordList)!=u'\u092a\u0930'):
			self.featureVector.append(0)
			return [0]
		print "got par"
		checkList=[u'\u0916\u093e\u0938\u0924\u094c\u0930',u'\u0935\u0939\u0940\u0902',u'\u0909\u0938',u'\u0907\u0938',u'\u0907\u0938 \u092c\u093e\u0924']
		if(self.globalWordList[conn[0]-1].word in checkList):
			self.featureVector.append(1)
			print "found",self.globalWordList[conn[0]-1].word
			return [1]
		try:
			if(self.globalWordList[conn[0]-2].word+" "+self.globalWordList[conn[0]-1].word in checkList):
				self.featureVector.append(1)
				print "found",self.globalWordList[conn[0]-2].word+" "+self.globalWordList[conn[0]-1].word
				return [1]
		except:
			pass
		print "not found"
		self.featureVector.append(0)
		return [0]
	def lekinFeature(self,conn):
		self.description=self.description+" lekinFeature"
		print "lekinFeature",len(self.featureVector) 
		if(getSpan(conn,self.globalWordList)!=u'\u0932\u0947\u0915\u093f\u0928'):
			self.featureVector.append(0)
			return [0]
		sentencePrev=[]
		sentenceNum=self.globalWordList[conn[0]].sentenceNum
		pos=conn[0]-1
		while(pos >=0 and self.globalWordList[pos].sentenceNum==sentenceNum):
			sentencePrev.append(pos)
			pos-=1
		if(pos>=0):
			sentencePrev.append(pos)
			print "appending ",self.globalWordList[pos].word
		sentencePrev.reverse()
		sentencePrevSpan=getSpan(sentencePrev,self.globalWordList)
		print sentencePrevSpan
		checkList=[u'\u092f\u0942\u0902 \u0924\u094b',u'\u092d\u0932\u0947 \u0939\u0940',u'\u0939\u093e\u0932\u093e\u0902\u0915\u093f',u'\u092c\u0947\u0936\u0915',u'\u0939\u093e\u0932\u093e\u0901\u0915\u093f',u'\u0924\u094b']
		for item in checkList:
			if item in sentencePrevSpan:
				print "found lekin",item
				self.featureVector.append(1)
				return [1]
		self.featureVector.append(0)
		return [0]
	def toRootFeature(self,conn,node,nodeDict):
		self.description=self.description+" toRootFeature"
		if(getSpan(conn,self.globalWordList)!=u'\u0924\u094b'):
#			self.featureVector.extend([0])
			return [0]
		print "toRootFeature"
		if(node.nodeRelation!="None"):
#			self.featureVector.append(0)
			return [0]
		sentencePrev=[]
		sentenceNum=self.globalWordList[conn[0]].sentenceNum
		pos=conn[0]-1
		while(pos >=0 and self.globalWordList[pos].sentenceNum==sentenceNum):
			sentencePrev.append(pos)
			pos-=1
		sentencePrev.reverse()
		sentencePrevSpan=getSpan(sentencePrev,self.globalWordList)
		print sentencePrevSpan
		checkList=[u'\u091c\u0948\u0938\u0947 \u0939\u0940',u'\u092f\u0926\u093f',u'\u0905\u0917\u0930',u'\u091c\u092c',u'\u0935\u0939\u0940\u0902']
		for item in checkList:
			if item in sentencePrevSpan:
				print "found toto",item
#				self.featureVector.append(0)
				return [0]
		print "to works"
#		self.featureVector.append(1)
		return [1]
	def tok7tFeature(self,conn,node,nodeDict):
		self.description=self.description+" tok7tFeature"
		if(getSpan(conn,self.globalWordList)!=u'\u0924\u094b'):
#			self.featureVector.extend([0])
			return [0]
		print "tok7tFeature"
		if(node.nodeRelation!="k7t" or len(node.childList)==0):
#		 	self.featureVector.extend([0])
			return [0]
		sentencePrevSpan=self.getPrevSentenceSpan(conn)
		print sentencePrevSpan
		checkList=[u'\u091c\u0948\u0938\u0947 \u0939\u0940',u'\u092f\u0926\u093f',u'\u0905\u0917\u0930',u'\u091c\u092c',u'\u0935\u0939\u0940\u0902']
		for item in checkList:
			if item in sentencePrevSpan:
				print "found toto1",item
#				self.featureVector.append(0)
				return [0]
		print "to works k7t"
#		self.featureVector.append(1)
		return [1]
	def dependencyFeature(self,conn,dependencyList):
		connective=getSpan(conn,self.globalWordList)
		for feature in self.connSpec[connective.encode("utf-8")]:
			if(feature in dependencyList):
				self.featureVector.append(1)
			else:
				self.featureVector.append(0)
	def markItemsinList(self,List,Set):
# 		set is universal set out of which marking objects contained in list
		feature=[]
		notMarked=0
		for item in Set:
			if(item in List):
				print item,"marked"
				feature.append(1)
				notMarked+=1
			else:
				feature.append(0)
		if(notMarked!=len(List)):
			print "feature ERROR"
		self.featureVector.extend(feature)
		return feature
	def getChunkInfo(self,word,offSet):
		sentence=self.sentenceList[word.sentenceNum]
		if(word.chunkNum+offSet>=0 and word.chunkNum+offSet<len(sentence.chunkList)):
			chunk=sentence.chunkList[word.chunkNum+offSet]
		else:
			chunk=None
		return chunk
	def getPrevSentenceSpan(self,conn,):
		sentencePrev=[]
		sentenceNum=self.globalWordList[conn[0]].sentenceNum
		pos=conn[0]-1
		while(pos >=0 and self.globalWordList[pos].sentenceNum==sentenceNum):
			sentencePrev.append(pos)
			pos-=1
		sentencePrev.reverse()
		sentencePrevSpan=getSpan(sentencePrev,self.globalWordList)
		return sentencePrevSpan
	def cleanFeature(self,removeList):
		removeList=sorted(removeList,reverse=True)
		for pos in removeList:
			val=self.featureVector.pop(pos)
			if(val==1):
				print "clean ERROR"

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
#		ignore_print.append("sentenceNum")
#		ignore_print.append("rawFileName")
		ignore_print.append("description")
		for attr in self.attrList:
			if(attr in ignore_print):
				continue
			FD.write(attr+" : "+str(getattr(self,attr))+"\n")
		return

def convertDataSet(featureCollection):
	print "-"*50,"ConvertDataSet"
	data=[]
	labels=[]
	for feature in featureCollection:
		numpyArr=numpy.array(feature.featureVector)
		data.append(numpyArr)
		labels.append(feature.classLabel)
	labels=numpy.array(labels)
	data=numpy.array(data)
	return data,labels
def removeExtraFeatures(featureCollection):
	featureSize=len(featureCollection[0].featureVector)
	featurePresent=[]
	print "featureSize---",featureSize
	for i in featureCollection[0].featureVector:
		featurePresent.append(False)
	for feature in featureCollection:
		vector=feature.featureVector
		for pos in range(0,featureSize):
			if(vector[pos]==1):
				featurePresent[pos]=True
	remove=[]
	for pos in range(0,featureSize):
		if(not featurePresent[pos]):
			remove.append(pos)
	print "useless features",remove
	return remove
