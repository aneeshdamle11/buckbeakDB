This project plays a part in understanding and implementing some of the interesting concepts from the Database Management System coursework.
It aims to provide an idea on how to aid airline customers in ticket bookings, and, from a CS perspective, how much of an important role does a Database play.
The name is inspired by a timeless classic on platform 9-3/4:)

## Setup
Install the following packages:
- python
> venv
- mysql (root setup) [Ref 3]
> Create a different user with all privileges granted. Reference: Method 2 of [Ref 4]

> Add the same in src/database_tools.py - Line 6, 7, 8

> Create a database named "airlineDB" with said all-accessible user

## Startup
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt # Might get a mysql error here, make sure the mysql setup is correct [Ref: 3]
$ python3 src/app.py # Might get a mysql error here, refer [4]
```

## References:
1. https://flaskguide.readthedocs.io/en/latest/flask/flask2.html
2. https://mysqlguide.readthedocs.io/en/latest/mysql/python.html
3. https://www.mysqltutorial.org/install-mysql-ubuntu/
4. Responding to a common access error: https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
