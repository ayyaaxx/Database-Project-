#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os  # Add this import
#Initialize the app from Flask
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()
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

	return render_template('AirlineStaffHomepage.html', data=data1)

#-------------------------------------------------------------------------
# AIRLINE STAFF VIEW FLIGHTS INFO

#Define route for AirlineStaffViewFlights
# @app.route('/ASviewFlightsAuth')
# def ASviewFlights():
# 	return render_template('ASviewFlightsAuth.html')

@app.route('/ASviewFlightsAuth', methods=['GET'])
def ASviewFlightsAuth():
    # Create a cursor
    cursor = conn.cursor()
    flight_num = request.args.get('flight_num') 

    # Execute the query to get flight information
    query = 'SELECT * FROM flight'
    cursor.execute(query)

    # Fetch all the results
    flights = cursor.fetchall()

    # Close the cursor
    cursor.close()
    print("Flights:", flights)

    # Render the HTML template with the flight data
    return render_template('ASviewFlightsAuth.html', flights=flights)

@app.route('/view_flight_logged', methods=['GET'])
def view_flight_logged():
    # Create a cursor
    c_email_address = session['username']
    cursor = conn.cursor()

    # Execute the query to get flight information
    query = 'SELECT t.*, f.*, c.* FROM ticket t JOIN flight f ON t.flight_num = f.flight_num JOIN customer c ON t.c_email_address = c.c_email_address WHERE t.c_email_address = %s'
    cursor.execute(query, (c_email_address,))

    # Fetch all the results
    flights = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Render the HTML template with the flight data
    return render_template('view_flight_logged.html', flights=flights)
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
# AIRLINE STAFF ADD A NEW AIRPORT 
@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if request.method == 'POST':
        # Get information from the form
        airport_code = request.form['airport_code']
        name = request.form['name']
        city = request.form['city']
        country = request.form['country']
        num_of_terminals = request.form['num_of_terminals']
        airport_type = request.form['airport_type']

        # Insert the new airport into the database
        cursor = conn.cursor()
        query = '''
            INSERT INTO airport (
                airport_code, name, city, country, num_of_terminals, airport_type
            ) VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(
            query, (airport_code, name, city, country, num_of_terminals, airport_type)
        )
        conn.commit()
        cursor.close()

        # Redirect to a page showing the added airport or any other relevant page
        return redirect(url_for('show_airports'))

    # Render the form to add a new airport
    return render_template('add_airport.html')
#-------------------------------------------------------------------------
# AIRLINE STAFF SHOW the airport added
@app.route('/show_airports', methods=['GET'])
def show_airports():
    cursor = conn.cursor()
    query = 'SELECT * FROM airport ORDER BY airport_code'
    cursor.execute(query)
    airports = cursor.fetchall()
    cursor.close()
    return render_template('show_airports.html', airports=airports)

# AIRLINE STAFF SHOW the airport added
@app.route('/add_airports', methods=['GET'])
def add_airports():
    cursor = conn.cursor()
    query = 'SELECT * FROM airport'
    cursor.execute(query)
    airports = cursor.fetchall()
    cursor.close()
    return render_template('add_airports.html', airports=airports)

#-------------------------------------------------------------------------
# AIRLINE STAFF SHOW the airplane added

# AIRLINE STAFF ADD A NEW AIRPLANE 
@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if request.method == 'POST':
        # Get information from the form
        airplane_id = request.form['airplane_id']
        airline_name = request.form['airline_name']
        maintenance_id = request.form['maintenance_id']
        num_of_seats = request.form['num_of_seats']
        airplane_age = request.form['airplane_age']
        model_num = request.form['model_num']

        # Insert the new airplane into the database
        cursor = conn.cursor()
        query = '''
            INSERT INTO airplane (
                airplane_id, airline_name, maintenance_id, num_of_seats, airplane_age, model_num
            ) VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(
            query, (airplane_id, airline_name, maintenance_id, num_of_seats, airplane_age, model_num)
        )
        conn.commit()
        cursor.close()

        # Redirect to a page showing the added airplane or any other relevant page
        return redirect(url_for('show_airplanes'))

    # Render the form to add a new airplane
    return render_template('add_airplane.html')

    # AIRLINE STAFF SHOW the airplanes added
@app.route('/show_airplanes', methods=['GET'])
def show_airplanes():
    cursor = conn.cursor()
    query = 'SELECT * FROM airplane ORDER BY airplane_id'
    cursor.execute(query)
    airplanes = cursor.fetchall()
    cursor.close()
    return render_template('show_airplanes.html', airplanes=airplanes)



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

@app.route('/spending', methods=['GET'])
def track_spending():
    cursor = conn.cursor()

    query1 = 'SELECT SUM(ticket_sale_price) FROM ticket WHERE purchased_date >= CURDATE() - INTERVAL 1 YEAR'
    cursor.execute(query1)
    past_year = cursor.fetchone()[0]  # Fetch the sum directly

    query2 = 'SELECT MONTH(purchased_date) AS month, SUM(ticket_sale_price) AS total_spent FROM ticket WHERE purchased_date >= CURDATE() - INTERVAL 6 MONTH GROUP BY month'
    cursor.execute(query2)
    six_months = cursor.fetchall()

    cursor.close()

    return render_template('home.html', past_year=past_year, six_months=six_months)

