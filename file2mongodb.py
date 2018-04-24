import face_recognition
from pymongo import MongoClient
import numpy as np
import pickle
DATABASE_SERVER='127.0.0.1'  #port 
DATABASE_PORT=27017
def RegisterNewUser(UserName,Department,UserPicture,conn):
	known_image = face_recognition.load_image_file(UserPicture)
	face_encoding = face_recognition.face_encodings(known_image)[0]
	#print(obama_face_encoding)
	db = conn.mydb  
	my_set = db['user']
	my_set.insert_one({'UserName':UserName  ,'Department':Department  ,'picture_binary' \
	: pickle.dumps(face_encoding)})


if __name__ == "__main__":
	#RegisterNewUser('test','testdepartment','obama.jpg')
	#data= pandas.read_csv('E:\\project\\face\\github\\t.csv') 
	conn = MongoClient(DATABASE_SERVER, DATABASE_PORT)
	f=open("t.csv","r")
	#f.readline()
	lines=f.readlines()     
	for line in lines:
		tmp=line.strip('\n\r').split(',')
		RegisterNewUser(tmp[0],tmp[1],tmp[2],conn)

	
