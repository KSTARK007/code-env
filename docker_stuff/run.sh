#!/bin/sh

: '	
	0: successful
	1: compilation error -> /logs/compilation_error
	2: test case error -> /logs/test_cases_error
	3: test case error -> /logs/test_cases_timeout
'

path='/information';
problem_id=$1;
language=$2;
n_test_cases=$(ls $path/$problem_id/test_cases/ip* | wc | awk '{print $1}');

# clearing out all the existing files
truncate -s 0 $path/$problem_id/logs/compilation_error;
truncate -s 0 $path/$problem_id/logs/test_cases_error;
truncate -s 0 $path/$problem_id/logs/test_cases_timeout;
truncate -s 0 $path/$problem_id/test_cases/currop;


# Selection of language
if [[ $language == "cpp" ]]
then
	# Compiling the code, renaming the exec file and outputing the stderr into a different file
	g++ $path/$problem_id/codes/code.c -o $path/$problem_id/codes/a.out 2> $path/$problem_id/logs/compilation_error;

	# if error(system or compilation) encountered the return 1 and exit 
	if [[ $? -ne 0 ]]
	then
		echo 1;
		exit;
	fi
	# for each testcase in the file run the folling code
	for i in $(seq 1 $n_test_cases);
	do
		# execute the exec file for x seconds after which it will be terminated 
		# take input from the file and output it to a different file
		timeout 1 $path/$problem_id/codes/a.out < $path/$problem_id/test_cases/ip$i > $path/$problem_id/test_cases/currop
		
		if [[ $? -ne 0 ]]
		then
		# in case the program takes more then x seconds we output the testcase number and the error code 3 
			echo $i > $path/$problem_id/logs/test_cases_timeout;
			echo 3;
			exit;
		fi
		
		# compare the difference between the given output of the test case and the computed output for the testcase
		differences=$(diff $path/$problem_id/test_cases/currop $path/$problem_id/test_cases/op$i | wc | awk '{print $1}');

		if [[ $differences -ne 0 ]]
		then
			# if there is a difference between the two then output the testcase number and the error code 2
			echo $i > $path/$problem_id/logs/test_cases_error;
			echo 2;
			exit;
		fi
	done
fi

if [[ $language == "c" ]]
then
	gcc $path/$problem_id/codes/code.c -o $path/$problem_id/codes/a.out 2> $path/$problem_id/logs/compilation_error;

	if [[ $? -ne 0 ]]
	then
		echo 1;
		exit;
	fi

	for i in $(seq 1 $n_test_cases);
	do
		timeout 1 $path/$problem_id/codes/a.out < $path/$problem_id/test_cases/ip$i > $path/$problem_id/test_cases/currop
		
		if [[ $? -ne 0 ]]
		then
			echo $i > $path/$problem_id/logs/test_cases_timeout;
			echo 3;
			exit;
		fi
		

		differences=$(diff $path/$problem_id/test_cases/currop $path/$problem_id/test_cases/op$i | wc | awk '{print $1}');

		if [[ $differences -ne 0 ]]
		then
			echo $i > $path/$problem_id/logs/test_cases_error;
			echo 2;
			exit;
		fi
	done	
fi

if [[ $language == "python" ]]
then
	for i in $(seq 1 $n_test_cases);
	do
		timeout 1 python3 $path/$problem_id/codes/code.py < $path/$problem_id/test_cases/ip$i > $path/$problem_id/test_cases/currop 2> $path/$problem_id/logs/compilation_error
		
		error=$?;

		if [[ $error -eq 1 ]]
		then
			echo 1;
			exit;
		elif [[ $error -ne 0 ]]
		then
			echo $i > $path/$problem_id/logs/test_cases_timeout;
			echo 3;
			exit;
		fi
		

		differences=$(diff $path/$problem_id/test_cases/currop $path/$problem_id/test_cases/op$i | wc | awk '{print $1}');

		if [[ $differences -ne 0 ]]
		then
			echo $i > $path/$problem_id/logs/test_cases_error;
			echo 2;
			exit;
		fi
	done
fi

echo 0;
