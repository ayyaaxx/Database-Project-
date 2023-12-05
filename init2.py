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

template_dir = os.path.abspath('project')  # Adjust the path accordingly
app.template_folder = template_dir 

#Define a route to index
@app.route('/')
def index():
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
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE c_email_address = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#-------------------------------------------------------------------------
# AIRLINE STAFF HOMEPAGE INFO

#Define route for AirlineStaffHomepage
@app.route('/AirlineStaffHomepage')
def homepage():
	return render_template('AirlineStaffHomepage.html')

#-------------------------------------------------------------------------
# AIRLINE STAFF VIEW FLIGHTS INFO

# #Define route for AirlineStaffViewFlights
@app.route('/ASviewFlights')
def ASviewFlights():
	return render_template('ASview.html')

@app.route('/ASviewFlightsAuth')
def ASviewFlightsAuth():
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM flight'
	cursor.execute(query)
	result = cursor.fetchall()
	cursor.close()

	return render_template('ASview.html', result = result)
	


#-------------------------------------------------------------------------
# AIRLINE STAFF CREATE FLIGHT INFO

#Define route for AirlineStaffCreateFlight
@app.route('/createFlight')
def createFlight():
	return render_template('AirlineStaffCreateFlight.html')

#Authenticates the AirlineStaffCreateFlight
@app.route('/createFlightAuth', methods=['POST'])
def createFlightAuth():	
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

	cursor = conn.cursor()

	airportCheck_query = "SELECT airport_code FROM airport WHERE airport_code = %s"
	cursor.execute(airportCheck_query, (airport_code,))
	existing_airport = cursor.fetchone()

	if existing_airport:
		flight_query = "INSERT INTO flight (flight_num, airline_name, airport_code, ticket_base_price, capacity, status, arrival_airport, arrival_date, arrival_time, departure_airport, departure_date, departure_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

		# Execute the query with the form data
		cursor.execute(flight_query, (flight_num, airline_name, airport_code, ticket_base_price, capacity, status,
							arrival_airport, arrival_date, arrival_time, departure_airport, departure_date, departure_time))

		# Commit the changes to the database
		conn.commit()

		return "Flight created successfully!"

	else:
		return "Airport with code {} does not exist.".format(airport_code)


	# Close the cursor
	cursor.close()

	# Redirect to a success page or return a success response
	return redirect('/')



	# return render_template('index.html')

#-------------------------------------------------------------------------
# AIRLINE STAFF CHANGE STATUS OF FLIGHT

#Define route for ASchangeFlightStatus
@app.route('/changeFlightStatus')
def changeFlightStatus():
	return render_template('ASchangeFlightStatus.html')

#Authenticates the ASchangeFlightStatus
# @app.route('/changeFlightStatus', methods=['POST'])
# def changeFlight():	




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


@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
if __name__ == "__main__":
	app.run('127.0.0.1', 5100, debug = True)