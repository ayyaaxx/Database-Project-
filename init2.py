#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os  # Add this import
from datetime import datetime
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

@app.route('/ASviewFlightsloggedAuth', methods=['GET'])
def ASviewFlightsloggedAuth():
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
    return render_template('ASviewFlightsloggedAuth.html', flights=flights)

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
@app.route('/add_tickets/<flight_num>', methods=['GET', 'POST'])
def add_tickets(flight_num):
    if request.method == 'POST':
        # Get information from the form
        ticket_id = request.form['ticket_id']
        c_email_address = request.form['c_email_address']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        ticket_sale_price = request.form['ticket_sale_price']
        purchased_date = request.form['purchased_date']
        purchased_time = request.form['purchased_time']

        # Insert the new ticket into the database with the associated flight_num
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
    return render_template('add_tickets.html', flight_num=flight_num)

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

#-----------------------------------------------------------------------
#CUSTOMER TRACK SPENDING

@app.route('/spending', methods=['GET'])
def track_spending():
    # Assuming you have a way to get the user's email address from the session
    c_email_address = session.get('username')


    if not c_email_address:
        # Handle the case where there's no user in the session
        error_message = "No user in session"
        return render_template('error.html', error=error_message)


    cursor = conn.cursor()


    # Total spending for the past year
    query1 = 'SELECT SUM(ticket_sale_price) FROM ticket WHERE c_email_address = %s AND purchased_date >= CURDATE() - INTERVAL 1 YEAR'
    cursor.execute(query1, (c_email_address,))
    past_year = cursor.fetchone()# Fetch the sum directly


    query2 = """SELECT MONTH(purchased_date) AS month, YEAR(purchased_date) AS year, SUM(ticket_sale_price) AS total_spent
                FROM ticket
                WHERE c_email_address = %s AND purchased_date >= CURDATE() - INTERVAL 6 MONTH
                GROUP BY month, year;"""
    cursor.execute(query2, (c_email_address,))
    six_months = cursor.fetchall()
   
    # Date range input from the user
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')


    # Query for spending within the specified date range
    query_range = """SELECT MONTH(purchased_date) AS month, YEAR(purchased_date) AS year, SUM(ticket_sale_price) AS total_spent
                     FROM ticket
                     WHERE c_email_address = %s AND purchased_date BETWEEN %s AND %s
                     GROUP BY month, year;"""
    cursor.execute(query_range, (c_email_address, start_date, end_date))
    spending_range = cursor.fetchall()


    cursor.close()


    return render_template('spending.html', past_year=past_year, six_months=six_months, spending_range=spending_range)

#-----------------------------------------------------------------------
#CUSTOMER RATING/COMMENTS
@app.route('/review_flight', methods=['GET', 'POST'])
def review_flight():
    if request.method == "POST":
        c_email_address = session.get('username')


        if not c_email_address:
            # No username in session, return an error response
            error_message = "No username in session"
            return render_template('error.html', error=error_message)


        rating = request.form['rating']
        comments = request.form['comments']
        selected_flight_num = request.form['selected_flight_num']


        # Insert the rating, comments, and selected flight_num into the database
        cursor = conn.cursor()
        rating_query = 'INSERT INTO customer_flight_rating (c_email_address, flight_num, rating, comments) VALUES (%s, %s, %s, %s)'
        cursor.execute(rating_query, (c_email_address, selected_flight_num, rating, comments))
        conn.commit()
        cursor.close()


        return redirect(url_for('home'))


    else:
        # Handle the case where the request method is a "GET" request
        c_email_address = session.get('username')


        if not c_email_address:
            # No username in session, return an error response
            error_message = "No username in session"
            return render_template('error.html', error=error_message)


        # Get the flights that the customer has already taken
        cursor = conn.cursor()
        current_datetime = datetime.now()
        flight_query = """SELECT DISTINCT f.flight_num
                           FROM ticket t JOIN flight f ON t.flight_num = f.flight_num
                           WHERE t.c_email_address = %s AND f.departure_date < %s
                        """


        cursor.execute(flight_query, (c_email_address, current_datetime.date()))
        customer_flights = cursor.fetchall()
        cursor.close()


        return render_template('review_flight.html', customer_flights=customer_flights)
