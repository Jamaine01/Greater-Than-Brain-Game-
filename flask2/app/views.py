from app import app
from flask import Flask, render_template, request, abort, Markup
import sqlite3
from random import randint
import pygal
from pygal.style import DarkSolarizedStyle

conn = sqlite3.connect('scores.db', check_same_thread=False)
db = conn.cursor()

def save_score(name, score, difficulty):
	#SAVE NAME ENTERED AND SCORES TO DB
	db.execute('''
		INSERT INTO scores(name, score, difficulty) VALUES(?,?,?)
		''', (name, score, difficulty))
	conn.commit()

def search_score(search_name):
	#SQLITE DOESNT SUPPORT VARIABLE INSERTIONS
	db.execute('''
		SELECT score, difficulty, timestamp FROM scores WHERE name = ? ORDER BY id
		''', (search_name,))
	return db.fetchall()

@app.route('/chart')
def graph():
	results = search_score('Jamaine')
	times = []
	scores = []
	for li in results:
		scores.append(li[0])
		times.append(str(li[2].replace('u', '').replace("'", '')))
	print 'Times', times
	print 'Scores', scores 
	title = 'Test'
	bar_chart = pygal.Bar(width=1200, height=600, explicit_size=True, title=title, style=DarkSolarizedStyle)
	bar_chart.x_labels = times
	bar_chart.add('Scores', scores)
	return render_template('chart.html', title=title, bar_chart=bar_chart)

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

@app.route('/fail/<score>/<difficulty>')
def fail(score, difficulty):
	return render_template('fail.html', score = score, difficulty = difficulty)

@app.route('/save', methods = ['POST'])
def save():
	#RETURN START PAGE IF NO NAME ENTERED
	if request.form['name'] != "":
		#IF NAME ENTERED, TAKES FORM VALUES AND SAVES THEM TO DB
		name = request.form['name']
		score = request.form['score']
		difficulty = request.form['difficulty']
		save_score(name, score, difficulty)
		print score
		return render_template('start.html')
	else:
		return render_template('start.html')

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/results', methods = ['POST'])
def search():
	#SETS VAR SEARCH TO FORM VALUE
	search = request.form['search']
	#FIND SCORES IN DB WITH FORM VALUE RESULTS
	results = search_score(search)

	print results

	final_results_easy = []
	high_easy = []
	final_results_med = []
	high_med = []
	final_results_hard = []
	high_hard = []
	#CLEANS UP SEARCH RESULTS, APPEND THEM TO LIST(FINAL_RESULTS)
	for r in results:
		if 'Easy' in r:
			high_easy.append(int(r[0]))
			r = str(r).replace('(','').replace(')','').replace(',',' --- ').replace("u'", "'").replace('2016-', '').replace('06-', 'June, ').replace('07', 'July')
			final_results_easy.append(r)
		elif 'Medium' in r:
			high_med.append(int(r[0]))
			r = str(r).replace('(','').replace(')','').replace(',',' --- ').replace("u'", "'").replace('2016-', '').replace('06-', 'June, ').replace('07', 'July')
			final_results_med.append(r)
		else :
			high_hard.append(int(r[0]))
			r = str(r).replace('(','').replace(')','').replace(',',' --- ').replace("u'", "'").replace('2016-', '').replace('06-', 'June, ').replace('07', 'July')
			final_results_hard.append(r)
	hi_easy = max(high_easy)
	hi_med = max(high_med)
	hi_hard = max(high_hard)
	sorted_results = sorted(final_results_easy)
	high_score = sorted_results[0]
	return render_template('results.html',search = search, high_score = high_score, final_results_easy = final_results_easy, final_results_med = final_results_med, final_results_hard = final_results_hard, hi_easy = hi_easy, hi_med = hi_med, hi_hard = hi_hard)


