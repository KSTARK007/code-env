from helper_functions import *
import os

# TODO:
# submission

class Login(Resource):
	
	#Checking log in credentials
	"""
	-2: password incorrect
	-1: username does not exist
	0: student
	1: faculty
	"""
	def get(self):
		details = request.args
		usn = details["Usn"]
		password = details["Password"]
		user_type = get_user_type(usn)

		if user_type==None:
			response = jsonify([-1])
			response.status_code = 400
			return response

		valid = credential_exists(usn, password, user_type)
		if valid==1:
			response = jsonify([int(user_type=="Faculty")])
			response.status_code = 200
		else:
			response = jsonify([-2])
			response.status_code = 400
		return response

	
	#Validate sign up credentials
	"""
	-1: user exists
	0: succesfully signed up
	"""
	def post(self):
		details = request.form
		usn = details["Usn"]
		print(get_user_type(usn))
		if get_user_type(usn)==None:
			password = details["Password"]
			name = details["Name"]
			section = details["Section"]
			batch = details["Batch"]
			department = details["Department"]

			cur = mysql.connection.cursor()
			result = cur.execute(f"INSERT INTO Student(Student_ID, Student_Name, Batch, Department, Section) VALUES ('{usn}', '{name}', {batch}, '{department}', '{section}')")
			result = cur.execute(f"INSERT INTO Student_login(Student_ID, Student_password) VALUES ('{usn}', '{password}')")
			mysql.connection.commit()
			cur.close()
			response = jsonify([0])
			response.status_code = 200

		else:
			response = jsonify([-1])
			response.status_code = 400

		return response


class Student(Resource):
	# Get relevant details of a student
	def get(self, usn):
		print("Getting Student Details "+usn)

		response = jsonify({})
		response.status_code = 400

		if user_exists(usn, "Student"):
			cur = mysql.connection.cursor()
			cur.execute(f"SELECT * FROM Student WHERE Student_ID='{usn}'")
			result = cur.fetchone()
			cur.close()

			data = {"Name":result[1], "Section":result[2], "Batch":str(result[3]), "Department":result[4]}

			response = jsonify(data)
			response.status_code = 200

		return response
	
	# Post the student usn and relevant details to the server
	def put(self, usn):
		print("Adding new student", usn)

		response = jsonify({})
		response.status_code = 400

		if not user_exists(usn, "Student"):
			details = request.form
			name = details["Name"]
			section = details["Section"]
			batch = details["Batch"]
			department = details["Department"]
			
			cur = mysql.connection.cursor()
			result = cur.execute(f"INSERT INTO Student(Student_ID, Student_Name, Batch, Department, Section) VALUES ('{usn}', '{name}', {batch}, '{department}', '{section}')")
			mysql.connection.commit()
			cur.close()

			response.status_code = 200

		return response


class Faculty(Resource):
	# Get relevant details of a faculty member
	def get(self, f_id):
		print("Getting Faculty Details "+f_id)

		response = jsonify({})
		response.status_code = 400

		if user_exists(f_id, "Faculty"):
			cur = mysql.connection.cursor()
			cur.execute(f"SELECT * FROM Faculty WHERE Faculty_ID='{f_id}'")
			result = cur.fetchone()
			cur.close()

			data = {"Name":result[1], "Department":result[2]}

			response = jsonify(data)
			response.status_code = 200

		return response

	# Post the faculty id and relevant details to the server
	def put(self, f_id):
		print("Adding new faculty", f_id)

		response = jsonify({})
		response.status_code = 400

		if not user_exists(f_id, "Faculty"):
			details = request.form
			name = details["Name"]
			department = details["Department"]
			
			cur = mysql.connection.cursor()
			result = cur.execute(f"INSERT INTO Faculty(Faculty_ID, Faculty_Name, Department) VALUES ('{f_id}', '{name}', '{department}')")
			mysql.connection.commit()
			cur.close()

			response.status_code = 200

		return response


