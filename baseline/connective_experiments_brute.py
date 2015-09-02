#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import itertools
from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
from annotated_data import *
from feature import *
from models import *

from tree_api import *

def searchConn(conn,wordList):
	conn=conn.split()
	pos=0
	posList=[]
	while(pos<len(wordList)-len(conn)+1):
		found=True
		for j in range(0,len(conn)):
			if(conn[j]!=wordList[pos+j].word):
				found=False
				break
		if(found):
			posList.append(pos)
			pos+=len(conn)
		else:
			pos+=1
	return posList

def searchSplitConn(conn1,conn2,wordList,sentenceList):
	conn1=conn1.split()
	conn2=conn2.split()
	posList=[]
	for sentence in sentenceList:
		p1=[]
		wordPos=sentence.wordNumList[0]
		while(wordPos < sentence.wordNumList[-1]-len(conn1)+2):
			found=True
			for j in range(0,len(conn1)):
				if(conn1[j]!=wordList[wordPos+j].word):
					found=False
					break
			if(found):
				p1.append(wordPos)
				wordPos+=len(conn1)
			else:
			 	wordPos+=1
		if(len(p1)==0):
			continue
		p2=[]
		wordPos=sentence.wordNumList[0]
		while(wordPos < sentence.wordNumList[-1]-len(conn2)+2):
			found=True
			for j in range(0,len(conn2)):
				if(conn2[j]!=wordList[wordPos+j].word):
					found=False
					break
			if(found):
				p2.append(wordPos)
				wordPos+=len(conn2)
			else:
			 	wordPos+=1
		if(len(p2)==0):
			continue
		for i in p1:
		 	for j in p2:
				if(i+len(conn1)<=j):
					posList.append((i,j))
	return posList


def convert_span(i,conn):
	l=[]
	for j in range(i,i+len(conn.split())):
		l.append(j)
	return l
def identifyConnectives(discourseFileInst,connList,connSplitList):
	positiveSetSingle=[]
	negativeSetSingle=[]
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList
	for conn in connList:
		posList=searchConn(conn,wordList)
		if(len(posList)==0):
			continue
#		print "found ",conn,len(posList)
		for i in posList:
#			for j in range(i,i+len(conn.split())):
#				print wordList[j].chunkNum,
#			print "\n"
			if(wordList[i].conn and (i!=0 and not wordList[i-1].conn)):
#					print "lol error",conn
				positiveSetSingle.append(convert_span(i,conn))
#				print "Yes",wordList[i].sense
			else:
				negativeSetSingle.append(convert_span(i,conn))
#			 	print "No"
	positiveSetSplit=[]
	negativeSetSplit=[]
	for conn in connSplitList:
		conn1,conn2=conn[0],conn[1]
		posList=searchSplitConn(conn1,conn2,wordList,sentenceList)
		if(len(posList)==0):
			continue
		for i,j in posList:
		 	if(not (wordList[i].splitConn and wordList[j].splitConn)):
				negativeSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))
			elif((i==0 or wordList[i-1].splitConn) or (i==len(wordList)-1 or wordList[i+1].splitConn)):
				print "Split",len(positiveSetSplit),len(negativeSetSplit)
				negativeSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))
			else:
				positiveSetSplit.append((convert_span(i,conn1),convert_span(j,conn2)))

	return (positiveSetSingle,negativeSetSingle,positiveSetSplit,negativeSetSplit)
def genFeatureSingleConn(conn,label,discourseFile,runInst):
		
		sentenceList=discourseFile.sentenceList
		wordList=discourseFile.globalWordList
		chunk=getChunk(conn[0],wordList,sentenceList)
		prevChunk=sentenceList[chunk.sentenceNum].chunkList[chunk.chunkNum-1]
		nxtChunk=sentenceList[chunk.sentenceNum].chunkList[chunk.chunkNum+1]
		print "hh",prevChunk.nodeName,nxtChunk.nodeName
		node=sentenceList[chunk.sentenceNum].nodeDict[chunk.nodeName]
		nodeDict=sentenceList[chunk.sentenceNum].nodeDict
		prevNode=sentenceList[prevChunk.sentenceNum].nodeDict[prevChunk.nodeName]
		nxtNode=sentenceList[nxtChunk.sentenceNum].nodeDict[nxtChunk.nodeName]
		if(getSpan(conn,wordList)==u'\u0924\u094b'):
			print discourseFile.rawFileName,wordList[conn[0]].sentenceNum
			print "get to",label
			print node.nodeRelation
			print node.getChunkName(node.nodeParent)
			for child in node.childList:
				print node.getChunkName(child),nodeDict[child].nodeRelation,
			if(len(node.childList)==0):
				print "None"
			else:
				print ""
		print "single conn","-"*30,node.getChunkName(nxtNode.nodeRelation),label
		for p in conn:
			print discourseFile.globalWordList[p].word,
		print "\n"
		feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile,discourseFile.globalWordList,discourseFile.sentenceList,conn)
		feature.wordFeature(conn)
		feature.tagFeature(conn)
