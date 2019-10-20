from helper_functions import *
import os

class Student(Resource):
	# Get relevant details of a student
	def get(self, usn):
		print("Getting Student Details "+usn)
		response = jsonify({})
		response.status_code = 400
		if student_exists(usn):
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM Student WHERE Student_ID="+usn)
			result = cur.fetchone()
			cur.close()

			data = {"Name":result[1], "Section":result[2], "Batch":str(result[3]), "Department":result[4]}
			print(data)

			response = jsonify(data)
			response.status_code = 200

		return response
	
	# Post the student usn and relevant details to the server
	def put(self, usn):
		print("Adding new student")

		response = jsonify({})
		response.status_code = 400

		if not student_exists(usn):
			details = request.form
			name = details["Name"]
			section = details["Section"]
			batch = details["Batch"]
			department = details["Department"]
			cur = mysql.connection.cursor()
			print(f"INSERT INTO Student(Student_ID, Student_Name, Batch, Department, Section) VALUES ('{usn}', '{name}', {batch}, '{department}', '{section}')")
			result = cur.execute(f"INSERT INTO Student(Student_ID, Student_Name, Batch, Department, Section) VALUES ('{usn}', '{name}', {batch}, '{department}', '{section}')")
			mysql.connection.commit()
			cur.close()

			response.status_code = 200

		return response	#Conflict here is that the given USN already exists

api.add_resource(Student, "/codecouch/student/<usn>")

if __name__=="__main__":
	app.run(debug=True)