class Question(Resource):
	# Gets the description of the question
	"""
	-1: user does not exist
	-2: question does not exist
	"""
	def get(self):
		details = request.args
		q_id = details["Q_id"]
		usn = details["Usn"]

		user_type = get_user_type(usn)

		if user_type==None:
			response = jsonify([-1])
			response.status_code = 400
			return response

		cur = mysql.connection.cursor()
		cur.execute(f"SELECT Description_Pathway, Number_Testcases, Question_name FROM Questions WHERE Question_ID={q_id}")
		result = cur.fetchone()
		cur.close()

		if result==None:
			response = jsonify([-2])
			response.status_code = 400
			return response	

		response = {}
		response["number_testcases"] = result[1]
		response["name"] = result[2]
		with open(result[0], "r") as file:
			response["description"] = file.read()

		response = jsonify(response)
		response.status_code = 200

		return response

	def post(self):
		files = request.files
		details = request.form

		file_names = list(files.keys())

		print(details)
		
		f_id = details["Usn"]
		name = details["Question_name"]
		tags = details["Tags"].split(" ")
		ip = [name for name in file_names if name[:2]=='ip']
		op = [name for name in file_names if name[:2]=='op']
		ip.sort()
		op.sort()

		if get_user_type(f_id)!="Faculty":
			response = jsonify([-1])
			response.status_code = 400
			return response

		cur = mysql.connection.cursor()
		cur.execute(f"INSERT INTO Questions (List_Testcases_Pathway, Description_Pathway, Faculty_ID, Question_name) VALUES ('unassigned','unassigned','unassigned', '{name}')")
		cur.connection.commit()
		cur.execute(f"SELECT Question_ID FROM Questions WHERE Description_Pathway = 'unassigned' AND Question_name='{name}'")
		q_id = cur.fetchone()[0]
		cur.close()

		file_path = "./Questions/"+str(q_id)+"/"
		try:
			os.stat(file_path)
		except:
			os.mkdir(file_path)

		files["description"].save(file_path+"description.txt")

		for ind in range(len(ip)):
			files[ip[ind]].save(file_path+"ip"+str(ind+1)+".txt")
			files[op[ind]].save(file_path+"op"+str(ind+1)+".txt")

		cur = mysql.connection.cursor()
		cur.execute(f"UPDATE Questions SET Number_Testcases={len(ip)}, List_Testcases_Pathway='{file_path}',Description_Pathway='{file_path+'description.txt'}', Faculty_ID='{f_id}' WHERE Question_ID={q_id}")
		cur.connection.commit()
		for tag in tags:
			cur.execute(f"INSERT INTO Question_tag VALUES({q_id}, '{tag}')")
		cur.connection.commit()	
		cur.close()

		response = jsonify([0])
		response.status_code = 200
		return response


class Questions(Resource):
	"""
	send last=-1 to get the first 10
	"""
	def get(self):
		details = request.args

		last = int(details["Last"])
		number = int(details["Number"])
		tag = details["Tag"]
		faculty = details["Faculty"]

		questions = []

		cur = mysql.connection.cursor()
		tag_cur = mysql.connection.cursor()
		query = f"SELECT * FROM Questions WHERE Question_ID>{number}" 
		if faculty!="":
			query = query+f" AND Questions.Faculty_ID='{faculty}'"
		if tag!="":
			query = query+f" AND Questions.Question_ID IN (SELECT Question_ID from Question_tag WHERE Tag_name='{tag}')"
		query = query+f" ORDER BY Question_ID DESC LIMIT {number}"
		print(query)
		cur.execute(query)
		row_count = cur.rowcount
		for row_ind in range(row_count):
			result = cur.fetchone()
			tag_cur.execute(f"SELECT Tag_name from Question_tag WHERE Question_ID={result[1]}")
			tags = []
			for ind in range(tag_cur.rowcount):
				tags.append(str(tag_cur.fetchone()[0]))
			print(tags)
			questions.append(
				{ "name":result[0], "id":result[1], "number": result[4], "faculty": result[5], "tags": " ".join(tags) }
				)
		tag_cur.connection.commit()
		cur.close()

		response = jsonify(questions)
		response.status_code = 200

		return response

class Testcase(Resource):
	"""
	-1: question id incorrect
	-2: testcase number does not exist
	"""
	def get(self, q_id, file_type, t_num):
		cur = mysql.connection.cursor()
		cur.execute(f"SELECT * FROM Questions WHERE Question_ID={q_id}")
		result = cur.fetchone()
		if result==None or file_type not in ['op', 'ip']:
			response = jsonify([-1])
			response.status_code = 400
			return response
		if result[4]<int(t_num):
			response = jsonify([-2])
			response.status_code = 400
			return response
		return send_file(f"./Questions/{q_id}/{file_type}{t_num}.txt")

class Submission(Resource):
	"""

	"""
	def get(self):
		pass



api.add_resource(Student, "/codecouch/student/<usn>")
api.add_resource(Faculty, "/codecouch/faculty/<f_id>")
api.add_resource(Login, "/codecouch/login/")
api.add_resource(Question, "/codecouch/question/")
api.add_resource(Questions, "/codecouch/questions/")
api.add_resource(Testcase, "/codecouch/testcases/<q_id>/<file_type>/<t_num>")



if __name__=="__main__":
	app.run(debug=True)