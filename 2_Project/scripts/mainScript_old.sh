#!/bin/bash

clear

#############
# GLOBAL VAR
#############
filename=".pathForAIDS"
repoPath=""
professor_dir="/output_files_professor"
professor_file=""
temp_file="tempfile.txt"
string_type=""
runningType=""

#############
#  COLORS
#############

red='\033[0;31m'
lightRed='\e[91m'
green='\e[32m'
lightYellow='\e[93m'
blue='\e[34m'
lightMagenta='\e[95m'
white='\e[97m'
lightCyan='\e[96m'
cyanBackground='\e[46m'
NC='\033[0m'
reset='\e[0m'

#############
# FUNCTIONS
#############

printFile()
{
	printf ""$lightMagenta"####################$NC"; echo ""
	printf ""$blue"File's Content"; echo "";
	printf ""$lightMagenta"####################$white"; echo "";echo "";
	cat $1;
}

ourAnswer()
{
	echo "";printf ""$lightMagenta"####################$NC"; echo ""
	printf ""$green"Our Answer"; echo "";
	printf ""$lightCyan"For type "$cyanBackground""$white"$1$reset"; echo "";
	printf ""$lightMagenta"####################$white"; echo "";echo "";
}

answerFromProf()
{
	answer_dir=$1$professor_dir
	length_answer=$(echo -n $answer_dir | wc -c)
	length_answer=$((length_answer+1))

	for prof_answers in "$answer_dir"/*
	do
		#echo "$test_File"
		answers_File_no_path=$(echo $prof_answers)
		answers_no_path=${answers_File_no_path:length_answer}
		
		#echo "$answers_no_path" #Nome do ficheiro
		string_ini="${answers_no_path#*_}"; #echo "${string_ini}" # See the file name from professor

		if [ $string_ini = $2 ]; then
            
			string_type="${answers_no_path%_*}";

			echo "";printf ""$lightMagenta"####################$NC"; echo ""
			printf ""$lightRed"Professor's Answer"; echo "";
			printf ""$lightCyan"For type "$cyanBackground""$white"$string_type$reset"; echo "";
			printf ""$lightMagenta"####################$white"; echo "";echo "";
            
			professor_file="$answer_dir"/"$answers_no_path" #echo "$professor_file"

			cat $professor_file
        fi

	done
	
}

prettyPrint()
{
	echo "";printf ""$lightYellow"###############################################################$NC"; echo ""
	printf ""$green"Processing file →  "$red"$1"; echo "";
	printf ""$lightYellow"###############################################################$NC"; echo "";echo "";
}

readFile()
{
	cd
	pwd=`pwd`
	fileWithPath=$pwd"/"$filename

	if [ -f $fileWithPath ]
	then
		projectFolder="$(cat $fileWithPath)"
		repoPath=$(echo $projectFolder) # Prints the project folder to a variable
	else
		printf ""$green"Please "$red"insert the FULL PATH"$green" to the 2nd Project root$NC";echo ""
		read projectPath
		
		#Create and save a file
		echo "$projectPath" > $fileWithPath

		repoPath=$(echo $projectPath) # Prints the project folder to a variable
	fi
}

main()
{
	readFile
    #echo $repoPath
    cd $(echo $repoPath | tr -d '\r')
    
	# Get test files
	input_files_dir=$repoPath"/tests"

	length_dir=$(echo -n $input_files_dir | wc -c)
	length_dir=$((length_dir+1))


	printf ""$green"Please "$red"insert the number:""$NC";echo "";echo ""
	printf ""$blue"0 - Pedro Ferreira$NC";echo ""
	printf ""$lightYellow"1 - Ruben Tadeia$NC";echo "";echo ""
	read type;
	
	if [ $type = "0" ]
	then
		runningType="convert"
	elif [ $type = "1" ]
	then
		runningType="prover"
	else
		exit
	fi	


	for test_File in "$input_files_dir"/*
	do
		#echo "$test_File"
		test_File_no_path=$(echo $test_File)
		test_File_no_path=${test_File_no_path:length_dir}

		answer_dir=$repoPath$professor_dir
		length_answer=$(echo -n $answer_dir | wc -c)
		length_answer=$((length_answer+1))

		for prof_answers in "$answer_dir"/*
		do
			#echo "$test_File"
			answers_File_no_path=$(echo $prof_answers)
			answers_no_path=${answers_File_no_path:length_answer}
			
			#echo "$answers_no_path" #Nome do ficheiro
			string_ini="${answers_no_path#*_}"; #echo "${string_ini}" # See the file name from professor

			if [ $string_ini = $test_File_no_path ]; then
            
				string_type="${answers_no_path%_*}";
			fi
		done

		if [ $string_type != $runningType ]
		then
			continue;
		fi

		# Removed the path from the file
		prettyPrint $test_File_no_path
		
		printFile $test_File

		answerFromProf $repoPath $test_File_no_path
		
		ourAnswer $runningType
		
		###########################################
		# Project line is this one below
		#
		# Atention a linha que devia ficar era
		# python3 convert.py < $test_File
		#
		# Estou a gravar num ficheiro. E a imprimir
		# num ficheiro para fazer um dif mais tarde
		###########################################
		if [ $type = "0" ]
		then
		#Pedro Ferreira
			python3 convert.py < $test_File >> $temp_file | tail -n 1
			cat $temp_file
		elif [ $type = "1" ]
		then
		#Ruben Tadeia
			python3 prover.py < $test_File >> $temp_file | tail -n 1
			cat $temp_file
		fi	

		echo "";

		if diff $professor_file $temp_file > /dev/null
		then 
			printf ""$blue"Resultado: "$green"Correcto";
		else
			printf ""$blue"Resultado: "$red"Errado";
		fi

		echo "";echo "";

		rm "$temp_file"
	done
	printf "$NC";
}

#############
# MAIN SCRIPT
#############
main