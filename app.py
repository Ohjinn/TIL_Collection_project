from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbTil

@app.route('/')
def index():
    return render_template('index.html')





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
