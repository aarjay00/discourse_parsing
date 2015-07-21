rm -rf ssf/*
for directory in ann/* ;
do
	new_directory="$(echo $directory | cut -d'/' -f2)"
	echo $directory
	mkdir -p "ssf_1/"$new_directory
	for files in $directory/*;
	do
		file="$(echo $files | cut -d'/' -f3 | cut -d'_' -f3)"
		ssf_file="$(tree -fi ../hdtb/HDTB_pre_release_version-0.03/IntraChunk/SSF/utf/  | grep $file  )"
		filename="$(echo $files | cut -d'/' -f3)"
		if [ "$ssf_file" == "" ]
		then
			echo "original file name "$files
			echo "searching for file num" $file
			echo $filename" ssf file not present"
			continue
		fi
#		echo $file
#		echo $ssf_file
		cp $ssf_file "ssf_1/"$new_directory/$filename
	done
done
