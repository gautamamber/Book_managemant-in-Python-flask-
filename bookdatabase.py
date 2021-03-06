import sqlite3
con = sqlite3.connect('book.db')
con.execute('CREATE TABLE operator_bookdata(bookid INTEGER PRIMARY KEY NOT NULL UNIQUE, authorid INTEGER, authorname TEXT, book TEXT, mrp REAL, previous_bal REAL, copyprinted INTEGER, total_copy INTEGER, specimen INTEGER, copy_sold INTEGER, balancestock INTEGER, royalty_rate REAL, royalty_amount REAL,  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(authorid) REFERENCES author(authorid))')
con.execute('CREATE TABLE users(userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, name TEXT, password TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
#con.execute('CREATE TABLE myauthor(id INTEGER PRIMARY KEY AUTOINCREMENT, username INTEGER, password TEXT)')
con.execute('CREATE TABLE author(key_authorid INTEGER PRIMARY KEY AUTOINCREMENT, authorid TEXT, password TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
con.close()
