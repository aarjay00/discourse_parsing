
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
from nltk.classify import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from util import *
from feature import *
from analysis import *

def genModel(corpus):
#	classifier = nltk.classify.NaiveBayesClassifier.train(corpus)
#	classifier = nltk.classify.MaxentClassifier.train(corpus,"GIS", trace=0, max_iter=100)
	classifier=SklearnClassifier(maxent()).train(corpus)
#	classifier.show_most_informative_features(50)
	return classifier

def runModel(corpus,corpus_f,corpus_l,corpus_n,cycleLen):
	combinedData=zip(corpus,corpus_f,corpus_l,corpus_n)
	for i in range(0,20):
		np.random.shuffle(corpus)
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
		tp=0
		tn=0
		fp=0
		fn=0
		
		classifier=genModel(train)
		tNum=0
		for testInst in test_f:
			pdist=classifier.prob_classify(testInst)
			if(pdist.prob("Yes") >= pdist.prob("No")):
				if(test_l[tNum]=="Yes"):
					tp+=1
				else:
					fp+=1
					err.append(test_n[tNum])
			else:
				if(test_l[tNum]=="No"):
					tn+=1
				else:
					fn+=1
					err.append(test_n[tNum])
			tNum+=1
		print tp,fp,tn,fn	 	
		try:	
			p=1.0*tp/(tp+fn)
		except:
			p=0.0
		try:	
			r=1.0*tp/(tp+fp)
		except:
			r=0.0
		try:
			f=2.0*p*r/(p+r)
		except:
			f=0.0
		acc=1.0*(tp+tn)/(tp+tn+fp+fn)
		avg_p=(avg_p*iteration+p)/(iteration+1)
		avg_r=(avg_r*iteration+r)/(iteration+1)
		avg_f=(avg_f*iteration+f)/(iteration+1)
		avg_acc=(avg_acc*iteration+acc)/(iteration+1)
	print avg_p,avg_r,avg_f,avg_acc
	return (avg_p,avg_r,avg_f,avg_acc,err)

			



if(len(sys.argv)<3):
	print "<fListnum> <iterations>"
	exit()


filePath=sys.argv[1]
fileFD=codecs.open(filePath,"rb")
fcollec=pickle.load(fileFD)
fileFD.close()


corpus=[]
corpus_f=[]
corpus_l=[]
corpus_n=[]

print "Features Used"
featureDesc=[]
featureDescNot=[]
fnum=0
for feat in fcollec[0][1]:
	takeFeature=raw_input("Include:"+feat[0]+"?")
	if(takeFeature=='y'):
		featureDesc.append(feat[0])
	else:
		featureDescNot.append(feat[0])
	fnum+=1
print ""
print fnum

print "featureDesc ","".join(i+" " for i in featureDesc)

for f in fcollec:
	d={}
	label=f[2]
	features=f[1]
	for feature in features:
		if(feature[0] in featureDesc):
			d[feature[0]]=feature[1]
	corpus.append((d,label))
	corpus_f.append(d)
	corpus_l.append(label)
	corpus_n.append(f[0])

iterations=int(sys.argv[2])
a,b,c,d,e=runModel(corpus,corpus_f,corpus_l,corpus_n,iterations)
print e

descCollection=[]

for i in e:
	descCollection.append(loadModel("processedData/featureCollection/"+str(i)))

basicAnalysis(descCollection,"connective_identification")

FD=open("nltk_accuracy","a")
FD.write("".join(i+" " for i in featureDesc)+"\n")
FD.write(str(round(a*100,2))+" "+str(round(b*100,2))+" "+str(round(c*100,2))+" "+str(round(d*100,2))+"\n")
