from flask import Flask
from database_server import Database

app = Flask(__name__)
db_url = 'http://178.208.92.230:5050'
db = Database(db_url)
BUFFER = {}