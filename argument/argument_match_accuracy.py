#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from ssf_api import *
from annotated_data import *


def compareSpans(originalSpan, generatedSpan):
	if(originalSpan==generatedSpan):
		return "Exact-Match"


	contained=True
	for pos in originalSpan:
		if(pos not in generatedSpan):
			contained=False
			break
	if(contained):
		return "Extra-Match"
	contained=True
	for pos in generatedSpan:
		if(pos not in originalSpan):
			contained=False
			break
	if(contained):
		return "Less-Match"
	for pos in generatedSpan:
	 	if(pos in originalSpan):
			return "OverLap"
	return "No-Match"

def checkArgumentMatch(conn,genArg1Span,genArg2Span,wordList):
	arg1Span=wordList[conn[0]].arg1Span
	arg2Span=wordList[conn[0]].arg2Span
	arg1Result=compareSpans(arg1Span,genArg1Span)
	arg2Result=compareSpans(arg2Span,genArg2Span)
	return (arg1Result,arg2Result)
