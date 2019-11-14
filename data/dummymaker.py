print("#!/bin/bash\n\n")
import random

questions = ["sort", "search", "factorial"]
n_testcases = [4, 12, 30]
lang = ["python", "c", "cpp"]

n_students = 50
n_faculty = 5
n_submissions_q = 30

tags = ["data-structures", "algorithms", "dp", "graph", "number-theory", "easy", "hard", "ml", "greedy"]
batches = ["2016", "2017"]
sections = ["A", "B", "C"]

#making students
for a in range(n_students):
	print(f'curl -X POST -d "Usn=s{a+1}&Name=sname{a+1}&Batch={random.choice(batches)}&Section={random.choice(sections)}&Department=CSE&Password=password" http://127.0.0.1:5000/codecouch/login/')

#making teachers
for a in range(n_faculty):
	print(f'curl -X PUT -d "Name=fname{a+1}&Department=CSE" http://127.0.0.1:5000/codecouch/faculty/f{a+1}')

#making questions
for a in range(len(questions)):
	thetags = " ".join(random.sample(tags, 2))
	files = " ".join([f"-F 'op{x+1}=@./{questions[a]}/op{x+1}' -F 'ip{x+1}=@./{questions[a]}/ip{x+1}'" for x in range(n_testcases[a])])
	print(f"""curl  -X POST -F 'Usn=f{random.randint(1, n_faculty)}' -F 'Question_name={questions[a]}' -F 'Tags={thetags}' -F 'description=@./{questions[a]}/description' {files} http://127.0.0.1:5000/codecouch/question/	""")

#making submissions
for b in range(len(questions)):
	studs = random.sample(range(1, n_students), n_submissions_q)

	for stud in studs:
		splitting = random.randint(0, n_testcases[b])
		l = [str(random.randint(-3, 0)) for _ in range(splitting)] + ["0" for _ in range(n_testcases[b]-splitting)]
		random.shuffle(l)
		a = "_".join(l)
		print(f"curl -X POST -F 'language={random.choice(lang)}' -F 'status={a}' -F 'code=@code' http://127.0.0.1:5000/codecouch/submission/{b+1}/s{stud}")