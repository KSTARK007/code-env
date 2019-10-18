from helper_functions import *
import os

class Student(Resource):
	# Get relevant details of a student
	@app.route('/<usn>',methods=['GET'])
	def get(self, usn):
		if student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM Student WHERE Student_ID="+usn)
			response = cur.fetchone()
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
		if not student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Student (Student_ID,Student_Name,Batch, Department, Section) VALUES ('%s','%s','%s','%s')",(usn,name,batch,section,department,section))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given USN already exists
	
	
class Faculty(Resource):
	# Get relevant details of a faculty
	@app.route('/<f_id>',methods=['GET'])
	def get(self, f_id):
		if faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM Faculty WHERE Faculty_ID="+f_id)
			response = cur.fetchone()
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
		if faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Faculty (Faculty_ID,Faculty_Name,Department) VALUES ('%s','%s','%s')",(usn,name,batch,section,department))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given faculty ID already exists
	
	
class Tag(Resource):
	
	#get the list of tags starting from a given set of letters
	@app.route('/suggestion/<partial_name>',methods=['GET'])
	def get_tag_suggestion(self,partial_name):
		cur = mysql.connection.cursor()
		cur.execute("SELECT Tag_name FROM Tags WHERE Tag_Name LIKE "+partial_name)
		response = cur.fetchall()
		cur.close()	
		return jsonify(data=response), status.HTTP_200_OK
	#get the list of tags attempted by a student
	@app.route('/student/<usn>',methods=['GET'])
	def get_tag_student(self,usn):
		if student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Tags,Question_attempt,Question_tag WHERE Question_attempt.Student_ID = "+usn+" AND Question_attempt.Question_ID = Question_tag.Question_ID AND Question_tag.Tag_ID = Tags.Tag_ID")
			response = cur.fetchall()
			cur.close()	
			return jsonify(data=response),status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	
	#get the list of tags attempted by all students under a faculty
	@app.route('/faculty/<f_id>',methods=['GET'])
	def get_tag_faculty(self,f_id):
		if faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Teaches,Tags,Question_attempt,Question_tag WHERE Teaches.Faculty_ID = "+f_id+" AND Question_attempt.Student_ID = Teaches.Student_ID AND Question_attempt.Question_ID = Question_tag.Question_ID AND Question_tag.Tag_ID = Tags.Tag_ID")
			response = cur.fetchall()
			cur.close()	
			return jsonify(data=response),status.HTTP_200_OK
		return status.HTTP_404_NOT_FOUND
	#Post a new tag entry to the database
	@app.route('/add/<tag_name>',methods=['POST'])
	def add_tag(self):
		tag_id = self.retrieve_tag(tag_name)
		details = request.form
		name = details["Name"]
		if not tag_exists(tag_id):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Tags (Tag_name) VALUES ('%s')",(name))
			mysql.connection.commit()
			return status.HTTP_201_CREATED
		return status.HTTP_409_CONFLICT	#Conflict here is that the given tag name already exists
	
	
