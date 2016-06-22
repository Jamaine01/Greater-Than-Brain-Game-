from app import app
from flask import Flask, render_template, request, abort, Markup
import sqlite3
from random import randint

conn = sqlite3.connect('scores.db', check_same_thread=False)
db = conn.cursor()

def save_score(name, score):
	db.execute('''
		INSERT INTO scores(name, score) VALUES(?,?)
		''', (name, score))
	conn.commit()

@app.route('/')
def home():
	return render_template('start.html')

@app.route('/begin')
def name_input():
	return render_template('begin.html')

@app.route('/play_easy')
def game_easy():
	return render_template('play_easy.html')

@app.route('/play_med')
def game_med():
	return render_template('play_med.html')

@app.route('/play_hard')
def game_hard():
	return render_template('play_hard.html')

@app.route('/fail/<score>')
def fail(score):
	return render_template('fail.html', score = score)

@app.route('/save', methods = ['POST'])
def save():
	name = request.form['name']
	score = request.form['score']
	save_score(name, score)
	print score
	return render_template('start.html')
