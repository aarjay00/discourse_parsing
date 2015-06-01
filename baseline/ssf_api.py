#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import ssf
from util import *

def extractSSFannotations(filePath):
	filePath=filePath.replace("/raw/","/ssf/")
	if not fileExists(filePath) :
		print "No file found"
		return None
	node =ssf.node()
	print "ssf from " , filePath,os.path.isfile(filePath)
	node.read_ssf_from_file(filePath)
	