class Question(Resource):

	# Get the description and tags of the question using post
	@app.route('/description',methods=['POST'])
	def get_description(self):
		details = request.form
		question_id = details["question_ID"]
		usn = details["Student_ID"]
		if is_accessible(question_id,usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Description_Pathway FROM Question WHERE Question_ID="+question_id)
			desc_path = cur.fetchone()[0]
			cur.close()
			desc = ""
			with open(desc_path,"r") as fp:
				desc = fp.read()
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Question_tag,Tags WHERE Question_Tag.Question_ID="+question_id+" AND Question_tag.Tag_ID = Tags.Tag_ID")
			Tag = cur.fetchone()[0]
			cur.close()
			return jsonify(data = [desc,tag]),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Student not allowed to access the question
	
	# Get the description and tags of the question using post for the faculty to view
	@app.route('/faculty_description',methods=['POST'])
	def get_description_faculty(self):
		details = request.form
		question_id = details["question_ID"]
		f_id = details["Faculty_ID"]
		if faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Description_Pathway FROM Question WHERE Question_ID="+question_id)
			desc_path = cur.fetchone()[0]
			cur.close()
			desc = ""
			with open(desc_path,"r") as fp:
				desc = fp.read()
			cur = mysql.connection.cursor()
			cur.execute("SELECT Tags.Tag_name FROM Question_tag,Tags WHERE Question_Tag.Question_ID="+question_id+" AND Question_tag.Tag_ID = Tags.Tag_ID")
			Tag = cur.fetchone()[0]
			cur.close()
			return jsonify(data = [desc,tag]),status.HTTP_200_OK
		return status.HTTP_401_UNAUTHORIZED	#Not a faculty
	
	# Get the test cases for a question
	@app.route('/testcases',methods=['POST'])
	def get_testcases(self):
		details = request.form
		question_id = details["question_ID"]
		usn = details["Student_ID"]
		if is_accessible(usn,question_id):
			if not question_attempted(usn,question_id):
				cur = mysql.connection.cursor()
				cur.execute("INSERT INTO Question_attempt (Student_ID,Question_ID) VALUES ('%s','%s')",(usn,question_id))
				mysql.connection.commit()
				cur.close()
			cur = mysql.connection.cursor()
			cur.execute("SELECT List_testcases_Pathway FROM Question WHERE Question_ID="+question_id)
			test_path = cur.fetchone()[0]
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
		if faculty_exists(f_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT List_testcases_Pathway FROM Question WHERE Question_ID="+question_id)
			test_path = cur.fetchone()[0]
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
		details = request.form
		description = details["description"]
		f_id = details["Faculty_ID"]
		test_cases = details["test_cases"]
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Questions (List_Testcases_Pathway,Description_Pathway,Faculty_ID) VALUES ('%s','%s','%s','%s')",("unassigned","unassigned",f_id))
		cur.connection.commit()
		cur.close()	
		try:
			os.stat("questions")
		except:
			os.mkdir("questions")
		cur = mysql.connection.cursor()
		cur.execute("SELECT Question_ID FROM Questions WHERE Description_Pathway = 'unassigned'")
		q_id = cur.fetchone()[0]
		cur.close()	
		try:
			os.stat("questions/"+q_id)
		except:
			os.mkdir("questions/"+q_id)
		with open("questions/"+q_id+"/description.txt","w") as fp:
			fp.write(description)
		with open("questions/"+q_id+"/testcases.txt","w") as fp:
			fp.write(str(len(test_cases)))
			for test_case in test_cases:
				tc = test_cases.split("\n")
				fp.write(str(len(tc)))
			for test_case in test_cases:
				fp.write(test_case)
		cur = mysql.connection.cursor()
		cur.execute("UPDATE Questions SET List_Testcases_Pathway='%s',Description_Pathway='%s' WHERE Description_Pathway='unassigned'",("questions/"+q_id+"/testcases.txt","questions/"+q_id+"/description.txt"))
		cur.connection.commit()
		cur.close()	
		return status.HTTP_201_CREATED
	
class Exam(Resource):

	#get questions of an exam using post
	@app.route('/questions',methods=['POST'])
	def get_questions(self,exam_id,usn):
		details = request.form
		exam_id = details["Exam_ID"]
		usn = details["Student_ID"]
		if exam_allowed(usn,exam_id):
			cur = mysql.connection.cursor()
			cur.execute("SELECT Question_ID FROM Exam_contents WHERE Exam_ID = "+exam_id)
			response = cur.fetchall()
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
			cur.execute("INSERT INTO Exam_contents (Question_ID,Exam_ID) values ('%s','%s')",(question_id,exam_id))
			response = cur.fetchall()
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
			cur.execute("INSERT INTO Exam_attempt (Student_ID,Exam_ID) values ('%s','%s')",(student_id,exam_id))
			response = cur.fetchall()
			cur.close()	
		return status.HTTP_201_CREATED
		
	
class Submission(Resource):

	#gets the test cases and assigns the submission ID
	@app.route('/receive',methods=['POST'])
	def get_testcase(self,question_id,usn):
		if is_accessible(question_id,usn):
			pass
		pass
	
	#posts the submission results for submission ID
	@app.route('/evaluated',methods=['POST'])
	def post(self,submission_id,usn,submission_res):
		if submission_exsits(submission_id,usn):
			pass
		pass
	
	
class Student_login(Resource):
	
	#Add or update login credentials details using post
	@app.route('/update',methods=['POST'])
	def update(self,username,srn,password):
		if student_credential_exists(username,srn):
			pass
		pass
	
	#Validate login credentials
	@app.route('/validate',methods=['POST'])
	def validate(self,username,password):
		pass
	

class Faculty_login(Resource):

	#Add or update login credentials details using post
	@app.route('/update',methods=['POST'])
	def update(self,username,f_id,password):
		if faculty_credential_exists(usn,f_id):
			pass
		pass
	
	#Validate login credentials
	@app.route('/validate',methods=['POST'])
	def validate(self,usn,password):
		pass
	
class Teaches(Resource):

	#Get details of which subjects are taught by faculty to student
	@app.route('/subject/<usn>/<f_id>',methods=['GET'])
	def get_subjects(self,usn,f_id):
		if student_exists(usn) and Faculty.faculty_exists(f_id):
			pass
		pass
	#Get details of the teachers of a student
	@app.route('/faculties/<usn>',methods=['GET'])
	def get_faculties(self,usn):
		if student_exists(usn):
			pass
		pass
	#Get details of students taught by a teacher
	@app.route('/students/<f_id>',methods=['GET'])
	def get_students(self,f_id):
		if faculty_exists(f_id):
			pass
		pass
	#Post subjects taught by faculty to server
	@app.route('/',methods=['POST'])
	def post(self,usn,f_id,subject):
		if student_exists(usn) and Faculty.faculty_exists(f_id):
			pass
		pass

class Analysis(Resource):
	
	#get the necessary data for student performance
	@app.route('/student/<usn>',methods=['GET'])
	def get_student_perf(self,usn):
		if student_exists(usn):
			pass
		pass
	#get the data for analysing overall performance of students under a faculty
	@app.route('/faculty/<f_id>',methods=['GET'])
	def get_faculty_perf(self,f_id):
		if faculty_exists(f_id):
			pass
		pass
	#get data related to overall performance of a student in an exam
	@app.route('/exam/<exam_id>',methods=['GET'])
	def get_exam_perf(self,exam_id):
		if exam_exists(exam_id):
			pass
		pass
	#get data related to performance of a student in an exam
	@app.route('/student_exam/<usn>/<exam_id>',methods=['GET'])
	def get_student_exam_perf(self,usn,exam_id):
		if exam_allowed(exam_id,usn):
			pass
		pass
	#get data related to overall performance of all students on a particular tag
	@app.route('/tag/<usn>',methods=['GET'])
	def get_tag_perf(self,tag_name):
		tag_id = Tag.retrieve_tag(tag_name)
		if tag_exists(tag_id):
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
		 if tag_attempted(tag_id,usn):
		 	pass
		 pass
	#get data related to tagwise performance of students under a faculty
	@app.route('/faculty_tagwise/<f_id>',methods=['GET'])
	def get_faculty_tags_perf(self,f_id):
		if faculty_exists(f_id):
			pass
		pass
	#get data related to tagwise performance of a student
	@app.route('/student_tagwise/<usn>',methods=['GET'])
	def get_student_tags_perf(self,usn):
		if student_exists(usn):
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
