from flask import Flask
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

class Student(Resource):
	# Get relevant details of a student
	@app.route('/<usn>',methods=['GET'])
	def get(self, usn):
		if self.student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM Student WHERE Student_ID="+usn)
			response = cursor.fetchone()
			cur.close()
			return jsonify(data=response), status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	
	# Post the student usn and relevant details to the server
	@app.route('/',methods=['POST'])
	def post(self):
		details = request.form
		usn = details["ID"]
		name = details["Name"]
		section = details["Section"]
		batch = details["Batch"]
		department = details["Department"]
		if not self.student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Student (Student_ID,Student_Name,Batch, Department, Section) VALUES (%s,%s,%s,%s)",(usn,name,batch,section,department,section))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given USN already exists
	
	#Check if entered USN exists already
	def student_exists(self,usn):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM Student WHERE Student_ID="+usn)
		response = cursor.fetchone()
		cur.close()
		if response==None:
			return 0
		return 1
	
class Faculty(Resource):
	# Get relevant details of a faculty
	@app.route('/<f_id>',methods=['GET'])
	def get(self, f_id):
		if self.faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM Faculty WHERE Faculty_ID="+f_id)
			response = cursor.fetchone()
			cur.close()
			return jsonify(data=response), status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	
	# Post the faculty ID and relavant details to the server
	@app.route('/',methods=['POST'])
	def post(self):
		details = request.form
		usn = details["ID"]
		name = details["Name"]
		department = details["Department"]
		if self.faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Faculty (Faculty_ID,Faculty_Name,Department) VALUES (%s,%s,%s)",(usn,name,batch,section,department))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given faculty ID already exists
	
	#Check if entered faculty ID exists already
	def faculty_exists(self,f_id):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM Faculty WHERE Faculty_ID="+f_id)
		response = cursor.fetchall()
		cur.close()
		if response==None or len(response)==0:
			return 0
		return 1
