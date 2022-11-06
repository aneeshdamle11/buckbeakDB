import mysql.connector as mc
from app import *
from flask import render_template, request, redirect
import database_tools as dbt

# Initialise DDL in database, insert example values
conn = dbt.authorise_database()
c = conn.cursor()
dbt.clear_tables(c)
dbt.create_tables(c)
dbt.insert_vals(conn, c)
conn.close()


# home page
@app.route('/') # root : main page
def index():
    return render_template('index.html')

available_flights = 0

# available flights display page
@app.route('/disp_flights', methods=['GET', 'POST'])
def disp_flights():
    global available_flights
    # get From, To and Departure time from user
    if request.method == 'POST':
        fromcity = request.form['from_city'].upper()
        tocity = request.form['to_city'].upper()
        deptdate = request.form['dept_date']

        print(fromcity, tocity, deptdate, type(fromcity), type(tocity),type(deptdate))
        try:
            conn = dbt.authorise_database()
            c = conn.cursor()
            c.execute(f"SELECT * \
                         FROM flight \
                        WHERE from_city = '{fromcity}'\
                          AND to_city = '{tocity}'\
                          AND departure_date='{deptdate}';")
            available_flights = c.fetchall()
            conn.commit()
            return render_template("flights.html", rows=available_flights)
        except mc.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close() # close the connection
    return 0

available_seats = 0

@app.route('/passenger', methods=['GET', 'POST'])
def passenger():
    global available_flights, available_seats
    if request.method == 'POST':
        flight_id = int(request.form["flight_id"])
        passenger_count = int(request.form["passenger_count"])
        try:
            conn = dbt.authorise_database()
            c = conn.cursor() # cursor
            c.execute(f"SELECT available_seats \
                         FROM flying_by \
                        WHERE flight_id = {flight_id}")
            available_seats = c.fetchone()[0]
            conn.commit()
            c.execute(f"SELECT price \
                          FROM flight \
                         WHERE flight_id = {flight_id}")
            price = c.fetchone()
            conn.commit()
            # TODO: For now, only 1 passenger can enter name
            if (available_seats > passenger_count):
                return render_template('passenger.html', id=flight_id,
                        price=price)
            else:
                return render_template("flights.html", rows=available_flights)
        except mc.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close() # close the connection


@app.route('/ticket_gen', methods=['GET', 'POST'])
def ticket_gen():
    print('Entering \"/ticket_gen\"')
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        flight_id = request.form['id']

        try:
            conn = dbt.authorise_database()
            c = conn.cursor() # cursor
            # before generating ticket, reduce number of available seats
            print("Before reducing available seats")
            c.execute(f"UPDATE flying_by \
                           SET available_seats = available_seats - 1 \
                         WHERE flight_id = {flight_id}")
            conn.commit()
            print("After reducing available seats")
            # generate ticket
            print("Before fetching price")
            c.execute(f"SELECT price \
                          FROM flight \
                         WHERE flight_id = {flight_id}")
            price = int(c.fetchone()[0])
            conn.commit()
            print("After fetching price")

            import datetime
            e = datetime.datetime.now()
            curr_date = f"{e.day}/{e.month}/{e.year}"
            curr_time = f"{e.hour}:{e.minute}:{e.second}"

            print("HERE BEFORE TICKET ENTRY")

            c.execute(f'INSERT INTO ticket (date, time, price, email_id, phone_no) \
            VALUES ("{curr_date}", "{curr_time}", {price}, "{email}", "{phone}");')
            conn.commit()

            print("HERE AFTER TICKET ENTRY")

            print("HERE BEFORE getting TICKET ID")

            c.execute(f'SELECT MAX(ticket_id) FROM ticket')
            print("HERE BEFORE getting TICKET ID")
            ticketID = c.fetchone()[0]
            conn.commit()

            print("HERE AFTER getting TICKET ID")

            print("HERE BEFORE getting JETID")
            # Get name of flight
            c.execute(f"SELECT name\
                         FROM jet\
                        WHERE jet_id IN (\
                              SELECT jet_id\
                                FROM flying_by\
                               WHERE flight_id IN (\
                                     SELECT flight_id\
                                       FROM flight\
                                      WHERE flight_id={flight_id}\
                                     )\
                                 AND available_seats = {available_seats}-1)")
            jname = c.fetchone()[0]
            conn.commit()

            print("HERE AFTER getting JETID")

            print("HERE BEFORE INSERTING INTO passenger")
            seat_no = f"{jname}-{flight_id}-{available_seats}"
            print(ticketID, first, last, seat_no, type(ticketID), type(first),
                    type(last), type(seat_no))
            c.execute(f'INSERT INTO passenger VALUES \
                       ({ticketID}, "{first}", "{last}", "{seat_no}")')
            conn.commit()
            print("HERE AFTER INSERTING INTO passenger")

            print("HERE BEFORE INSERTING INTO booked_for_flight")
            print(f"TICKETID: {ticketID}")
            c.execute(f"INSERT INTO booked_for_flight VALUES \
                      ({ticketID}, {flight_id})")
            conn.commit()
            print("HERE AFTER INSERTING INTO booked_for_flight")

            return render_template('disp_ticket.html',
                                    flight_name=jname,
                                    first_name=first,
                                    last_name=last,
                                    email=email,
                                    phone=phone,
                                    seat_no=seat_no)

        except mc.Error as err: # if error
            # then display the error in 'database.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close()
    else:
        print("HELLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")


# Admin Login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = dbt.authorise_database()
            c = conn.cursor() # cursor
            c.execute(f'SELECT password \
                         FROM admin_logs \
                        WHERE username = "{username}";')
            pwd = c.fetchone()
            print(pwd, type(pwd))
            if pwd:
                if password == pwd[0]:
                    return render_template('admin_profile.html', username=username)
                else:
                    msg = "Incorrect username and password"
            else:
                msg = "Incorrect username and password"

        except mc.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close() # close the connection

    return render_template('admin_login.html', msg=msg)


@app.route('/logout')
def logout():
    return render_template('index.html')

# New admin registration
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            conn = dbt.authorise_database()
            c = conn.cursor() # cursor
            # insert data
            c.execute("SELECT username FROM admin_logs")
            users = c.fetchall()
            if not username or not password or not email:
                msg = 'Please fill out the form!'
            elif username in users:
                msg = 'Account already exists!'
            else:
                c.execute('INSERT INTO admin_logs (username, password, email_id) \
                        VALUES (%s, %s, %s)', (username, password, email))
                conn.commit()
                msg = 'You have successfully registered!'
        except mc.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close() # close the connection

    # Show registration form with message (if any)
    return render_template('admin_register.html', msg=msg)


@app.route('/add_jets', methods=['GET', 'POST'])
def add_jets():
    if request.method == 'POST':
        name = request.form['jet_name']
        status = request.form['status']
        capacity = request.form['capacity']

        try:
            conn = dbt.authorise_database()
            c = conn.cursor() # cursor
            # Add jet
            c.execute(f'INSERT INTO jet (name, status, capacity) VALUES \
                       ("{name}", "{status}", {capacity});')
            conn.commit()
        except mc.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            conn.close() # close the connection

    return render_template('index.html')




