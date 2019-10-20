
from flask import Flask, request, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask_mysqldb import MySQL
from flask import jsonify
from flask_api import status


app = Flask(__name__)
api = Api(app)



"""
The contents in post request given as parameters for convenience of representation
Some get requests are made post, to ensure data security
parameters with variable no. of arguments represented by '*' as is the general python syntax
"""

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Coding_Platform'

mysql = MySQL(app)


"""
User helper functions
"""
#Check if entered USN exists already
def user_exists(usn, user_type):
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM {user_type} WHERE {user_type}_ID='{usn}'")
	response = cur.fetchone()
	cur.close()
	if response==None:
		return 0
	return 1

def credential_exists(usn, password, user_type):
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM {user_type}_login WHERE {user_type}_ID='{usn}' AND {user_type}_password='{password}'")
	response = cur.fetchone()
	cur.close()
	if response==None:
		return 0
	return 1
		
def get_user_type(usn):
	cur = mysql.connection.cursor()
	cur.execute(f"SELECT * FROM Student WHERE Student_ID='{usn}'")
	response_student = cur.fetchone()
	cur.execute(f"SELECT * FROM Faculty WHERE Faculty_ID='{usn}'")
	response_faculty = cur.fetchone()
	cur.close()
	if response_student!=None:
		return "Student"
	elif response_faculty!=None:
		return "Faculty"
	return None

"""
Tag helper functions 
"""
#check if a given tag ID exists
def tag_exists(self,tag_id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Tags WHERE Tag_ID="+tag_id)
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1
		
	#check if a student has attempted questions on a given tag
def tag_attempted(self,tag_id,usn):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Question_attempt,Questions WHERE Question_attempt.Student_ID = %s AND Question_attempt.Question_ID = Questions.Question_ID AND Questions.Tag_ID=%s",(usn,tag_id))
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1
	
	#Retrieve the tag ID of given tag name if existant. If not return -1
def retrieve_tag(self,tag_name):
	cur = mysql.connection.cursor()
	cur.execute("SELECT Tag_ID FROM Tags WHERE Tag_name="+tag_name)
	response = cursor.fetchone()
	cur.close()	
	if response == None or len(response)==0:
		return -1	
	for row in record:
		return row[0]

"""
Question helper functions
"""
#validate if the question with the given ID is accessible for the given usn
def is_accessible(self, question_id,usn):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Exam_attempt,Exam_contents WHERE Exam_attempt.Student_ID = %s AND Exam_attempt.Exam_ID = Exam_contents.Exam_ID AND Exam_contents.Question_ID=%s",(usn,exam_id))
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1

		
	#check if a student has attempted questions on a given tag
def question_attempted(self,question_id,usn):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Question_attempt WHERE Student_ID = %s AND Question_ID=%s",(usn,question_id))
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1


"""
Exam helper functions
"""
#verify if the student is allowed to take the exam
def exam_allowed(self,usn,exam_id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Exam_attempt WHERE Student_ID = %s AND Exam_ID=%s",(usn,exam_id))
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1
		
	#verify if the given exam exists
def exam_exists(self,exam_id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM Exam WHERE Exam_ID="+exam_id)
	response = cursor.fetchone()
	cur.close()	
	if response == None:
		return 0	
	return 1

"""
Submission helper functions
"""
#validates if the given submission ID and USN matches
def submission_exists(self,submission_id,usn):
	return 0
		
"""
Student_login helper functions
"""
#Check if given username exists for given usn
def student_credential_exists(self,username,usn):
	return 0

"""
Faculty_login helper functions
"""
#Check if given username exists for given faculty ID
def faculty_credential_exists(self,username,f_id):
	return 0