class Tag(Resource,Student,Faculty):
	"""
	Inherits from class student and faculty
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource
		Faculty.__init__()
		Faculty.Resource = Resource
	
	#get the list of tags starting from a given set of letters
	@app.route('/suggestion/<partial_name>',methods=['GET'])
	def get_tag_suggestion(self,partial_name):
		cur = mysql.connection.cursor()
		cur.execute("SELECT Tag_name FROM Tags WHERE Tag_Name LIKE "+partial_name)
		response = cursor.fetchall()
		cur.close()	
		return jsonify(data=response), status.HTTP_200_OK
	#get the list of tags attempted by a student
	@app.route('/student/<usn>',methods=['GET'])
	def get_tag_student(self,usn):
		if Student.student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Tags,Question_attempt,Question_tag WHERE Question_attempt.Student_ID = "+usn+" AND Question_attempt.Question_ID = Question_tag.Question_ID AND Question_tag.Tag_ID = Tags.Tag_ID")
			response = cursor.fetchall()
			cur.close()	
			return jsonify(data=response),status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	
	#get the list of tags attempted by all students under a faculty
	@app.route('/faculty/<f_id>',methods=['GET'])
	def get_tag_faculty(self,f_id):
		if Faculty.faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Teaches,Tags,Question_attempt,Question_tag WHERE Teaches.Faculty_ID = "+f_id+" AND Question_attempt.Student_ID = Teaches.Student_ID AND Question_attempt.Question_ID = Question_tag.Question_ID AND Question_tag.Tag_ID = Tags.Tag_ID")
			response = cursor.fetchall()
			cur.close()	
			return jsonify(data=response),status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	#Post a new tag entry to the database
	@app.route('/add/<tag_name>',methods=['POST'])
	def add_tag(self):
		tag_id = self.retrieve_tag(tag_name)
		details = request.form
		name = details["Name"]
		if not self.tag_exists(tag_id):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Tags (Tag_name) VALUES (%s)",(name))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given tag name already exists
	
	#check if a given tag ID exists
	def tag_exists(self,tag_id):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM Tags WHERE Tag_ID="tag_id)
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
		cur.execute("SELECT Tag_ID FROM Tags WHERE Tag_name="tag_name)
		response = cursor.fetchone()
		cur.close()	
		if response == None or len(response)==0:
			return -1	
		for row in record:
			return row[0]

class Question(Resource,Student,Tag,Faculty):
	"""
	Inherits from class student and tag
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource
		Faculty.__init__()
		Faculty.Resource = Resource
		Tag.__init__()
		Tag.Resource = Resource

	# Get the description and tags of the question using post
	@app.route('/description',methods=['POST'])
	def get_description(self):
		details = request.form
		question_id = details["question_ID"]
		usn = details["Student_ID"]
		if self.is_accessible(question_id,usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Description_Pathway FROM Question WHERE Question_ID="+question_id)
			desc_path = cursor.fetchone()[0]
			cur.close()
			desc = ""
			with open(desc_path,"r") as fp:
				desc = fp.read()
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Question_tag,Tags WHERE Question_Tag.Question_ID="+question_id+" AND Question_tag.Tag_ID = Tags.Tag_ID")
			Tag = cursor.fetchone()[0]
			cur.close()
			return jsonify(data = [desc,tag]),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Student not allowed to access the question
	
	# Get the description and tags of the question using post for the faculty to view
	@app.route('/faculty_description',methods=['POST'])
	def get_description_faculty(self):
		details = request.form
		question_id = details["question_ID"]
		f_id = details["Faculty_ID"]
		if Faculty.faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Description_Pathway FROM Question WHERE Question_ID="+question_id)
			desc_path = cursor.fetchone()[0]
			cur.close()
			desc = ""
			with open(desc_path,"r") as fp:
				desc = fp.read()
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Question_tag,Tags WHERE Question_Tag.Question_ID="+question_id+" AND Question_tag.Tag_ID = Tags.Tag_ID")
			Tag = cursor.fetchone()[0]
			cur.close()
			return jsonify(data = [desc,tag]),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Not a faculty
	
	# Get the test cases for a question
	@app.route('/testcases',methods=['POST'])
	def get_testcases(self):
		details = request.form
		question_id = details["question_ID"]
		usn = details["Student_ID"]
		if self.is_accessible(usn,question_id):
			if not question_attempted(usn,question_id):
				cur = mysql.connection.cursor()
				cur.execute("INSERT INTO Question_attempt (Student_ID,Question_ID) VALUES (%s,%s)",(usn,question_id))
				mysql.connection.commit()
				cur.close()
			cur = mysql.connection.cursor()
			cur.execute("SELECT List_testcases_Pathway FROM Question WHERE Question_ID="+question_id)
			test_path = cursor.fetchone()[0]
			cur.close()
			desc = ""
			cases = []
			with open(desc_path,"r") as fp:
				no_test_cases = int(fp.readline().stripl().split(" ")[0])
				lines = []
				for i in range(no_test_cases):
					line = int(fp.readline().strip())
					lines.append(line)
				for i in lines:
					case = ""
					for j in range(lines):
						line = fp.readline().stripl()
						case = case+"\n"+line
					cases.append(case)
			return jsonify(data = cases),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Student not allowed to access the testcase
	
	# Get the test cases for a question for the faculty to view
	@app.route('/testcases_faculty',methods=['POST'])
	def get_testcases_faculty(self):
		details = request.form
		question_id = details["question_ID"]
		f_id = details["Faculty_ID"]
		if Faculty.faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT List_testcases_Pathway FROM Question WHERE Question_ID="+question_id)
			test_path = cursor.fetchone()[0]
			cur.close()
			desc = ""
			cases = []
			with open(desc_path,"r") as fp:
				no_test_cases = int(fp.readline().stripl().split(" ")[0])
				lines = []
				for i in range(no_test_cases):
					line = int(fp.readline().strip())
					lines.append(line)
				for i in lines:
					case = ""
					for j in range(lines):
						line = fp.readline().stripl()
						case = case+"\n"+line
					cases.append(case)
			return jsonify(data = cases),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Not a faculty
	
	# Post the details of a question and related test cases
	@app.route('/add',methods=['POST'])
	def post(self, faculty_id,*question_details):
		pass
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


class Exam(Resource,Question,Student):
	"""
	Inherits from class student and question
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource
		Question.__init__()
		Question.Resource = Resource

	#get questions of an exam using post
	@app.route('/questions',methods=['POST'])
	def get_questions(self,exam_id,usn):
		details = request.form
		exam_id = details["Exam_ID"]
		usn = details["Student_ID"]
		if self.exam_allowed(usn,exam_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Question_ID FROM Exam_contents WHERE Exam_ID = "+exam_id)
			response = cursor.fetchall()
			cur.close()	
			return jsonify(data=response),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED
		
	#post questions to be provided for the exam
	@app.route('/questions',methods=['POST'])
	def post_questions(self,exam_id,*question_ids):
		details = request.form
		exam_id = details["Exam_ID"]
		question_ids = details["Question_IDs"]
		for question_id in question_ids:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Exam_contents (Question_ID,Exam_ID) values (%s,%s)",(question_id,exam_id))
			response = cursor.fetchall()
			cur.close()	
		return status.HTTP_201_CREATED
		
	#update students to attempt exam using post
	@app.route('/students',methods=['POST'])
	def post_students(self,exam_id,*usns):
		details = request.form
		exam_id = details["Exam_ID"]
		usns = details["Student_IDs"]
		for student_id in student_ids:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Exam_attempt (Student_ID,Exam_ID) values (%s,%s)",(student_id,exam_id))
			response = cursor.fetchall()
			cur.close()	
		return status.HTTP_201_CREATED
		
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

class Submission(Resource,Question):
	"""
	Inherits from class question
	"""
	def __init__(self):
		Question.__init__()
		Question.Resource = Resource

	#gets the test cases and assigns the submission ID
	@app.route('/receive',methods=['POST'])
	def get_testcase(self,question_id,usn):
		if Question.is_accessible(question_id,usn):
			pass
		pass
	
	#posts the submission results for submission ID
	@app.route('/evaluated',methods=['POST'])
	def post(self,submission_id,usn,submission_res):
		if self.submission_exsits(submission_id,usn):
			pass
		pass
	
	#validates if the given submission ID and USN matches
	def submission_exists(self,submission_id,usn):
		return 0
class Student_login(Resource,Student):
	"""
	Inherits from class student
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource

	#Add or update login credentials details using post
	@app.route('/update',methods=['POST'])
	def update(self,username,srn,password):
		if self.credential_exists(username,srn):
			pass
		pass
	
	#Validate login credentials
	@app.route('/validate',methods=['POST'])
	def validate(self,username,password):
		pass
	#Check if given username exists for given usn
	def credential_exists(self,username,usn):
		return 0


class Faculty_login(Resource,Faculty):
	"""
	Inherits from class faculty
	"""
	def __init__(self):
		Faculty.__init__()
		Faculty.Resource = Resource

	#Add or update login credentials details using post
	@app.route('/update',methods=['POST'])
	def update(self,username,f_id,password):
		if self.credential_exists(usn,f_id):
			pass
		pass
	
	#Validate login credentials
	@app.route('/validate',methods=['POST'])
	def validate(self,usn,password):
		pass
	#Check if given username exists for given faculty ID
	def credential_exists(self,username,f_id):
		return 0

class Teaches(Resource,Student,Faculty):
	"""
	Inherits from class student and faculty
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource
		Faculty.__init__()
		Faculty.Resource = Resource

	#Get details of which subjects are taught by faculty to student
	@app.route('/subject/<usn>/<f_id>',methods=['GET'])
	def get_subjects(self,usn,f_id):
		if Student.student_exists(usn) and Faculty.faculty_exists(f_id):
			pass
		pass
	#Get details of the teachers of a student
	@app.route('/faculties/<usn>',methods=['GET'])
	def get_faculties(self,usn):
		if Student.student_exists(usn):
			pass
		pass
	#Get details of students taught by a teacher
	@app.route('/students/<f_id>',methods=['GET'])
	def get_students(self,f_id):
		if Faculty.faculty_exists(f_id):
			pass
		pass
	#Post subjects taught by faculty to server
	@app.route('/',methods=['POST'])
	def post(self,usn,f_id,subject):
		if Student.student_exists(usn) and Faculty.faculty_exists(f_id):
			pass
		pass

class Analysis(Resource,Student,Exam,Faculty,Tag):
	"""
	Inherits from class student
	"""
	def __init__(self):
		Student.__init__()
		Student.Resource = Resource
		Exam.__init__()
		Exam.Resource = Resource
		Faculty.__init__()
		Faculty.Resource = Resource
		Tag.__init__()
		Tag.Resource = Resource

	#get the necessary data for student performance
	@app.route('/student/<usn>',methods=['GET'])
	def get_student_perf(self,usn):
		if Student.student_exists(usn):
			pass
		pass
	#get the data for analysing overall performance of students under a faculty
	@app.route('/faculty/<f_id>',methods=['GET'])
	def get_faculty_perf(self,f_id):
		if Faculty.faculty_exists(f_id):
			pass
		pass
	#get data related to overall performance of a student in an exam
	@app.route('/exam/<exam_id>',methods=['GET'])
	def get_exam_perf(self,exam_id):
		if Exam.exam_exists(exam_id):
			pass
		pass
	#get data related to performance of a student in an exam
	@app.route('/student_exam/<usn>/<exam_id>',methods=['GET'])
	def get_student_exam_perf(self,usn,exam_id):
		if Exam.exam_allowed(exam_id,usn):
			pass
		pass
	#get data related to overall performance of all students on a particular tag
	@app.route('/tag/<usn>',methods=['GET'])
	def get_tag_perf(self,tag_name):
		tag_id = Tag.retrieve_tag(tag_name)
		if Tag.tag_exists(tag_id):
			pass
		pass
	#get list of tags attempted by a student
	@app.route('/tag_list/<usn>',methods=['GET'])
	def get_student_tag_list(self,usn):
		pass
	#get data related to performance of a student on a particular tag
	@app.route('/student_tag/<usn>/<tag_name>',methods=['GET'])
	def get_student_tag_perf(self,usn,tag_name):
		tag_id = Tag.retrieve_tag(tag_name)
		 if Tag.tag_attempted(tag_id,usn):
		 	pass
		 pass
	#get data related to tagwise performance of students under a faculty
	@app.route('/faculty_tagwise/<f_id>',methods=['GET'])
	def get_faculty_tags_perf(self,f_id):
		if Faculty.faculty_exists(f_id):
			pass
		pass
	#get data related to tagwise performance of a student
	@app.route('/student_tagwise/<usn>',methods=['GET'])
	def get_student_tags_perf(self,usn):
		if Student.student_exists(usn):
			pass
		pass
	
api.add_resource(Student, "/student")
api.add_resource(Faculty, "/faculty")
api.add_resource(Tag, "/tag")
api.add_resource(Question, "/question")
api.add_resource(Exam, "/exam")
api.add_resource(Submission, "/submission")
api.add_resource(Student_login, "/studentcred")
api.add_resource(Faculty_login, "/facultycred")
api.add_resource(Teaches, "/teach")
api.add_resource(Analysis,"/analysis")

if __name__=="main":
	app.run(debug=True)