# Flask route for purchasing tickets

# Function to insert ticket data into the database
# def insert_ticket(ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price):
#     with conn.cursor() as cursor:
#         # Insert ticket data into the 'ticket' table
#         sql = "INSERT INTO ticket (ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price, purchased_date, purchased_time) VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE(), CURTIME())"
#         values = (ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price)
#         cursor.execute(sql, values)
#     conn.commit()

# AIRLINE STAFF ADD A NEW TICKET
# AIRLINE STAFF ADD A NEW TICKET
# @app.route('/add_tickets', methods=['GET', 'POST'])
# def add_tickets():
#     if request.method == 'POST':
#         # Get information from the form
#         ticket_id = request.form['ticket_id']
#         flight_num = request.form['flight_num']
#         c_email_address = request.form['c_email_address']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         date_of_birth = request.form['date_of_birth']
#         ticket_sale_price = request.form['ticket_sale_price']

#         # Insert the new ticket into the database
#         cursor = conn.cursor()
#         query = '''
#             INSERT INTO ticket (
#                 ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s)
#         '''
#         try:
#             cursor.execute(
#                 query, (ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price)
#             )
#             conn.commit()
#         except Exception as e:
#             conn.rollback()
#             print(f"Error inserting data: {e}")
#         finally:
#             cursor.close()

#         # Redirect to a page showing the added ticket or any other relevant page
#         return redirect(url_for('show_tickets'))

#     # Render the form to add a new ticket
#     return render_template('add_tickets.html')


# AIRLINE STAFF SHOW the tickets added
# @app.route('/show_tickets', methods=['GET'])
# def show_tickets():
#     cursor = conn.cursor()
#     query = 'SELECT * FROM ticket ORDER BY ticket_id'
#     cursor.execute(query)
#     tickets = cursor.fetchall()
#     cursor.close()
#     return render_template('show_tickets.html', tickets=tickets)



# @app.route('/show_tickets', methods=['GET', 'POST'])
# def show_tickets():
#     # Retrieve the c_email_address from the form data
#     c_email_address = request.form.get('c_email_address')

#     cursor = conn.cursor()

#     # Modify the query to include the condition for the logged-in user's email address
#     query = "SELECT * FROM ticket WHERE c_email_address = %s"

#     cursor.execute(query, (c_email_address,))
#     tickets = cursor.fetchall()
#     cursor.close()

#     return render_template('show_tickets.html', tickets=tickets)

# @app.route('/view_my_tickets', methods=['GET'])
# def view_my_tickets():
#     # Retrieve the c_email_address from the form data
#     c_email_address = session['username']

#     cursor = conn.cursor()

#     # Modify the query to include the condition for the logged-in user's email address
#     query = "SELECT * FROM ticket WHERE c_email_address = %s"

#     cursor.execute(query, (c_email_address,))
#     tickets = cursor.fetchall()
#     cursor.close()

#     return render_template('view_my_tickets.html', tickets=tickets)

# AIRLINE STAFF ADD A NEW TICKET
@app.route('/add_tickets', methods=['GET', 'POST'])
def add_tickets():
    if request.method == 'POST':
        # Get information from the form
        ticket_id = request.form['ticket_id']
        flight_num = request.form['flight_num']
        c_email_address = request.form['c_email_address']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        ticket_sale_price = request.form['ticket_sale_price']
        purchased_date = request.form['purchased_date']
        purchased_time = request.form['purchased_time']

        # Insert the new ticket into the database
        cursor = conn.cursor()
        query = '''
            INSERT INTO ticket (
                ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price, purchased_date, purchased_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(
            query, (ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price, purchased_date, purchased_time)
        )
        conn.commit()
        cursor.close()

        # Redirect to a page showing the added ticket or any other relevant page
        return redirect(url_for('show_tickets'))

    # Render the form to add a new ticket
    return render_template('add_tickets.html')


@app.route('/show_tickets', methods=['GET', 'POST'])
def show_tickets():
    # Retrieve the c_email_address from the form data
    c_email_address = session['username']

    cursor = conn.cursor()

    # Modify the query to include the condition for the logged-in user's email address
    query = "SELECT * FROM ticket WHERE c_email_address = %s"

    cursor.execute(query, (c_email_address,))
    tickets = cursor.fetchall()
    cursor.close()

    return render_template('show_tickets.html', tickets=tickets)

# @app.route('/view_my_tickets', methods=['GET'])
# def view_my_tickets():
#     # Retrieve the c_email_address from the form data
#     c_email_address = session['username']

#     cursor = conn.cursor()

#     # Modify the query to include the condition for the logged-in user's email address
#     query = "SELECT * FROM ticket WHERE c_email_address = %s"

#     cursor.execute(query, (c_email_address,))
#     tickets = cursor.fetchall()
#     cursor.close()

#     return render_template('view_my_tickets.html', tickets=tickets)
		
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

from flask import request, render_template


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