#!/usr/bin/env python
# -*- coding:utf-8 -*-
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
	db = conn.mydb  #连接mydb数据库，没有则自动创建
	my_set = db['user']
	my_set.insert_one({'UserName':UserName,'Department':Department,'picture_binary' \
	: pickle.dumps(face_encoding)})
def FindUser(UserPicture,conn,cutoff):
	known_image = face_recognition.load_image_file(UserPicture)
	face_encoding = face_recognition.face_encodings(known_image)[0]
	db = conn.mydb  #连接mydb数据库，没有则自动创建
	my_set = db['user']
	tmp=100
	for i in my_set.find():
		keys = i.keys()
		if "picture_binary" not in keys:
			continue
		face_encoding_database=pickle.loads(i["picture_binary"])
		dist = np.linalg.norm(face_encoding - face_encoding_database)  
		if dist<tmp:
			tmp=dist
			username=i["UserName"]
			department=i["Department"]

	return username,department



if __name__ == "__main__":
	conn = MongoClient(DATABASE_SERVER, DATABASE_PORT)
	#RegisterNewUser('test','testdepartment','obama.jpg')
	username,department=FindUser('obama.jpg',conn,0.6)
	print(username)
	print(department)
	