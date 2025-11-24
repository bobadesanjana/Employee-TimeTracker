from flask import Flask

app = Flask(__name__)

from views import *
if __name__ == "__main__":
    app.secret_key= "this is app secret key"
    app.run(host="localhost",port=3000,debug=True)