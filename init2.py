#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os  # Add this import


#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='FinalProject',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

template_dir = os.path.abspath('Project')  # Adjust the path accordingly
app.template_folder = template_dir 

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#-------------------------------------------------------------------------
# LOGIN INFO

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE c_email_address = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#-------------------------------------------------------------------------
# REGISTER INFO

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the register
@app.route('/registerAuth', methods=['POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    building_num = request.form['building_num']
    street = request.form['street']
    apt_num = request.form['apt_num']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']

    #cursor used to send queries
    cursor = conn.cursor()

    #executes query to check if the user already exists
    query = 'SELECT * FROM customer WHERE c_email_address = %s'
    cursor.execute(query, (username,))
    
    #stores the results in a variable
    data = cursor.fetchone()

    #use fetchall() if you are expecting more than 1 data row
    error = None

    if data:
        #If the previous query returns data, then the user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        # Insert new user into the database with all fields
        ins = '''
            INSERT INTO customer (
                c_email_address, password, first_name, last_name, date_of_birth,
                building_num, street, apt_num, city, state, zip_code, phone_number,
                passport_number, passport_expiration, passport_country
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(
            ins, (
                username, password, first_name, last_name, date_of_birth,
                building_num, street, apt_num, city, state, zip_code, phone_number,
                passport_number, passport_expiration, passport_country
            )
        )
        conn.commit()
        cursor.close()
        return render_template('index.html')

#-------------------------------------------------------------------------
# AIRLINE STAFF REGISTER

#Define route for AirlineStaffRegister
@app.route('/registerAirline')
def register_airline_homepage():
	return render_template('registerAirline.html')

#Authenticates the register for airline_staff
@app.route('/registerAirline', methods=['POST'])
def registerAirlineStaffAuth():
    #grabs information from the forms
    username = request.form['username']
    airline_name = request.form['airline_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    password = request.form['password'] 
    #cursor used to send queries
    cursor = conn.cursor()

    #executes query to check if the user already exists
    query = 'SELECT * FROM airline_staff WHERE username = %s AND airline_name = %s'
    cursor.execute(query, (username, airline_name))

    #stores the results in a variable
    data = cursor.fetchone()

    #use fetchall() if you are expecting more than 1 data row
    error = None

    if data:
        # If the previous query returns data, then the user exists
        error = "This user already exists"
        return render_template('registerAirline.html', error=error)
    else:
        # Insert new staff into the database
        ins = '''
            INSERT INTO airline_staff (
                username, airline_name, first_name, last_name, date_of_birth, password
            ) VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(
            ins, (username, airline_name, first_name, last_name, date_of_birth, password)
        )
        conn.commit()
        cursor.close()
        return render_template('index.html')

#-------------------------------------------------------------------------
# Airline Staff LOGIN INFO
#Define route for login
@app.route('/Airlinelogin')
def AirlineLogin():
	return render_template('Airlinelogin.html')

#Authenticates the login
@app.route('/Airlinelogin', methods=['GET', 'POST'])
def AirlineloginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('AirlineHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('Airlinelogin.html', error=error)

#-------------------------------------------------------------------------
# AIRLINE STAFF HOMEPAGE INFO

#Define route for AirlineStaffHomepage
@app.route('/AirlineStaffHomepage')
def homepage():
	return render_template('AirlineStaffHomepage.html')

#Authenticates the AirlineStaffHomepage
@app.route('/AirlineStaffHomepageAuth', methods=['GET', 'POST'])
def AirlineStaffHomepageAuth():
	#grabs information from the forms
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM flight WHERE airline_name = %s'
	cursor.execute(query, (airline_name))
	#stores the results in a variable
	data1 = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None

	return render_template('ASview.html', data=data1)

#-------------------------------------------------------------------------
# AIRLINE STAFF VIEW FLIGHTS INFO

#Define route for AirlineStaffViewFlights
@app.route('/ASviewFlights')
def ASviewFlights():
	return render_template('AirlineStaffViewFlights.html')

	
#Authenticates the AirlineStaffViewFlights
@app.route('/ASviewFlightsAuth', methods=['GET', 'POST'])
def ASviewFlightsAuth():	
	flight_num = request.form['flight_num']
	airline_name = request.form['airline_name']
	airport_code = request.form['airport_code']
	ticket_base_price = request.form['ticket_base_price']
	capacity = request.form['capacity']
	status = request.form['status']
	arrival_airport  = request.form['arrival_airport']
	arrival_date = request.form['arrival_date']
	arrival_time = request.form['arrival_time']
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']

#-------------------------------------------------------------------------
# AIRLINE STAFF CREATE FLIGHT INFO

#Define route for AirlineStaffCreateFlight
@app.route('/createFlight')
def createFlight():
	return render_template('AirlineStaffCreateFlight.html')

#Authenticates the AirlineStaffCreateFlight
@app.route('/createFlightAuth', methods=['GET', 'POST'])
def createFlightAuth():	
	flight_num = request.form['flight_num']

#-------------------------------------------------------------------------




@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, c_email_address FROM customer WHERE c_email_address = %s ORDER BY c_email_address'
    cursor.execute(query, (username,))
    data1 = cursor.fetchall()
    cursor.close()

    for each in data1:
        print(each['first_name'])

    return render_template('home.html', username=username, posts=data1)


@app.route('/AirlineHome')
def AirlineHome():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT first_name, airline_name FROM airline_staff WHERE username = %s ORDER BY username'
    cursor.execute(query, (username,))
    data1 = cursor.fetchall()
    cursor.close()

    for each in data1:
        print(each['first_name'])

    return render_template('AirlineHome.html', username=username, posts=data1)
		
# @app.route('/post', methods=['GET', 'POST'])
# def post():
# 	username = session['username']
# 	cursor = conn.cursor();
# 	blog = request.form['blog']
# 	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
# 	cursor.execute(query, (blog, username))
# 	conn.commit()
# 	cursor.close()
# 	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5100, debug = True)