import MySQLdb

class UsersDB:
	host = 'localhost'
	user = 'root'
	password = '123'
	db = 'Users'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.cursor = self.connection.cursor()

		try:
			self.cursor.execute("""
				CREATE TABLE PERSON (
				USER_ID INT,
				NAME CHAR(20) NOT NULL,
				AUTHORIZATION CHAR(1),
				IMAGE_PATH CHAR(20) )
				""")
			self.connection.commit()
		except:
			self.connection.rollback()


	def insert(self, query):
		try:
			self.cursor.execute(query)
			self.connection.commit()
		except:
			self.connection.rollback()

	def query(self, query):
		cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	def __del__(self):
		self.connection.close()

	sql = """CREATE TABLE PERSON (
			USER_ID INT,
			NAME CHAR(20) NOT NULL,
			AUTHORIZATION CHAR(1),
			IMAGE_PATH CHAR(20) )"""
	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

	sql = "INSERT INTO PERSON VALUES (%"
	db.close()