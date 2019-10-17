from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

class Question(Resource):

	# Get the details of a question and related test cases
	def get(self, question_id):
		pass

	# Post the details of a question and related test cases
	def post(self, question_id):
		pass

api.add_resource(Question, "/question")

if __name__=="main":
	app.run(debug=True)