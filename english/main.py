#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import json

from util import *
from feature import *
from model_api import *


brownClusterDict={}
sentimentDict={}


def readBrownClusters(brownClusterLocation):
	global sentimentDict
	global brownClusterDict
	FD=open(brownClusterLocation,'r')

	for line in FD.readlines():
		line=line[:-1]
		line=line.split('\t')
		brownClusterDict[line[1].lower()]=line[0]
	print len(brownClusterDict.keys())
	FD.close()
	fileFD=open("mpqa_subj_05.json","r")
	sentimentDict=json.load(fileFD)
	print len(sentimentDict.keys())

def readDocuments(documentLocation,relationLocation):
	
	documentData=codecs.open(documentLocation,encoding='utf-8')
	documentList=json.load(documentData)
	
	relationData=codecs.open(relationLocation,encoding='utf-8')
	relationList=[json.loads(x) for x in relationData]

	return documentList,relationList


def divideRelations(relationList):
	explicitRelationList=[]
	implicitRelationList=[]
	for relation in relationList:
		connective=relation['Connective']['CharacterSpanList']
		if(len(connective)==0 or relation['Type']!="Explicit"):
			implicitRelationList.append(relation)
		else:
			if(relation['Type']=="Explicit"):
				explicitRelationList.append(relation)
			if(relation['Type']!="Explicit" and relation['Type']!="AltLex"):
				print "hmmma",relation['Type']
	return implicitRelationList,explicitRelationList

def divideRelationsFinal(relationList):
	explicitRelationList=[]
	implicitRelationList=[]
	for relation in relationList:
		connective=relation['Connective']['CharacterSpanList']
		if(len(connective)==0 ):
			implicitRelationList.append(relation)
		else:
			explicitRelationList.append(relation)
	return implicitRelationList,explicitRelationList

def explictFeatureGeneration(documentList,explicitRelationList):


	print "number of explicit relations",len(explicitRelationList)


	featureCollection=[]
	for explicitRelation in explicitRelationList :
		parseFile=documentList[explicitRelation["DocID"]]
		feature=Feature(explicitRelation["ID"])

		feature.connectiveString(explicitRelation)
		feature.connectivePOS(parseFile,explicitRelation)
		feature.previousWord(parseFile,explicitRelation)
		feature.nextWord(parseFile,explicitRelation)
		feature.connectiveSelfCategory(parseFile,explicitRelation)	
		feature.connectiveParentSelfCategory(parseFile,explicitRelation)	
		feature.connectiveLeftSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveRightSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveSyntaxInteraction()
#		feature.connectiveParentLeftSiblingSelfCategory(parseFile,explicitRelation)
#		feature.connectiveParentRightSiblingSelfCategory(parseFile,explicitRelation)
		feature.parentLinkedContext(parseFile,explicitRelation)
#		feature.connectiveToRootPath(parseFile,explicitRelation)
#		feature.syntaxSyntaxInteraction()
		try:
			feature.setClassLabel(explicitRelation["Sense"][0])
		except:
			pass
		featureCollection.append(feature)

	return featureCollection


def implicitFeatureGeneration(documentList,implicitRelationList):

	print "number of implicit relations",len(implicitRelationList)

	featureCollection=[]
	num=0	
	for implicitRelation in implicitRelationList:
	
		parseFile=documentList[implicitRelation["DocID"]]
		feature=Feature(implicitRelation["ID"])

		feature.firstWordArg1(parseFile,implicitRelation)
		feature.firstWordArg2(parseFile,implicitRelation)
#		feature.firstAndLastArg1(parseFile,implicitRelation)
#		feature.lastWordArg1(parseFile,implicitRelation)
#		feature.lastWordArg2(parseFile,implicitRelation)
#		feature.first2WordArg1(parseFile,implicitRelation)
#		feature.first2WordArg2(parseFile,implicitRelation)
		feature.first3WordArg1(parseFile,implicitRelation)
		feature.first3WordArg2(parseFile,implicitRelation)
#		feature.brownCluster(parseFile,implicitRelation,brownClusterDict)
		feature.modalWords(parseFile,implicitRelation)
		feature.numberPresence(parseFile,implicitRelation)
#		feature.verbSimilarity(parseFile,implicitRelation,brownClusterDict)
		feature.argumentSentiment(parseFile,implicitRelation,sentimentDict)
		feature.argumentPosition(parseFile,implicitRelation)
		feature.parseTreeProductionRules(parseFile,implicitRelation)
		try:
			feature.setClassLabel(implicitRelation["Sense"][0])
		except:
			pass
		featureCollection.append(feature)
#		if(num>10):
#			exit()
		num+=1
	for feature in featureCollection:
		feature.productionRuleCutoff()
	return featureCollection

