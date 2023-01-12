#!/bin/bash

# # curl -w "%{http_code}\n" http://127.0.0.1:5000/codecouch/student/1237

# curl -w "%{http_code}\n" -X POST -d "Usn=s1&Name=Plato&Batch=100&Section=C&Department=Philosophy&Password=poison" http://127.0.0.1:5000/codecouch/login/

# # curl -w "%{http_code}\n" http://127.0.0.1:5000/codecouch/faculty/12e

# curl -w "%{http_code}\n" -X PUT -d "Name=Socrates&Department=Philosophy" http://127.0.0.1:5000/codecouch/faculty/f1

# # curl -w "%{http_code}\n" -X GET -d "Usn=AB&Password=CSE" http://127.0.0.1:5000/codecouch/login/


# # curl -w "%{http_code}\n" -X GET -d "Usn=f1&Password=poison" http://127.0.0.1:5000/codecouch/login/

# curl -w "%{http_code}\n" -X POST -F 'Usn=f1' -F 'Question_name=Beginning in Athens' \
# -F 'Tags=Holy Water' \
# -F 'description=@./description' \
# -F 'op1=@./op1' \
# -F 'op2=@./ip2' \
# -F 'op3=@./ip3' \
# -F 'ip1=@./ip1' \
# -F 'ip2=@./ip2' \
# -F 'ip3=@./ip3' \
# http://127.0.0.1:5000/codecouch/question/

# curl -w "%{http_code}\n" -X GET -d "Usn=s1&Q_id=15" http://127.0.0.1:5000/codecouch/question/

# curl -w "%{http_code}\n" -X GET -d "Last=-1&Number=4&Tag=&Faculty=f3" http://127.0.0.1:5000/codecouch/questions/

# curl -w "%{http_code}\n" -X GET http://127.0.0.1:5000/codecouch/testcases/8/ip/2

curl -w "%{http_code}\n" -X POST -F 'Usn=f1' -F 'Question_name=Binary Search' \
-F 'Tags=algo ds' \
-F 'description=@./description' \
-F 'op1=@./op1' \
-F 'op2=@./ip2' \
-F 'op3=@./ip3' \
-F 'ip1=@./ip1' \
-F 'ip2=@./ip2' \
-F 'ip3=@./ip3' \
http://127.0.0.1:5000/codecouch/question/