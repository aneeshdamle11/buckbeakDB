import mysql.connector as mc


# connect to mydatabase (database will be created if DNE)
def authorise_database():
    conn = mc.connect(host='localhost',
                      user='buckbeak',
                    # password='optional',
                      db='airlineDB')
    return conn

# clear_tables: deletes existing tables 
# TODO: Testing purpose, to be removed later
def clear_tables(c):
    c.execute("DROP TABLE IF EXISTS passenger")
    c.execute("DROP TABLE IF EXISTS booked_for_flight")
    c.execute("DROP TABLE IF EXISTS flying_by")
    c.execute("DROP TABLE IF EXISTS ticket")
    c.execute("DROP TABLE IF EXISTS flight")
    c.execute("DROP TABLE IF EXISTS jet")
    c.execute("DROP TABLE IF EXISTS admin_logs")

# create_tables: executes DDL commands of database
# TODO: Implement
def create_tables(c):
    # ticket
    c.execute('CREATE TABLE ticket ( \
               ticket_id INTEGER NOT NULL AUTO_INCREMENT, \
               date VARCHAR(10) NOT NULL, \
               time VARCHAR(10) NOT NULL, \
               price INTEGER NOT NULL, \
               email_id VARCHAR(20), \
               phone_no VARCHAR(10), \
               PRIMARY KEY (ticket_id))')

    # passenger
    c.execute("CREATE TABLE passenger (\
               ticket_id INTEGER NOT NULL, \
               first_name VARCHAR(20) NOT NULL,\
               last_name VARCHAR(20) NOT NULL,\
               seat_no VARCHAR(50) NOT NULL,\
               PRIMARY KEY (ticket_id, seat_no), \
               FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)\
               ON DELETE CASCADE ON UPDATE CASCADE)")
    
    # flight
    c.execute("CREATE TABLE flight(\
               flight_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,\
               from_city VARCHAR(20) NOT NULL,\
               to_city VARCHAR(20) NOT NULL,\
               departure_date VARCHAR(10) NOT NULL,\
               departure_time VARCHAR(10) NOT NULL,\
               arrival_date VARCHAR(10) NOT NULL,\
               arrival_time VARCHAR(10) NOT NULL,\
               price INTEGER NOT NULL,\
               PRIMARY KEY (flight_id));")

    # booked_for_flight --> ticket to flight
    c.execute("CREATE TABLE booked_for_flight(\
               ticket_id INTEGER NOT NULL, \
               flight_id INTEGER NOT NULL,\
               PRIMARY KEY (ticket_id),\
               FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)\
               ON DELETE CASCADE ON UPDATE CASCADE, \
               FOREIGN KEY (flight_id) REFERENCES flight(flight_id)\
               ON DELETE CASCADE ON UPDATE CASCADE)")\

    # jet
    c.execute("CREATE TABLE jet (\
               jet_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,\
               name VARCHAR(20),\
               status CHAR(1) NOT NULL,\
               capacity INTEGER NOT NULL,\
               PRIMARY KEY (jet_id));")

    # flying_by --> flight to jet
    c.execute("CREATE TABLE flying_by (\
               flight_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT, \
               jet_id INTEGER NOT NULL, \
               available_seats INTEGER NOT NULL,\
               PRIMARY KEY (flight_id),\
               FOREIGN KEY (flight_id) REFERENCES flight(flight_id)\
               ON DELETE CASCADE ON UPDATE CASCADE, \
               FOREIGN KEY (jet_id) REFERENCES jet(jet_id)\
               ON DELETE CASCADE ON UPDATE CASCADE);")

    # admin log
    c.execute("CREATE TABLE admin_logs (\
               admin_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,\
               username VARCHAR(20) NOT NULL,\
               password VARCHAR(20) NOT NULL, \
               email_id VARCHAR(20), \
               PRIMARY KEY (admin_id));")


# insert_vals: executes DML commands of database
# TODO: Implement
def insert_vals(conn, c):
    # flight schedule
    insert_into_flight = 'INSERT INTO flight (from_city, to_city, \
    departure_date, departure_time, arrival_date, arrival_time, price)'

    insert_into_flying_by = 'INSERT INTO flying_by'

    insert_into_jet = 'INSERT INTO jet (name, status, capacity)'

    c.execute(insert_into_flight + 'VALUES \
    ("PUNE", "DELHI", "07/11/2022","23:00", "08/11/2022", "01:00", "8000");')

    c.execute(insert_into_flight + 'VALUES \
    ("PUNE", "DELHI", "07/11/2022","18:00", "07/11/2022", "20:00", "7000")')

    c.execute(insert_into_flight + 'VALUES \
    ("BANGALORE", "DELHI", "07/11/2022","23:00", "08/11/2022", "01:30", "6000")')

    c.execute(insert_into_flight + 'VALUES \
  ("BANGALORE", "DELHI", "07/11/2022","20:00", "07/11/2022", "22:00", "9000")')

    c.execute(insert_into_flight + 'VALUES \
  ("BANGALORE", "DELHI", "07/11/2022","17:00", "07/11/2022", "19:00", "9000")')

    c.execute(insert_into_flight + 'VALUES \
  ("DELHI", "CHENNAI", "07/11/2022","23:00", "08/11/2022", "01:00", "9000")')


    c.execute(insert_into_jet + ' VALUES ("AIRBUS", 1, 100)')
    c.execute(insert_into_jet + ' VALUES ("BOEING", 1, 250)')
    c.execute(insert_into_jet + ' VALUES ("INDIGO", 1, 200)')
    c.execute(insert_into_jet + ' VALUES ("AIRINDIA", 1, 200)')
    c.execute(insert_into_jet + ' VALUES ("LUFTHANSA", 1, 225)')

    c.execute(insert_into_flying_by + ' VALUES (1, 1, 100)')
    c.execute(insert_into_flying_by + ' VALUES (2, 2, 250)')
    c.execute(insert_into_flying_by + ' VALUES (3, 3, 200)')
    c.execute(insert_into_flying_by + ' VALUES (4, 4, 200)')
    c.execute(insert_into_flying_by + ' VALUES (5, 5, 225)')
    c.execute(insert_into_flying_by + ' VALUES (6, 1, 225)')

    conn.commit() # apply changes

    return 0


if __name__=='__main__':
    conn = authorise_database()
    c = conn.cursor()
    clear_tables(c)
    create_tables(c)
    insert_vals(conn, c)
    c.execute("SELECT * FROM flight")
    print(c.fetchall())
    conn.close()
