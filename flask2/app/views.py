from app import app
from flask import Flask, render_template, request, abort
import sqlite3
from random import randint

@app.route('/')
def home():
	return render_template('start.html')

@app.route('/begin')
def name_input():
	return render_template('name_begin.html')

# global score 
# score = -1

@app.route('/play')
def game():
	# global score 
	# score = score + 1
	return render_template('play.html')

@app.route('/fail')
def fail():
	return render_template('fail.html')
