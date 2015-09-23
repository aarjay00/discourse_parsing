
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
import time
from nltk.classify import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from util import *
from feature import *
from analysis import *

from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
def genModel(corpus):
#	classifier = nltk.classify.NaiveBayesClassifier.train(corpus)
#	classifier = nltk.classify.MaxentClassifier.train(corpus,"GIS", trace=0, max_iter=100)
#	classifier=SklearnClassifier(maxent(class_weight={1:1.1,0:1.0})).train(corpus)
#	classifier=SklearnClassifier(maxent(solver="liblinear")).train(corpus)
	classifier=SklearnClassifier(maxent()).train(corpus)
#	classifier=SklearnClassifier(MultinomialNB(fit_prior=False)).train(corpus)
#	classifier=SklearnClassifier(SVC(probability=True , class_weight={1:1,0:.5})).train(corpus)
#	classifier.show_most_informative_features(50)
	return classifier


def genConnSpecCorpus(corpus):
	connSpecCorpus={}
	for sample in corpus:
		if(sample[0]["wordFeature"] not in connSpecCorpus.keys()):
			connSpecCorpus[sample[0]["wordFeature"]]=[]
		connSpecCorpus[sample[0]["wordFeature"]].append(sample)
	return connSpecCorpus



def runModel(corpus,corpus2,corpus_f,corpus_l,corpus_n,cycleLen,jointModel):
	combinedData=zip(corpus,corpus_f,corpus_l,corpus_n)
#	for i in range(0,10):
#		np.random.seed()
#		np.random.shuffle(corpus)
	corpus,corpus_f,corpus_l,corpus_n=zip(*combinedData)
	
	avg_p=0.0
	avg_r=0.0
	avg_f=0.0
	avg_acc=0.0
	err=[]
	for iteration in range(0,cycleLen):
		print "Iteration",iteration,"-"*50
		size=len(corpus)/cycleLen
		start=size*iteration
		end=start+size
		test_f=corpus_f[start:end]
		test_l=corpus_l[start:end]
		test_n=corpus_n[start:end]
		train=corpus[:start]+corpus[end+1:]
		trainConnSpec=genConnSpecCorpus(corpus2[:start]+corpus2[end+1:])
		tp=0
		tn=0
		fp=0
		fn=0
	
		classifier=genModel(train)
		tNum=0
		for testInst in test_f:
			pdist=classifier.prob_classify(testInst)
			totalProb=pdist.prob("Yes")
			if(jointModel):
				try:
					classifierConnSpec=genModel(trainConnSpec[testInst["wordFeature"]])
					pdistConnSpec=classifierConnSpec.prob_classify(testInst)
					factor=len(trainConnSpec[testInst["wordFeature"]])
					factor=1.0*factor/(factor+50)
					factor=.50
					totalProb=pdist.prob("Yes")*(1-factor)+pdistConnSpec.prob("Yes")*factor
				except:
					FD=open("noConnSpec","a")
					FD.write(testInst["wordFeature"]+"\n")
					FD.close()
			if((totalProb>.5 and pdist.prob("Yes")<.5) or (totalProb<.5 and pdist.prob("Yes")>.5)):
				print "change",totalProb,pdist.prob("Yes"),pdistConnSpec.prob("Yes"),test_l[tNum],factor
				print testInst["wordFeature"]
#			if(pdist.prob("Yes") >= pdist.prob("No")):
			if(totalProb>.5):
				if(test_l[tNum]=="Yes"):
					tp+=1
				else:
					fp+=1
					err.append((test_n[tNum],totalProb))
			else:
				if(test_l[tNum]=="No"):
					tn+=1
				else:
					fn+=1
					err.append((test_n[tNum],totalProb))
			tNum+=1
		print tp,fp,tn,fn	 	
		try:	
			r=1.0*tp/(tp+fn)
		except:
			r=0.0
		try:	
			p=1.0*tp/(tp+fp)
		except:
			p=0.0
		try:
			f=2.0*p*r/(p+r)
		except:
			f=0.0
		acc=1.0*(tp+tn)/(tp+tn+fp+fn)
		avg_p=(avg_p*iteration+p)/(iteration+1)
		avg_r=(avg_r*iteration+r)/(iteration+1)
		avg_f=(avg_f*iteration+f)/(iteration+1)
		avg_acc=(avg_acc*iteration+acc)/(iteration+1)
	print round(avg_p*100,2),round(avg_r*100,2),round(avg_f*100,2),round(avg_acc*100,2)
	return (avg_p,avg_r,avg_f,avg_acc,err)

			



if(len(sys.argv)<3):
	print "<fListnum> <iterations>"
	exit()


filePath=sys.argv[1]
fileFD=codecs.open(filePath,"rb")
fcollec=pickle.load(fileFD)
fileFD.close()



print "Features Used"
featureDesc=[]
fnum=0
for feat in fcollec[0][1]:
	takeFeature=raw_input("Include:"+feat[0]+"?")
	if(takeFeature=='y'):
		featureDesc.append(feat[0])
	fnum+=1
print ""
print fnum

print "featureDesc ","".join(i+" " for i in featureDesc)

featureDesc2=[]


jointModel=False
secondFeatureCollection=raw_input("take second featureset?")
if(secondFeatureCollection=="y"):
	jointModel=True
	fnum=0
	for feat in fcollec[0][1]:
		takeFeature=raw_input("Include:"+feat[0]+"?")
		if(takeFeature=='y'):
			featureDesc2.append(feat[0])
	fnum+=1
	print ""
	print fnum

print "featureDesc2 ","".join(i+" " for i in featureDesc2)



corpus=[]
corpus_f=[]
corpus_l=[]
corpus_n=[]

corpus2=[]

for f in fcollec:
	d={}
	d2={}
	label=f[2]
	features=f[1]
	for feature in features:
		if(feature[0] in featureDesc):
			d[feature[0]]=feature[1]
		if(feature[0] in featureDesc2):
			d2[feature[0]]=feature[1]
	corpus.append((d,label))
	corpus2.append((d,label))
	corpus_f.append(d)
	corpus_l.append(label)
	corpus_n.append(f[0])

iterations=int(sys.argv[2])
a,b,c,d,e=runModel(corpus,corpus2,corpus_f,corpus_l,corpus_n,iterations,jointModel)
#print e

descCollection=[]

for i in e:
	descCollection.append(loadModel("processedData/featureCollection/"+str(i[0])))
	descCollection[-1].addAttr("extraAttr",str(i[1]))

basicAnalysis(descCollection,"connective_identification")

FD=open("nltk_accuracy","a")
if(not jointModel):
	FD.write("".join(i+" " for i in featureDesc)+"\n")
else:
	FD.write("Model1"+"".join(i+" " for i in featureDesc)+"\n")
	FD.write("Model2"+"".join(i+" " for i in featureDesc2)+"\n")

FD.write(str(round(a*100,2))+" "+str(round(b*100,2))+" "+str(round(c*100,2))+" "+str(round(d*100,2))+"\n")

#exportModel("./dependedencyProbabilities",collec)