#--------------------------------------------------------------------------------------
#AIRLIINE STAFF VIEW COMMENTS
@app.route('/ASviewcomments/<flight_num>', methods=['GET'])
def view_flight_ratings(flight_num):
    cursor = conn.cursor()


    # Query to get average rating and all comments for a specific flight
    query = 'SELECT AVG(rating) AS avg_rating, comments FROM customer_flight_rating WHERE flight_num = %s GROUP BY comments'
    cursor.execute(query, (flight_num,))
    ratings_data = cursor.fetchall()


    cursor.close()


    return render_template('ASViewComments.html', flight_num=flight_num, ratings_data=ratings_data)

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
#         purchased_date = request.form['purchased_date']
#         purchased_time = request.form['purchased_time']

#         # Insert the new ticket into the database
#         cursor = conn.cursor()
#         query = '''
#             INSERT INTO ticket (
#                 ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price, purchased_date, purchased_time
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         '''
#         cursor.execute(
#             query, (ticket_id, flight_num, c_email_address, first_name, last_name, date_of_birth, ticket_sale_price, purchased_date, purchased_time)
#         )
#         conn.commit()
#         cursor.close()

#         # Redirect to a page showing the added ticket or any other relevant page
#         return redirect(url_for('show_tickets'))

#     # Render the form to add a new ticket
#     return render_template('add_tickets.html')


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

from flask import request, redirect, url_for

@app.route('/delete_ticket/<ticket_id>', methods=['DELETE', 'POST'])
def delete_ticket(ticket_id):
    # Your delete logic here

    # Use the ticket_id from the URL to identify the ticket to be deleted
    cursor = conn.cursor()

    # Execute the delete query
    query = 'DELETE FROM ticket WHERE ticket_id = %s'
    cursor.execute(query, (ticket_id,))
    conn.commit()

    cursor.close()

    # Redirect to a page showing remaining tickets or any other relevant page
    return redirect(url_for('show_tickets'))

@app.route('/maintenance_schedule_success', methods=['GET'])
def maintenance_schedule_success():
    cursor = conn.cursor()

    query = '''
        SELECT airplane.airplane_id, airplane.model_num, maintenance.start_date
        FROM airplane
        JOIN maintenance ON airplane.maintenance_id = maintenance.maintenance_id
    '''
    cursor.execute(query)
    airplanes_scheduled_for_maintenance = cursor.fetchall()
    cursor.close()
    return render_template('maintenance_schedule_success.html', airplanes=airplanes_scheduled_for_maintenance)


# Route to schedule maintenance
@app.route('/schedule_maintenance', methods=['GET', 'POST'])
def schedule_maintenance():
    if request.method == 'POST':
        # Extract form data
        maintenance_id = request.form['maintenance_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Perform necessary validations on the data

        # Insert maintenance information into the database
        cursor = conn.cursor()
        query = '''
           INSERT INTO maintenance (maintenance_id, start_date, end_date)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (maintenance_id, start_date, end_date))
        conn.commit()
        cursor.close()

        # Redirect to a page showing the scheduled maintenance or any other relevant page
        return redirect(url_for('maintenance_schedule_success'))

    # Render the form to schedule maintenance
    return render_template('schedule_maintenance.html')

@app.route('/ASchangeFlightStatus', methods=['GET'])
def ASchangeFlightStatus():
    flight_num = request.args.get('flight_num')

    cursor = conn.cursor()
    query_status = 'SELECT status FROM flight WHERE flight_num = %s'
    cursor.execute(query_status, (flight_num,))
    current_status = cursor.fetchone()['status']
    cursor.close()

    return render_template('ASchangeFlightStatus.html', flight_num=flight_num, current_status=current_status)


@app.route('/update_flight_status', methods=['POST'])
def update_flight_status():
    flight_num = request.form['flight_num']
    new_status = request.form['status']

    cursor = conn.cursor()
    query = 'UPDATE flight SET status = %s WHERE flight_num = %s'
    cursor.execute(query, (new_status, flight_num))
    conn.commit()
    cursor.close()

    return redirect(url_for('ASfutureFlights', message='Flight status updated successfully'))



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