def runCompleteSystem():
	if(len(sys.argv)<4):
		print "Please train and test document parses and relation data folder location , and also brown cluster location"
		exit()
	trainDocumentLocation=sys.argv[1]+"parses.json"
	trainRelationLocation=sys.argv[1]+"relations.json"

	testDocumentLocation=sys.argv[2]+"parses.json"
	testRelationLocation=sys.argv[2]+"relations-no-senses.json"
#	testRelationLocation=sys.argv[2]+"relations.json"
	
	trainDocumentList,trainRelationList=readDocuments(trainDocumentLocation,trainRelationLocation)
	testDocumentList,testRelationList=readDocuments(testDocumentLocation,testRelationLocation)


	readBrownClusters(sys.argv[3])

	trainImplicitRelationList,trainExplicitRelationList=divideRelationsFinal(trainRelationList)
	testImplicitRelationList,testExplicitRelationList=divideRelationsFinal(testRelationList)

	finalResults={}
#-------------Explict Relations --------------------------
	trainExplicitFeatureCollection=explictFeatureGeneration(trainDocumentList,trainExplicitRelationList)
	testExplicitFeatureCollection=explictFeatureGeneration(testDocumentList,testExplicitRelationList)

	trainModel(trainExplicitFeatureCollection,"explicitModel")
	
	results=simpleTrainedModelRun(testExplicitFeatureCollection,"explicitModel","explicitRelation",False)
	for num in range(0,len(results)):
		finalResults[testExplicitRelationList[num]["ID"]]=results[num]
	
#-------------Implict Relations --------------------------

	trainImplicitFeatureCollection=implicitFeatureGeneration(trainDocumentList,trainImplicitRelationList)
	testImplicitFeatureCollection=implicitFeatureGeneration(testDocumentList,testImplicitRelationList)

	trainModel(trainImplicitFeatureCollection,"implicitModel")
	results=simpleTrainedModelRun(testImplicitFeatureCollection,"implicitModel","implicitRelation",False)
	for num in range(0,len(results)):
		finalResults[testImplicitRelationList[num]["ID"]]=results[num]
	for testRelation in testRelationList:
	 	testRelation["Sense"]=[finalResults[testRelation["ID"]]]
		if(testRelation["Connective"]["RawText"]==""):
			testRelation["Type"]="Implicit"
		else:
			testRelation["Type"]="Explicit"

	 	testRelation["Connective"]["TokenList"]=[token[2] for token in testRelation["Connective"]["TokenList"]]
	 	testRelation["Arg1"]["TokenList"]=[token[2] for token in testRelation["Arg1"]["TokenList"]]
	 	testRelation["Arg2"]["TokenList"]=[token[2] for token in testRelation["Arg2"]["TokenList"]]
	FD=open("finalResult.json","w")
	for testRelation in testRelationList:
		json.dump(testRelation,FD)
		FD.write("\n")
	FD.close()
if __name__=='__main__':
	runCompleteSystem()
	exit()
	if(len(sys.argv)<4):
		print "Please train and test document parses and relation data folder location , and also brown cluster location"
		exit()

	trainDocumentLocation=sys.argv[1]+"parses.json"
#	trainRelationLocation=sys.argv[1]+"relations-no-senses.json"
	trainRelationLocation=sys.argv[1]+"relations.json"

	testDocumentLocation=sys.argv[2]+"parses.json"
#	testRelationLocation=sys.argv[2]+"relations-no-senses.json"
	testRelationLocation=sys.argv[2]+"relations.json"
	
	trainDocumentList,trainRelationList=readDocuments(trainDocumentLocation,trainRelationLocation)
	testDocumentList,testRelationList=readDocuments(testDocumentLocation,testRelationLocation)


	readBrownClusters(sys.argv[3])

	trainImplicitRelationList,trainExplicitRelationList=divideRelations(trainRelationList)
	testImplicitRelationList,testExplicitRelationList=divideRelations(testRelationList)


#	trainExplicitFeatureCollection=explictFeatureGeneration(trainDocumentList,trainExplicitRelationList)


#	trainModel(trainExplicitFeatureCollection,"explicitModel")

#	testExplicitFeatureCollection=explictFeatureGeneration(testDocumentList,testExplicitRelationList)
	
#	simpleTrainedModelRun(testExplicitFeatureCollection,"explicitModel","explicitRelation")
	

	trainImplicitFeatureCollection=implicitFeatureGeneration(trainDocumentList,trainImplicitRelationList)
	testImplicitFeatureCollection=implicitFeatureGeneration(testDocumentList,testImplicitRelationList)

	trainModel(trainImplicitFeatureCollection,"implicitModel")
	simpleTrainedModelRun(testImplicitFeatureCollection,"implicitModel","implicitRelation")

