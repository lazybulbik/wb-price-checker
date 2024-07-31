from flask import Flask
from database_server import Database

app = Flask(__name__)
db = Database('http://127.0.0.1:5050')