from flask import *
import sqlite3, hashlib, os
from functools import wraps
import logging
from flask_login import current_user
from logging.handlers import RotatingFileHandler
from passlib.hash import sha256_crypt
from datetime import datetime
app = Flask(__name__)


#check is login decorator



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            
            return redirect(url_for('oplogin'))

    return wrap
def alogin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            
            return redirect(url_for('login'))

    return wrap



@app.route('/')
def main():
	return render_template("main.html")





@app.route('/operatorlogin', methods = ['GET', 'POST'])
def oplogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			result = cur.execute('SELECT username,password FROM users')
			if result > 0:
				data = cur.fetchall()
				for each in data:

					if each[0] == username and each[1] ==  hashlib.md5(password.encode()).hexdigest():
						a = session['username'] = username
						session['logged_in'] = True
						print(type(app.logger.info(a)))
						return redirect(url_for("index"))
			else:
				return render_template("operatorlogin.html")
			

	return render_template('operatorlogin.html')

# Check if user logged in






@app.route('/operatoreg', methods = ['POST', 'GET'])
def op_reg():
	if request.method == 'POST':
		username = request.form['username']
		name = request.form['name']
		password = request.form['password']
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			cur.execute('INSERT INTO users(username,name, password) VALUES (?,?,?)',(username,name,hashlib.md5(password.encode()).hexdigest()))
			con.commit()
		con.close()
		return render_template("operatorlogin.html")
	return render_template("opreg.html")



#Operator login redirect on operator  common dashborad

@app.route('/operator')
@login_required
def index():
	con = sqlite3.connect("book.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT operator_bookdata.bookid, operator_bookdata.authorid, operator_bookdata.authorname, operator_bookdata.book, operator_bookdata.mrp, operator_bookdata.previous_bal, operator_bookdata.copyprinted, operator_bookdata.total_copy, operator_bookdata.specimen, operator_bookdata.copy_sold, operator_bookdata.balancestock, operator_bookdata.royalty_rate, operator_bookdata.royalty_amount FROM operator_bookdata")
	rows = cur.fetchall()
	if rows > 0:

		return render_template("index.html", rows = rows)
	else: 
		msg = "nothing"
		return render_template('index.html', msg = msg)
	cur.close()




@app.route('/new', methods = ['POST','GET'])
@login_required
def new():
	if request.method == 'POST':
		bid = request.form['bid']
		aid = request.form['aid']
		aname = request.form['aname']
		bname = request.form['bname']
		mrp = request.form['mrp']
		pbalance = request.form['pbalance']
		cprinted = request.form['cprinted']
		tcopies = request.form['tcopies']
		sissued = request.form['sissued']
		csold = request.form['csold']
		bstock = request.form['bstock']
		rrate = request.form['rrate']
		ramount = request.form['ramount']
		
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			cur.execute('INSERT INTO operator_bookdata (bookid, authorid, authorname, book, mrp, previous_bal, copyprinted, total_copy, specimen, copy_sold, balancestock, royalty_rate, royalty_amount) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)' , (bid, aid, aname, bname, mrp, pbalance, cprinted, tcopies ,sissued, csold, bstock, rrate, ramount))
			con.commit()
			return redirect((url_for('index')))
	return render_template("new.html")


#Update existing account of author


@app.route('/update', methods = ['POST' , 'GET'])
@login_required
def update():
	if request.method == 'POST':
		bid = request.form['bid']
		aid = request.form['aid']
		aname = request.form['aname']
		bname = request.form['bname']
		mrp = request.form['mrp']
		pbalance = request.form['pbalance']
		cprinted = request.form['cprinted']
		tcopies = request.form['tcopies']
		sissued = request.form['sissued']
		csold = request.form['csold']
		bstock = request.form['bstock']
		rrate = request.form['rrate']
		ramount = request.form['ramount']
		
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			cur.execute('UPDATE operator_bookdata SET key_auhtorid = ? , authorname = ? , book = ? , mrp = ?, previous_bal = ?, copyprinted = ?, total_copy = ?, specimen = ?, copy_sold = ? , balancestock = ?, royalty_rate = ?, royalty_amount = ? WHERE bookid = ?', (aid, aname, bname, mrp, pbalance, cprinted, tcopies ,sissued, csold, bstock, rrate, ramount,bid))
			
			con.commit()
			return redirect(url_for('index'))

	return render_template('update.html')



@app.route('/authordashboard')
@alogin_required
def get_data():
	con = sqlite3.connect("book.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT operator_bookdata.authorid, operator_bookdata.authorname, operator_bookdata.book, operator_bookdata.mrp, operator_bookdata.previous_bal, operator_bookdata.copyprinted, operator_bookdata.total_copy, operator_bookdata.specimen, operator_bookdata.copy_sold, operator_bookdata.balancestock, operator_bookdata.royalty_rate, operator_bookdata.royalty_amount FROM operator_bookdata WHERE  authorid   = "+ str(session['authorid']) )
	rows = cur.fetchall()
	if rows > 0:
		return render_template("author.html", rows = rows)
	else: 
		msg = "nothing"
		return render_template('index.html', msg = msg)
	cur.close()



@app.route("/logout")
@login_required
def ologout():
    session.clear()
    return redirect(url_for('oplogin'))

@app.route("/authorlogout")
@alogin_required
def alogout():
    session.clear()    
    return redirect(url_for('login'))




#Author registration

@app.route('/authorreg' , methods = ['POST','GET'])
@alogin_required
def register():
	if request.method == 'POST':
		authorid = request.form['authorid']
		password = request.form['password']
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			cur.execute('INSERT INTO author (authorid,password) VALUES (?,?)', (authorid,hashlib.md5(password.encode()).hexdigest()))
			con.commit()
		con.close()
		return redirect(url_for('login'))

	return render_template('authorregistration.html')




#NEW AUTHR =============================


@app.route('/authorlogin', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		authorid = request.form['authorid']
		password = request.form['password']
		with sqlite3.connect('book.db') as con:
			cur = con.cursor()
			result = cur.execute('SELECT key_authorid,authorid,password FROM author')
			if result > 0:
				data = cur.fetchall()
				for each in data:

					if each[1] == authorid and each[2] == hashlib.md5(password.encode()).hexdigest():
						session['logged_in'] = True
						a = session['authorid'] = authorid

						print(type(app.logger.info(a)))
						return redirect(url_for("get_data"))
			else:
				return render_template("authorloginlogin.html")
			

	return render_template('authorlogin.html')





# Check if user logged i






if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