#		feature.nodeFeature(node.nodeRelation,"nodeRelationSet")
#		feature.nodeFeature(node.getChunkName(node.nodeParent),"nodeParentSet")
#		feature.nodeFeature(prevNode.nodeRelation,"nodeRelationSetPrev")
#		feature.nodeFeature(nxtNode.nodeRelation,"nodeRelationSetNext")
#		feature.nodeFeature(node.getChunkName(prevNode.nodeParent),"nodeParentSetPrev")
#		feature.nodeFeature(node.getChunkName(nxtNode.nodeParent),"nodeParentSetNext")
		feature.tagNeighbor(conn,-1)
		feature.tagNeighbor(conn,1)
#		feature.tagNeighbor(conn,-2)
#		feature.tagNeighbor(conn,2)
#		feature.tagCombo(conn,0,-1)
		feature.chunkFeature(conn)
		if(runInst[0]==1):
			feature.hasNodeRelation("k1",node.nodeName,nodeDict,10)
		if(runInst[1]==1):
			feature.hasNodeRelation("k2",node.nodeName,nodeDict,10)
		if(runInst[2]==1):
			feature.hasNodeRelation("k3",node.nodeName,nodeDict,10)
		if(runInst[3]==1):
			feature.hasNodeRelation("k4",node.nodeName,nodeDict,10)
		if(runInst[4]==1):
			feature.hasNodeRelation("k5",node.nodeName,nodeDict,10)
		if(runInst[5]==1):
			feature.hasNodeRelation("k7t",node.nodeName,nodeDict,10)
		if(runInst[6]==1):
			feature.hasNodeRelation("r6",node.nodeName,nodeDict,10)
		if(runInst[7]==1):
			feature.hasNodeRelation("r6-k1",node.nodeName,nodeDict,10)
		if(runInst[8]==1):
			feature.hasNodeRelation("k7p",node.nodeName,nodeDict,10)
		if(runInst[9]==1):
			feature.hasNodeRelation("k7",node.nodeName,nodeDict,10)
#		feature.hasNodeRelationSpecific(conn,u'\u0915\u0947 \u092c\u093e\u0926',["k2","k7t"],node.nodeName,nodeDict,10)
#		feature.hasNodeRelationSpecific(conn,u'\u0915\u0947 \u092c\u093e\u0926',["k1"],node.nodeName,nodeDict,10)
#		feature.hasNodeRelationSpecific(conn,u'\u0915\u0947 \u092c\u093e\u0926',["k7t"],node.nodeName,nodeDict,10)
#		feature.hasNodeRelationSpecific(conn,u'\u0915\u0947 \u092c\u093e\u0926',["r6"],node.nodeName,nodeDict,10)
		feature.chunkCombo(conn,0,-1)
		feature.chunkCombo(conn,0,1)
#		feature.chunkCombo(conn,0,-2)
		feature.chunkNeighbor(conn,1)
		feature.chunkNeighbor(conn,-1)
#		feature.chunkNeighbor(conn,2)
#		feature.chunkNeighbor(conn,-2)
		feature.setClassLabel(label)
		feature.aurFeature2(conn,node.nodeName,nodeDict,wordList[conn[0]].conn)
#		feature.aurFeature(conn)
		feature.parFeature(conn)
		l1=feature.toRootFeature(conn,node,nodeDict)
		l2=feature.tok7tFeature(conn,node,nodeDict)
		if(l1==[1] or l2==[1]):
			print "hohoho"
			feature.featureVector.append(1)
		else:
			feature.featureVector.append(0)
		feature.lekinFeature(conn)
		print feature.featureVector
#		if(getSpan(conn,wordList)==u'\u0915\u0947 \u092c\u093e\u0926'):
#			print "ke baad",label,
#			print node.getChunkName(node.nodeName)
#			print len(node.childList)
#			for child in node.childList:
#				print node.getChunkName(child),"-",nodeDict[child].nodeRelation,
#			print ""
		return feature

