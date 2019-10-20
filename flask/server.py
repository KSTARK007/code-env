from helper_functions import *
import os

class Login(Resource):
	
	#Add or update login credentials details using post
	def get(self):
		if student_credential_exists():
			pass
		pass
	
	#Validate login credentials
	def post(self):
		pass

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

api.add_resource(Student, "/codecouch/student/<usn>")
api.add_resource(Faculty, "/codecouch/faculty/<f_id>")

if __name__=="__main__":
	app.run(debug=True)