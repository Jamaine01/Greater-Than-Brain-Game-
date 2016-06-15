from app import app
from flask import Flask, render_template, request, abort
import sqlite3
from random import randint

@app.route('/')
def home():
	return render_template('start.html')

@app.route('/play')
def game():
	num_one = randint(20,100)
	num_two = randint(20, 100)

	return render_template('play.html', num_one = num_one, num_two = num_two)