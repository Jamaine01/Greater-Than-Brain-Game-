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

def search_score(search_name):
	#SQLITE DOESNT SUPPORT VARIABLE INSERTIONS
	db.execute('''
		SELECT score FROM scores WHERE name = ? ORDER BY id
		''', (search_name,))
	return db.fetchall()

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
	if request.form['name'] != "":
		name = request.form['name']
		score = request.form['score']
		save_score(name, score)
		print score
		return render_template('start.html')
	else:
		return render_template('start.html')

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/results', methods = ['POST'])
def search():
	search = request.form['search']
	results = search_score(search)
	final_results = []
	for r in results:
		r = str(r).replace('(','').replace(')','').replace(',','')
		final_results.append(r)
	return render_template('results.html',search = search, final_results = final_results)


