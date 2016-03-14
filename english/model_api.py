import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
import time
import itertools
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from sklearn.svm import SVC
import operator

from util import *
from feature import *
from analysis import *



def genClassifer(corpus,weight=False):
	if(not weight):
		classifier=SklearnClassifier(maxent()).train(corpus)
	else:
		classifier=SklearnClassifier(maxent(class_weight={1:2,0:1})).train(corpus)
		print "weighted"
	return classifier


def convertFeatureCollection(featureCollection,chooseFeatures=False,chosenFeatures=[]):

	dataSet=[]
	for feature in featureCollection:
		featureVector=feature.featureVector
		for f in featureVector.keys():
			if chosenFeatures and f not in in chosenFeatures:
				del featureVector[f]
		dataSet.append((featureVector,feature.classLabel))
	return dataSet
def featureSelection(featureCollection):
	featureSet=featureCollection[0].featureVector.keys()
	chosenFeatureSet=[]
	print "Choose features to be used"
	for f  in featureSet:
		take=raw_input(f)
		if(take=="y" or take=="Y"):
			chosenFeatureSet.append(f)
	return chosenFeatureSet


def simpleClassify(dataSet,foldNum,weight=False):

	averageAcc=0.0
	dataSize=len(dataSet)
	negativeSamples=[]
	for iteration in range(foldNum):
		start=iteration*(dataSize/foldNum)
		end=start+(dataSize/foldNum)
		testDataSet=dataSet[start:end]
		trainDataSet=dataSet[:start]+dataSet[end+1:]
		classifier=genClassifer(trainDataSet,weight)

		positive=0
		negative=0
		sampleNum=0
		testf=[sample[0] for sample in testDataSet]
		testl=[sample[1] for sample in testDataSet]
		results=classifier.classify_many(testf)
		for sampleNum in range(0,len(results)):
			if(results[sampleNum]==testl[sampleNum]):
				positive+=1
			else:
				negative+=1
			 	negativeSamples.append(sampleNum+start)
		accuracy=1.0*positive/(positive+negative)
#		print "accuracy for round %d is %f"%(iteration,accuracy)
		averageAcc=(averageAcc*iteration+accuracy)/(iteration+1)
	return (averageAcc,negativeSamples)


def featureCombinations(featureCollection,analysisLocation,weight=False):
	featureSet=featureCollection[0].featureVector.keys()
	featureCombo=[combo for x in range(1,len(featureSet)+1) for combo in itertools.combinations(featureSet,x) ]
	print "feature sizes",len(featureCombo)
	resultCollection=[]
	num=0
	for featureSet in featureCombo:
		print num
		dataSet=convertFeatureCollection(featureCollection,True,featureSet)
		acc,err=simpleClassify(dataSet,5,weight)
		resultCollection.append((acc,featureSet,err))
		num+=1
	resultCollection=sorted(resultCollection,key=operator.itemgetter(0))
	for i in resultCollection:
		print i[0],i[1]
	errorCollection = [featureCollection[num] for num in resultCollection[-1][2]]
	studyErrors(errorCollection,analysisLocation)
	return resultCollection[-1]


def runFeatureCombination(featureCollectionLocation,analysisLocation,loadCollection=True,weight=False):	   
	if(loadCollection):
		featureCollection=loadModel(featureCollectionLocation)
	else:
		featureCollection=featureCollectionLocation

	return featureCombinations(featureCollection,analysisLocation,weight)	
def chooseFeatures(featureCollectionLocation):
	featureCollection=loadModel(sys.argv[1])
	chosenFeatureSet=featureSelection(featureCollection)
	
	featureSet=featureCollection[0].featureVector.keys()
	chosenFeatureSet=featureSelection(featureSet)
	dataSet=convertFeatureCollection(featureCollection,True,chosenFeatureSet)
	
	avgAccuracy,errorSamplesNum=simpleClassify(dataSet,10)
	
	errorSamples=[featureCollection[num] for num in errorSamplesNum]
	print "avgAccuracy is ",averageAcc
	studyErrors(errorSamples,"arg2SubTreePos")
def simpleModelRun(featureCollectionLocation,foldNum,analysisLocation,loadCollection=True):
	if(loadCollection):
		featureCollection=loadModel(featureCollectionLocation)
	else:
		featureCollection=featureCollectionLocation

	featureSet=featureCollection[0].featureVector.keys()

	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	avgAccuracy,errorSamplesNum=simpleClassify(dataSet,foldNum)

	errorSamples=[featureCollection[num] for num in errorSamplesNum]
	print "avgAccuracy is ",avgAccuracy
	studyErrors(errorSamples,analysisLocation)


def singleIterationClassify(featureCollection,iterationNum,foldNum,weight=False):
	
	featureSet=featureCollection[0].featureVector.keys()
	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	
	dataSize=len(dataSet)
	start=iterationNum*(dataSize/foldNum)
	end=start+(dataSize/foldNum)
	testDataSet=dataSet[start:end]
	trainDataSet=dataSet[:start]+dataSet[end+1:]
	classifier=genClassifer(trainDataSet,weight)
	testDataSet=[sample[0] for sample in testDataSet]
	return classifier.classify_many(testDataSet)
#	return classifier

def singleIterationClassifyExpand(featureCollection,iterationNum,foldNum,weight=False):
	
	featureSet=featureCollection[0].featureVector.keys()

	dataSize=len(featureCollection)
	start=iterationNum*(dataSize/foldNum)
	end=start+(dataSize/foldNum)
	
	featureCollectionTest=featureCollection[start:end]
	featureCollectionTrain=featureCollection[:start]+featureCollection[end+1:]

	featureCollectionTestExpanded=[]
	for f in featureCollectionTest:
		featureCollectionTestExpanded.extend(f)

	featureCollectionTrainExpanded=[]
	for f in featureCollectionTrain:
		featureCollectionTrainExpanded.extend(f)

	testDataSet=convertFeatureCollection(featureCollectionTestExpanded,False,featureSet)
	trainDataSet=convertFeatureCollection(featureCollectionTrainExpanded,False,featureSet)
	
	classifier=genClassifer(trainDataSet,weight)
	testDataSet=[sample[0] for sample in testDataSet]
	r=classifier.classify_many(testDataSet)

	results=[]
	i=0
	for f in featureCollectionTest:
		results.append(r[i:i+len(f)])
		i+=len(f)
	return results
