#!/bin/bash
if [ $# == 0 ]
then
	echo "3 arguments"
	exit
fi
file_name=$1
sentence_num=$2
dat_type=$3


if [ "$dat_type" == "graph" ]
then
	file_path="$(tree -if -L 2  dependencyTreeGraph | grep $file_name)"
	echo $file_path
#	if [ $sentence_num == -1 ]
#	then
	gedit "$file_path""/sentenceInfo" &
#	else
	killall eog
	eog "$file_path""/""$sentence_num"".png" &
#	fi
else	
	file_path="$(tree -if -L 2 ../data/$dat_type | grep $file_name)"
	echo $file_path
	gedit $file_path &
fi
