from flask import Flask

# "app" as an object of class Flask
app = Flask(__name__)

# import files
from routes import *


if __name__=='__main__':
    # port = 5000 : we can modify it for localhost
    app.run(host='localhost', port=5000, debug=True) # local webserver : app.run()
