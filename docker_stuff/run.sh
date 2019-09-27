#!/bin/bash

: '
	0: successful
	1: compilation error -> /logs/compilation_error
	2: test case error -> /logs/test_cases
'

path='../information/';
problem_id=$1;
language=$2;
n_test_cases=$(ls $path/$problem_id/test_cases/ip* | wc | awk '{print $1}');

truncate -s 0 $path/$problem_id/logs/compilation_error;
truncate -s 0 $path/$problem_id/logs/test_cases_error;

if [[ $language == "cpp" ]]
then
	echo "g++";
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
		$path/$problem_id/codes/a.out < $path/$problem_id/test_cases/ip$i > $path/$problem_id/test_cases/currop;
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
	echo "python";
fi

echo 0;