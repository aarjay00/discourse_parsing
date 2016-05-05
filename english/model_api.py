import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
import time
import itertools
import matplotlib.pyplot as plt


from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix

import operator

from util import *
from feature import *
from analysis import *



def genClassifer(corpus,weight=False):
	if(not weight):
		logistic=maxent()
#		featureselector=RFE(logistic,step=10)
#		pipeline=Pipeline([('rfe',featureselector),('maxent',logistic)])
		classifier=SklearnClassifier(logistic).train(corpus)
	else:
		classifier=SklearnClassifier(maxent(class_weight={1:2,0:1})).train(corpus)
		print "weighted"
	return classifier


def convertFeatureCollection(featureCollection,chooseFeatures=False,chosenFeatures=[]):

	dataSet=[]
	for feature in featureCollection:
		featureVector=feature.featureVector
		chosenFeatureVector={}
		for f in featureVector.keys():
			if chosenFeatures and f in chosenFeatures:
				chosenFeatureVector[f]=featureVector[f]
		dataSet.append((chosenFeatureVector,feature.classLabel))
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
	negativeSampleLabels=[]

	classifier=genClassifer(dataSet,weight)
	exportModel("./completeModel",classifier)
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
			 	negativeSampleLabels.append(results[sampleNum])
		accuracy=1.0*positive/(positive+negative)
#		print "accuracy for round %d is %f"%(iteration,accuracy)
		averageAcc=(averageAcc*iteration+accuracy)/(iteration+1)
	return (averageAcc,negativeSamples,negativeSampleLabels)


def featureCombinations(featureCollection,analysisLocation,weight=False):
	featureSet=featureCollection[0].featureVector.keys()
	featureCombo=[combo for x in range(1,len(featureSet)+1) for combo in itertools.combinations(featureSet,x) ]
	print "feature sizes",len(featureCombo)
	resultCollection=[]
	num=0
	exit()
	for featureSet in featureCombo:
		print num
		dataSet=convertFeatureCollection(featureCollection,True,featureSet)
		acc,err,errLabel=simpleClassify(dataSet,5,weight)
		resultCollection.append((acc,featureSet,err,errLabel))
		num+=1
	resultCollection=sorted(resultCollection,key=operator.itemgetter(0))
	for i in resultCollection:
		print i[0],i[1]
	errorCollection = [featureCollection[num] for num in resultCollection[-1][2]]
	for errorNum in range(0,len(errorCollection)):
	 	errorCollection[errorNum].featureVector["classifiedAs"]=resultCollection[-1][3][errorNum]
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
	avgAccuracy,errorSamplesNum,errorSampleLabels=simpleClassify(dataSet,foldNum)

	errorSamples=[featureCollection[num] for num in errorSamplesNum]
	for errorSampleNum in range(0,len(errorSamples)):
		errorSamples[errorSampleNum].featureVector["classifiedAs"]=errorSampleLabels[errorSampleNum]
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
def trainModel(featureCollection,modelLocation):

	featureSet=featureCollection[0].featureVector.keys()
	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	classifier=genClassifer(dataSet,False)
	exportModel(modelLocation,classifier)

def simpleTrainedModelRun(featureCollection,modelLocation,analysisLocation):

	featureSet=featureCollection[0].featureVector.keys()
	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	classifier=loadModel(modelLocation)
	
	
	dataSetFeature=[sample[0] for sample in dataSet]
	dataSetLabel=[sample[1] for sample in dataSet]

	results=classifier.classify_many(dataSetFeature)

	sampleNum=0
	positive=0
	negative=0
	errorSamples=[]
	errorSampleLabels=[]

	print(classification_report(dataSetLabel,results))
	print accuracy_score(dataSetLabel,results)
	print precision_score(dataSetLabel,results,average="weighted")
	print recall_score(dataSetLabel,results , average="weighted")
	
	cm=confusion_matrix(dataSetLabel,results)
	np.set_printoptions(precision=2)
	print('Confusion matrix, without normalization')
	print(cm)
	plt.figure()
	plot_confusion_matrix(cm,classifier.labels())
	plt.show()

	for result in results:
		if(result==dataSetLabel[sampleNum]):
			positive+=1
		else:
		 	negative+=1
		 	errorSamples.append(featureCollection[sampleNum])
		 	errorSampleLabels.append(result)
		sampleNum+=1
	avgAccuracy=1.0*positive/(positive+negative)
	for errorSampleNum in range(0,len(errorSamples)):
		errorSamples[errorSampleNum].featureVector["classifiedAs"]=errorSampleLabels[errorSampleNum]
	print "avgAccuracy is ",avgAccuracy
	studyErrors(errorSamples,analysisLocation)
def plot_confusion_matrix(cm,labels, title='Confusion matrix', cmap=plt.cm.Blues):
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(labels))
	plt.xticks(tick_marks,labels, rotation=90)
	plt.yticks(tick_marks, labels)
	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
