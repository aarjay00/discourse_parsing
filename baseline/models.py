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
from annotated_data import *
from feature import *
from analysis import *


from sklearn.linear_model import LogisticRegression as maxent
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier

from sklearn.svm import SVC
from sklearn.lda import LDA
from sklearn.qda import QDA
from random import shuffle
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB


def genModel(classList):
	classWeight={}
	for classLabel in classList:
		classWeight[classLabel]=1.0
	model=maxent(solver='liblinear',class_weight=classWeight)
#	model=maxent(dual=True,solver='lbfgs' , max_iter=200)
#	model=tree.DecisionTreeClassifier()
#	model=AdaBoostClassifier(n_estimators=100)
#	model=MultinomialNB()
#	model=Perceptron(n_iter=10)
#	model=SGDClassifier()
#	model=SVC()
#	model=LDA(solver='svd')
#	model=QDA()
	return model


def runModel(featureCollection,featureDescCollection,classList,cycleLen,yesWt=1,noWt=1):
	combinedData=zip(featureCollection,featureDescCollection)
	shuffle(combinedData)
	featureCollection,featureDescCollection=zip(*combinedData)
	avgPrecision={}
	avgRecall={}
	avgModelScore={}
	errorCollection=[]
	
	for classLabel in classList:
		avgPrecision[classLabel]=0.0
		avgRecall[classLabel]=0.0
		avgModelScore[classLabel]=0.0

	fn={}
	fp={}
	for iteration in range(0,cycleLen):
		print "Iteration",iteration,"-"*50
		size=len(featureCollection)/cycleLen
		start=size*iteration
		end=start+size
#		print start,end
		test=featureCollection[start:end]
		testDesc=featureDescCollection[start:end]
		train=featureCollection[:start]+featureCollection[end+1:]
#		print len(test),len(train)

		dataSet,dataLabels=convertDataSet(train)

		model=genModel(classList)
		model.fit(dataSet,dataLabels)
		
		truePositives={}
		falsePositives={}
		gold={}
		precision={}
		recall={}

		for classLabel in classList:
			truePositives[classLabel]=0
			falsePositives[classLabel]=0
			gold[classLabel]=0
			precision[classLabel]=0.0
			recall[classLabel]=0.0

		d,l=convertDataSet(test)
		print "model score",model.score(d,l)
		featureNum=0
		for feature in test:

			arr=numpy.array(feature.featureVector)
			result=model.predict(arr)[0]
			if(result==feature.classLabel):
				truePositives[feature.classLabel]+=1
			else:
			 	falsePositives[feature.classLabel]+=1
			 	print "wrong here !!!"
			 	errorCollection.append(testDesc[featureNum])

			gold[feature.classLabel]+=1
			featureNum+=1	
		for classLabel in classList:	
			try:
				precision[classLabel]=(1.0*truePositives[classLabel])/(truePositives[classLabel]+falsePositives[classLabel])
				avgPrecision[classLabel]=(avgPrecision[classLabel]*iteration + precision[classLabel])/(iteration+1)
			except:
				print "e1"
			try:
				recall[classLabel]=(1.0*truePositives[classLabel])/(gold[classLabel])
				avgRecall[classLabel]=(avgRecall[classLabel]*iteration + recall[classLabel])/(iteration+1)
			except:
				print "e2"
			try:
				print "Precision : %f Recall %f"%(precision[classLabel],recall[classLabel])
			except:
				print "e3"
			avgModelScore[classLabel]=(avgModelScore[classLabel]*iteration+model.score(d,l))/(iteration+1)
	print "Final",avgPrecision,avgRecall

	FD=open("results.txt","a")
	for classLabel in classList:
		FD.write(classLabel+"\n")
		FD.write(str(avgPrecision[classLabel])+" "+str(avgRecall[classLabel])+" "+str(avgModelScore[classLabel])+" "+str((2*avgPrecision[classLabel]*avgRecall[classLabel])/(avgRecall[classLabel]+avgPrecision[classLabel]))+"\n")
	#	FD.write(str(avgPrecision[classLabel])+" "+str(avgRecall[classLabel])+" "+str(avgModelScore[classLabel])+"\n")
	FD.close()

	basicAnalysis(errorCollection)

#	return (avgPrecision,avgRecall,avgModelScore,(2*avgPrecision*avgRecall)/(avgRecall+avgPrecision))
	exit()


# USELESS STUFF not willing to delete yet :P--------------------------------------------------------------------

	FD=open("issues","w")
	sum=0
	FD.write(str("false positives"+str(len(fp)))+"\n")
	for key,value in fp.items():
		FD.write(key+" "+str(value[0])+"\n")
		sum+=value[0]
	FD.write(str(sum)+"\n")
	sum=0
	FD.write(str("false negatives"+str(len(fn)))+"\n")
	for key,value in fn.items():
		sum+=value[0]
		FD.write(key+" "+str(value[0])+"\n")
	FD.write(str(sum)+"\n")
	FD.close()

	for feature in fp[u'\u0914\u0930'][1]:
#	if(feature.connective==u'\u0932\u0947\u0915\u093f\u0928'):
		if(feature.connective==u'\u0914\u0930'):
			print "Label",feature.classLabel,"-"*30
			sentenceNum=feature.globalWordList[feature.conn[0]].sentenceNum
			sentence=feature.discourseFile.sentenceList[sentenceNum]
			chunkNum=0
			before=False
			after=False
			middle=False
			for chunk in sentence.chunkList:
				if(chunk.chunkTag[:2]=="VG"):
					if(middle==False):
						before=True
					else:
						after=True
				for word in chunk.wordNumList:
					if(feature.discourseFile.globalWordList[word].word==u'\u0914\u0930'):
						middle=True
					print feature.discourseFile.globalWordList[word].word,
				print chunk.chunkTag+"0",chunkNum,
				chunkNum+=1
			print ""