def genFeatureSplitConn(conn,label,discourseFile):
		print "conn","-"*30,
		for p in conn[0]:
			print discourseFile.globalWordList[p].word,
		print "---",
		for p in conn[1]:
			print discourseFile.globalWordList[p].word,
		feature=Feature("lists/splitConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile,discourseFile.globalWordList,discourseFile.sentenceList,conn)
		feature.wordFeature(conn[0],conn[1])
#		feature.wordFeature(conn[1])
		feature.tagFeature(conn[0])
		feature.tagFeature(conn[1])
#		feature.tagNeighbor(conn[0],-1)
#		feature.tagNeighbor(conn[1],1)
		feature.chunkFeature(conn[0])
		feature.chunkFeature(conn[1])
		feature.chunkNeighbor(conn[0],1)
		feature.chunkNeighbor(conn[0],2)
#		feature.chunkNeighbor(conn[0],-1)
		feature.chunkNeighbor(conn[1],-1)
		feature.chunkNeighbor(conn[1],-2)
#		feature.chunkNeighbor(conn[1],1)
		feature.setClassLabel(label)
		return feature

	
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection=loadModel("processedData/annotatedData")
def run(runInst):	
	print len(discourseFileCollection)
	positiveSet=[]
	negativeSet=[]
	positiveSetSplit=[]
	negativeSetSplit=[]
	fileNum=0
	featureCollectionSingle=[]
	featureCollectionSplit=[]
	featureCollectionDescSingle=[]
	featureCollectionDescSplit=[]
	for discourseFile in discourseFileCollection:
		wordList=discourseFile.globalWordList
		pSet,nSet,pSetSplit,nSetSplit=identifyConnectives(discourseFile,connList,connSplitList)
		for conn in pSet:
			featureCollectionSingle.append(genFeatureSingleConn(conn,"Yes",discourseFile,runInst))
			featureDescInst=featureDesc(discourseFile.rawFileName,wordList[conn[0]].sentenceNum,"Single connective identification","Yes",len(featureCollectionDescSingle))
			featureDescInst.addAttr("Single connective",getSpan(conn,wordList))
			try:
				featureDescInst.addAttr("Single connective neighborhood",wordList[conn[0]-1].word)
			except:
				featureDescInst.addAttr("Single connective neighborhood","First")
			featureCollectionDescSingle.append(featureDescInst)
		for conn in nSet:
			featureCollectionSingle.append(genFeatureSingleConn(conn,"No",discourseFile,runInst))
			featureDescInst=featureDesc(discourseFile.rawFileName,wordList[conn[0]].sentenceNum,"Single connective identification","No",len(featureCollectionDescSingle))
			featureDescInst.addAttr("Single connective",getSpan(conn,wordList))
			try:
				featureDescInst.addAttr("Single connective neighborhood",wordList[conn[0]-1].word)
			except:
				featureDescInst.addAttr("Single connective neighborhood","First")
			featureCollectionDescSingle.append(featureDescInst)
		for conn in pSetSplit:
			featureCollectionSplit.append(genFeatureSplitConn(conn,"Yes",discourseFile))
			featureDescInst=featureDesc(discourseFile.rawFileName,wordList[conn[0][0]].sentenceNum,"Split connective identification","Yes",len(featureCollectionDescSplit))
			featureCollectionDescSplit.append(featureDescInst)
		for conn in nSetSplit:
			featureCollectionSplit.append(genFeatureSplitConn(conn,"No",discourseFile))
			featureDescInst=featureDesc(discourseFile.rawFileName,wordList[conn[0][0]].sentenceNum,"Split connective identification","No",len(featureCollectionDescSplit))
			featureCollectionDescSplit.append(featureDescInst)
		positiveSet.extend(pSet)
		negativeSet.extend(nSet)
		positiveSetSplit.extend(pSetSplit)
		negativeSetSplit.extend(nSetSplit)
		fileNum+=1
	print len(positiveSetSplit),len(negativeSetSplit)
	print len(positiveSet),len(negativeSet)
	print len(featureCollectionSingle)


	extraFeatureList=removeExtraFeatures(featureCollectionSingle)
	for featureNum in range(0,len(featureCollectionSingle)):
		featureCollectionSingle[featureNum].cleanFeature(extraFeatureList)

	print "featureSize",len(featureCollectionSingle[0].featureVector)




#FD=codecs.open("to","w")
#for featureDesc in featureCollectionDescSingle:
#	print featureDesc.attrList
#	if(getattr(featureDesc,"Single connective")==u'\u0924\u094b'):
#		featureDesc.printFeatureDesc(FD)
#FD.close()
#exit()

	classList=[]
	for feature in featureCollectionSingle:
		classList.append(feature.classLabel)
	classList=list(set(classList))
	print classList
	max_acc=-1
	min_acc=100
	max_precision=-1
	min_precision=100
	avg_accuracy=0.0
	time=20

	errorCollection=[]
	for i in range(0,time):
		print "running"
		#x,y,z,l=runModel(featureCollectionSplit,8,1,1)
		x,y,z,err=runModel(featureCollectionSingle,featureCollectionDescSingle,classList,"connective_identification",15,1,1)
		errorCollection.extend(err)
		avg_accuracy+=z["Yes"]
		max_acc=max(max_acc,z["Yes"])
		min_acc=min(min_acc,z["Yes"])
	print "Accuracy",round(min_acc*100,2),"-",round(max_acc*100,2),"-",round(avg_accuracy*100.0/time,2)
	FD=open("accuracy_results","a")
	FD.write(featureCollectionSingle[0].description+"\n")
	FD.write("Accuracy "+str(round(min_acc*100,2))+"-"+str(round(max_acc*100,2))+"-"+str(round(avg_accuracy*100.0/time,2))+"\n")
	FD.close()
runCollection = list(itertools.product([0, 1], repeat=7))
for runInst in lst():
	print "SeparateRun","-"*100
	run(runInst)
