from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as flask_session
import model
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


# @app.before_request
# def check_login():
# 	user_data = flask_session.get('user')
# 	if user_data and len(user_data) > 1:
# 		g.user_id = user_data[0]
# 		g.user_email = user_data[1]

@app.route('/')
def home_page(): 
	return render_template("login.html")		

@app.route('/test1', methods=['POST'])
def login_p(): 
	username = request.form['username']
	password = request.form['password']
	user = model.db_session.query(model.Parent).filter_by(username=username).filter_by(password=password).first()
	if user: 
		flask_session['user'] = user.id
		flash("Login successful")
		return redirect(url_for('search_page'))
	else: 
		flash("Username/password is invalid")
		return redirect(url_for('home_page'))

@app.route('/test2', methods=['POST'])
def login_d(): 
	username = request.form['username']
	password = request.form['password']
	user_obj = model.db_session.query(model.Daycare).filter_by(username=username).filter_by(password=password).first()
	if user_obj: 
		flask_session['user'] = user_obj.id
		flash("Login successful")
		return redirect(url_for('search_page'))
	else: 
		flash("Username/password is invalid")
		return redirect(url_for('home_page'))


@app.route('/new_parent', methods=['POST'])
def new_parent():
	username = request.form['username']
	password = request.form['password']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']
	new_parent = model.Parent(username = username, password = password, zipcode = zipcode, neighborhood = neighborhood)
	model.db_session.add(new_parent)
	model.db_session.commit()
	print "new parent added: ", new_parent
	return render_template('testing.html', username = username)

@app.route('/par_signup')
def par_signup():
	return render_template('par_signup.html')


@app.route('/new_daycare', methods=['POST'])
def new_daycare():
	username = request.form['username']
	password = request.form['password']
	biz_name = request.form['biz_name']
	primary_contact = request.form['primary_contact']
	zipcode = request.form['zipcode']
	neighborhood = request.form['neighborhood']
	address = request.form['address']
	phone = request.form['phone']
	email = request.form['email']
	web_url = request.form['web_url']
	fb_url = request.form['fb_url']
	yr_in_biz = request.form['yr_in_biz']
	capacity = request.form['capacity']
	num_staff = request.form['num_staff']
	license_num = request.form['license_num']
	about_us = request.form['about_us']

	new_daycare = model.Daycare(username = username, password = password, biz_name = biz_name, primary_contact = primary_contact, zipcode = zipcode, neighborhood = neighborhood, address = address, phone = phone, email = email, web_url = web_url, fb_url = fb_url, yr_in_biz = yr_in_biz, capacity = capacity, num_staff = num_staff, license_num = license_num, about_us = about_us)
	model.db_session.add(new_daycare)
	model.db_session.commit()
	return render_template('testing.html', username = username)

@app.route('/dc_signup')
def dc_signup():
	return render_template('dc_signup.html')

	
# @app.route('/search_page')
# def search_page(): 
# 	return render_template('landing_page.html')

@app.route('/search_page')
def search_page(): 
	zipcode = request.form['zipcode']
	daycare_list = model.db_session.query(model.Daycare).filter_by(zipcode = zipcode).all()
	return render_template('daycare_list_results.html', daycare_list=daycare_list)


@app.route('/viewdc/<int:daycare.id>')
def view_daycare():
	daycare_obj = model.session.query(model.Daycare).filter_by(daycare = daycare.id).one()
	return redirect('view_daycare_page.html', daycare_obj = daycare_obj)


if __name__ == "__main__":
    app.run(debug = True)
