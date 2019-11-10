DROP DATABASE Coding_Platform;
CREATE DATABASE Coding_Platform;
USE Coding_Platform;

-- DROP TABLE Submissions CASCADE;
-- DROP TABLE Questions_attempt CASCADE;
-- DROP TABLE Exam_attempt CASCADE;
-- DROP TABLE Exam_contents CASCADE;
-- DROP TABLE Question_tag CASCADE;
-- DROP TABLE Questions CASCADE;
-- DROP TABLE Exam CASCADE;
-- DROP TABLE Tags CASCADE;
-- DROP TABLE Teaches CASCADE;
-- DROP TABLE Faculty_email CASCADE;
-- DROP TABLE Student_email CASCADE;
-- DROP TABLE Faculty_login CASCADE;
-- DROP TABLE Student_login CASCADE;
-- DROP TABLE Faculty CASCADE;
-- DROP TABLE Student CASCADE;



/*Note - This code was tested on postgresql 9.5.19 and may or may not be compatible with other SQL servers such as mySQL or few lower versions of postgreSQL. In such cases, try the following replacements -

1. Replace every occurence of the word 'SERIAL' with 'INT AUTO_INCREMENT'
				(and/or)
2. Add the phrase 'FOREIGN KEY' before every occurence of the word 'REFERENCES'
*/




CREATE TABLE Student(
Student_ID VARCHAR(14) PRIMARY KEY,  /*It is a must for admin to fill the student USN for each entry*/
Student_Name VARCHAR(30),
Section VARCHAR(2),
Batch NUMERIC(4),
Department VARCHAR(40)
);

/*student - ID(pk), name, section, batch, department*/

CREATE TABLE Faculty(
Faculty_ID VARCHAR(15) PRIMARY KEY,
Faculty_Name VARCHAR(25) NOT NULL,
Department VARCHAR(30)
);

/*faculty - ID(pk), name department*/


CREATE TABLE Student_login(
Student_password VARCHAR (20),
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE,
PRIMARY KEY(Student_ID)
);

/*student login - username (unique), password, student ID (fk - student,pk)*/



CREATE TABLE Faculty_login(
Faculty_password VARCHAR (20),
Faculty_ID VARCHAR(14) REFERENCES Faculty(Faculty_ID)  ON DELETE CASCADE,
PRIMARY KEY(Faculty_ID)
);

/*faculty login - username (unique), password, faculty ID (fk -faculty)*/


CREATE TABLE Student_email(
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE,
Email_ID VARCHAR(30) UNIQUE NOT NULL,
PRIMARY KEY(Student_ID,Email_ID)
);

/*student email - (student ID(fk - student), email) (pk)*/



CREATE TABLE Faculty_email(
Faculty_ID VARCHAR(14) REFERENCES Faculty(Faculty_ID)  ON DELETE CASCADE,
Email_ID VARCHAR(30) UNIQUE NOT NULL,
PRIMARY KEY(Faculty_ID,Email_ID)
);

/*faculty email - (faculty ID(fk - faculty), email) (pk)*/



CREATE TABLE Teaches (
Subject VARCHAR(20),
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE,
Faculty_ID VARCHAR(14) REFERENCES Faculty(Faculty_ID)  ON DELETE CASCADE,
PRIMARY KEY(Student_ID,Faculty_ID,Subject)
);

/*teaches - (subject, student ID(fk - student), faculty ID(fk - faculty)) (pk)*/


CREATE TABLE Exam(
Exam_ID SERIAL PRIMARY KEY,	
Title VARCHAR(30),
Faculty_ID VARCHAR(14) REFERENCES Faculty(Faculty_ID) ON DELETE CASCADE 
);

/*exam - ID(pk), title, faculty ID (fk - faculty)(not NULL)*/



CREATE TABLE Questions(
Question_name VARCHAR(50),
Question_ID SERIAL PRIMARY KEY,
List_Testcases_Pathway VARCHAR (40),		/*Pathway to a text file containing the list of test cases for a given problem*/
Description_Pathway VARCHAR(40),		/*Pathway to the file containing the question/problem statement*/
Number_Testcases INT,
Faculty_ID VARCHAR(15) REFERENCES Faculty (Faculty_ID) ON DELETE CASCADE
);

/*questions - ID(pk), list of test cases (pathway), tag, description (pathway), faculty (fk - faculty)*/


CREATE TABLE Question_tag(
Question_ID INT REFERENCES Questions(Question_ID) ON DELETE CASCADE,  
Tag_name VARCHAR(30),
PRIMARY KEY(Question_ID,Tag_name)
);

/*question tag - (question ID(fk - question), tag ID(fk - tag))(pk)*/

CREATE TABLE Exam_contents (
Exam_ID INT REFERENCES Exam(Exam_ID) ON DELETE CASCADE,
Question_ID INT REFERENCES Questions(Question_ID) ON DELETE CASCADE,
PRIMARY KEY(Exam_ID,Question_ID)
);

/*exam contents - (exam ID(fk - exam), question ID(fk - question))*/


CREATE TABLE Exam_attempt(
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE, 
Exam_ID INT REFERENCES Exam(Exam_ID) ON DELETE CASCADE,
PRIMARY KEY(Student_ID,Exam_ID)
);

/*exam attempt - (student ID(fk - student), exam ID (fk - exam)) (pk)*/




CREATE TABLE Question_attempt(
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE,
Question_ID INT REFERENCES Questions(Question_ID) ON DELETE CASCADE,
PRIMARY KEY(Student_ID,Question_ID)
);

/*question attempt - (student ID(fk - student), question ID (fk - question)) (pk)*/


CREATE TABLE Submissions(
Code_Pathway VARCHAR(40),	/*Pathway to the submission code*/
Submission_ID SERIAL,
Student_ID VARCHAR(14) REFERENCES Student(Student_ID) ON DELETE CASCADE,
Question_ID INT REFERENCES Questions(Question_ID) ON DELETE CASCADE,
PRIMARY KEY(Submission_ID,Student_ID,Question_ID)
);

/*submissions - code (pathway), (submission ID, student ID (fk - student), question ID (fk - question)) (pk)*/

