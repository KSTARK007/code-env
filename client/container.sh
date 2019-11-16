#!/bin/bash

# docker build -t coder .

# docker run -v ~/Documents/Sem7/ProjSE/client/information:/information coder ./run.sh 1 python 1

# container.sh 1 python 1 s1

problem_id=$1;
language=$2;
timelimit=$3;
usn=$4;
extension=$5;
docker run -v ~/Documents/Sem7/ProjSE/codeEnv/information:/information -p 8080:8080 coder ./run.sh $problem_id $language $timelimit

codelocation='code=@/home/kavya/Documents/Sem7/ProjSE/codeEnv/information/'$problem_id'/codes/code'$extension
output=$(cat ~/Documents/Sem7/ProjSE/codeEnv/information/$problem_id/logs/test_cases_output | tr "\n" "_")
status='status='$output

curl -w "%{http_code}\n" -X POST -F "language="$language \
-F $status \
-F $codelocation \
http://127.0.0.1:5000/codecouch/submission/$problem_id/$usn 
