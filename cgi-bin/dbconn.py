import sqlite3
import os

import threading

from definitions import img_dir
#the file where the database will operate
import MySQLdb

address = 'localhost'
user = 'root'
password = 'password'
collection = 'mydb'

#posts non-op to appear:
posts_non_op = 2

lock_db = threading.Lock()
#lock_id = threading.Lock()
#lock_id_img = threading.Lock()

class DbConn:
	_conn = None
	_cursor = None
	_count = 0
	_count_img = 0

	def __init__(self):
		lock_db.acquire()
		self._conn = MySQLdb.connect(address, user, password, collection)
		self._cursor = self._conn.cursor()
		
		self.execute("SET NAMES utf8;")
		c = self.execute("SELECT MAX(post_id) FROM thread_post_t;")
		if(c == None or c[0][0] == None):
			self._count = 0
		else:
			self._count = c[0][0]

		cimg = self.execute("SELECT MAX(img_id) FROM thread_post_t WHERE img_id!=\"\";")
		if(cimg == None or cimg[0][0] == None):
			self._count_img = 0
		else:
			self._count_img = int(str(cimg[0][0]).split('.')[0])

	def __del__(self):
		self.commit()
		self._conn.close()
		lock_db.release()

	def commit(self):
		try:
			self._conn.commit()
		except sqlite3.OperationalError, e:
			self.db.rollback()
			print "!!! Error: %s !!!" % (e)		

	def execute(self, query):
		try:
			self._cursor.execute(query)
			return self._cursor.fetchall()
		except sqlite3.OperationalError, e:
			self._conn.rollback()
			print "!!! Error: %s !!!" % (e)

	def create_tables(self):
		self.execute("CREATE TABLE thread_post_t (thread_id INT, post_id INT UNIQUE, user_id VARCHAR(8), e_mail VARCHAR(32), pass_delete VARCHAR(16), img_id VARCHAR(16), img_name VARCHAR(33), sha1 VARCHAR(41), img_thumb_X INT, img_thumb_Y INT, img_size INT, img_dim VARCHAR(16), content VARCHAR(512), date TIMESTAMP, user VARCHAR(16));")
	
		self.execute("CREATE TABLE threadbump_t (thread_id INT UNIQUE, date TIMESTAMP, replies INT, replies_img INT);")

	def recreate(self):
		self.drop_tables()
		self.create_tables()

	def id(self):
		self._count = self._count + 1
		return self._count
	
	def id_img(self):
		self._count_img = self._count_img +1
		return self._count_img

	def drop_tables(self):
		imgs = self.execute('''SELECT img_id FROM thread_post_t WHERE img_id!=\"\";''')
		for i in imgs:
			os.system("rm -f %s%s; rm -f %sthumb_%s" % (img_dir, i[0], img_dir, i[0]))
		self.execute('''DROP TABLE thread_post_t;''')
		self.execute('''DROP TABLE threadbump_t;''')

	def list_threads(self):
		return self.execute("SELECT * FROM threadbump_t ORDER BY date DESC;")
	
	def get_post_op(self, thread):
		return self.execute("SELECT * FROM thread_post_t WHERE post_id=%s ORDER BY date;" % thread)[0]
	
	def get_posts_thread(self, thread):
		a = self.execute("SELECT replies FROM threadbump_t WHERE thread_id=%s;" % thread)[0][0]
		if a > posts_non_op:
			a = posts_non_op
		r = self.execute("SELECT * FROM thread_post_t WHERE thread_id=%s ORDER BY date;" % thread)[-a:]
		if (r[0][1] == thread):
			return r[1:]
		else:
			return r
		

	def list_posts(self, thread_id):
		return self.execute("SELECT * FROM thread_post_t WHERE thread_id=" + str(thread_id) + " ORDER BY date;")

	def post(self, thread_id, post_id, content, user_id="", e_mail="", pass_delete="", img_id="", img_name="", sha1="", img_thumb_X=0, img_thumb_Y=0, img_size=0, img_dim="", usr_ip=""):
		if thread_id == 0:
			thread_id = post_id
			self.execute("INSERT INTO threadbump_t VALUES (%s, CURRENT_TIMESTAMP, 0, 0);" % (thread_id))
		else:
			qntd = self.execute("SELECT COUNT(*) FROM thread_post_t WHERE thread_id=%s;" % (thread_id))
			self.execute("UPDATE threadbump_t SET replies=%s WHERE thread_id=%s;" % (int(qntd[0][0]), thread_id))
			if(img_id is not ""):
				qntd = self.execute("SELECT replies_img FROM threadbump_t WHERE thread_id=%s;" % (thread_id))
				self.execute("UPDATE threadbump_t SET replies_img=%s WHERE thread_id=%s;" % (int(qntd[0][0])+1, thread_id))
			if(user_id != "Heaven"):
				self.execute("UPDATE threadbump_t SET date=CURRENT_TIMESTAMP WHERE thread_id=%s;" % (thread_id))
		return self.execute("INSERT INTO thread_post_t VALUES (%s, %s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", %s, %s, %s, \"%s\", \"%s\", CURRENT_TIMESTAMP, \"%s\");" % (thread_id, post_id, user_id, e_mail, pass_delete, img_id, img_name, sha1, img_thumb_X, img_thumb_Y, img_size, img_dim, content, usr_ip))


if __name__ == "__main__":
	db = DbConn()
	db.create_tables()
