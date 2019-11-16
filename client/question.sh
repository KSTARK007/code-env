#!/bin/bash
echo  hello owrl;
problem_id=$1;
usn=$2
echo $problem_id;
echo $uns;

if [ -d "./information/"$problem_id ]
then
	echo "done"
else
	mkdir "./information/"$problem_id 2> /dev/null
	mkdir "./information/"$problem_id"/codes/" 2> /dev/null
	mkdir "./information/"$problem_id"/test_cases/" 2> /dev/null
	mkdir "./information/"$problem_id"/logs/" 2> /dev/null

	num=$(curl -s -w "" -X GET "http://127.0.0.1:5000/codecouch/question/?Usn="$usn"&Q_id="$problem_id \
	| python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["number_testcases"])')

	for i in $(seq 1 $num);
	do
		curl -X GET http://127.0.0.1:5000/codecouch/testcases/$problem_id/ip/$i > "./information/"$problem_id"/test_cases/"ip$i
		curl -X GET http://127.0.0.1:5000/codecouch/testcases/$problem_id/op/$i > "./information/"$problem_id"/test_cases/"op$i
	done
fi
