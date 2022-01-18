from flask import Flask

app = Flask(__name__)

from Pocasi.web_app import routes
