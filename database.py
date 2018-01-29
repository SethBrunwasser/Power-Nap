
import sqlite3
import sys

class UsersDB:

	def __init__(self):
		self.connection = sqlite3.connect('users.db')
		self.cursor = self.connection.cursor()

		self.cursor.execute("DROP TABLE IF EXISTS PERSON")
		self.cursor.execute("""
			CREATE TABLE PERSON(
			USER_ID INTEGER PRIMARY KEY autoincrement,
			NAME TEXT NOT NULL,
			AUTHORIZATION TEXT,
			IMAGE_PATH TEXT
			);""")
		self.connection.commit()

	def new_user(self, name, authorization, path):
	
		self.cursor.execute("INSERT INTO PERSON (NAME, AUTHORIZATION, IMAGE_PATH) VALUES (?, ?, ?)", 
			(name, authorization, path))
	
	def query(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def query_all(self):
		data = self.cursor.execute("SELECT * FROM PERSON;")
		for row in data:
			print(row)
		return self.cursor.fetchall()

#	def __del__(self):
#		self.connection.close()
