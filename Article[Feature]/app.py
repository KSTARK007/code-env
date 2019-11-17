from flask import *
import json  
  
app = Flask(__name__) 
  
@app.route('/getfile/<search>') 
def get_file(search):
	f = open("./data.json")
	x = f.read()
	f.close()
	d = dict()
	data = json.loads(x)
	for i in range(len(data)):
		if(str(search).lower() in str(data[str(i)]["title"]).lower()):
			d[str(i)] = data[str(i)]
			print(data[str(i)]["title"])
	if(len(d)==0):
		return jsonify({"error":"no entry in the database"})
	# output = json.dumps(d)
	return jsonify(d)


@app.route('/postfile/<datas>') 
def post_file(datas):
	result = request.form
	f = open("./data.json",)
	x = f.read()
	f.close()
	data = json.loads(x)
	t = datas.split(";")
	temp = {}
	temp["title"] = str(t[0])
	temp["data"] = str(t[1])
	temp["code"] = str(t[2])
	temp["link"] = str(t[3])
	data[str(len(data))] = temp
	out = json.dumps(data)
	fi = open("./data.json","w")
	fi.write(out)
	return ""
  
# main driver function 
if __name__ == '__main__': 
  
    app.run() 
