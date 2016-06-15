import sqlite3
conn = sqlite3.connect('invest.db')

db = conn.cursor()

db.execute('''
	CREATE TABLE user (
	user_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	fname TEXT,
	lname TEXT,
	email TEXT,
	pwd TEXT
	)
	''')

def create_(fname, lname, email, pwd):
	db.execute('''
		INSERT INTO user(fname, lname, email, pwd) VALUES(?, ?, ?, ?)
		''', (fname, lname, email, pwd))
	conn.commit()

#create_('Jamaine', 'Roseborough', 'jroseborough01@gmail.com', 'jrcss1103')

