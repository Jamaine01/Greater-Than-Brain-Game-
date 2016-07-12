from app import app
from flask import Flask, render_template, request, abort, Markup
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
import sqlite3
from random import randint
import urllib
import json
import pygal
from pygal.style import Style
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
# from werkzeug.contrib.cache import GAEMemcachedCache
# import memcache

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
login_manager.init_app(app)

conn = sqlite3.connect('scores.db', check_same_thread=False)
db = conn.cursor()


def db_account(name, pwd):
	db.execute('''
		INSERT INTO scores(name, pwd) VALUES(?,?)
		''', (name, pwd))
	conn.commit()


def save_score(name, pwd, score, difficulty):
	#SAVE NAME ENTERED AND SCORES TO DB
	db.execute('''
		INSERT INTO scores(name, pwd, score, difficulty) VALUES(?,?,?,?)
		''', (name, pwd, score, difficulty))
	conn.commit()


def search_score(search_name, pwd_search):
	#SQLITE DOESNT SUPPORT VARIABLE INSERTIONS
	db.execute('''
		SELECT score, difficulty, timestamp FROM scores WHERE name = ? AND pwd = ?
		''', (search_name, pwd_search))
	return db.fetchall()

def login_db(myname, mypassword):
	db.execute('''
		SELECT name FROM scores WHERE name = ? AND pwd = ?
		''', (myname, mypassword))
	return db.fetchall()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/chart')
def graph():
	file = urllib.urlopen('https://data.seattle.gov/resource/kzjm-xkqj.json').read()

	data = json.loads(file)

	platforms = []

	platform_counts = {}

	for i in data:
		platforms.append(i['type'])

	for platform in platforms:
		platform_counts[platform] = platform_counts.get(platform, 0) + 1

	all_platforms = platform_counts.items()

	chart = pygal.Pie()

	chart.title = 'Fire Call Types'

	for i in all_platforms:
		percentage = i[1] * 0.1
		chart.add(i[0], percentage)

	return chart.render()
	# file = urllib.urlopen('https://data.cityofnewyork.us/resource/qfe3-6dkn.json').read()

	# data = json.loads(file)

	# locations = []

	# places = dict()

	# for i in data:
	# 	if 'city' in i:
	# 			locations.append(i['city'])

	# count = len(locations)

	# for place in locations:
	# 	places[place] = places.get(place, 0) + 1

	# places = places.items()

	# chart = pygal.Pie()
	# chart.title = 'Water Complaints'

	# for i in places:
	# 	percentage = i[1] * 0.0997
	# 	chart.add(i[0], percentage)

	# return chart.render()
		

@app.route('/')
def home():
	return render_template('start.html')

@app.route('/signup')
def signup_account():
	return render_template('create_account.html')

@app.route('/create', methods = ['POST']) 
def save_account_to_db():
	name = request.form['account_name']
	password = request.form['account_pwd']
	con_pwd = request.form['confirm_pwd']
	if password != con_pwd:
		return render_template('create_account.html')
	else:
		db_account(name, password)
		return render_template('login.html')

@app.route('/login-user')
def log_in():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    name = request.form['account_name']
    pwd = request.form['account_pwd']
    if len(name) >= 1:
    	confirm = login_db(name, pwd)
    	if len(confirm) >= 1:
    		print cache.get('name'), cache.get('pwd')
    		return name, render_template('begin.html')
    		cache.set('user', name, timeout=5 * 60)
    	return render_template('login.html')


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
	check = cache.get('user')
	if check!='None':
		print 'Ok!'
		print check
	return render_template('fail.html', score = score, difficulty = difficulty)

@app.route('/save', methods = ['POST'])
def save():
	#RETURN START PAGE IF NO NAME ENTERED
	if request.form['name'] != "":
		if request.form['pwd'] != "":
			#IF NAME ENTERED, TAKES FORM VALUES AND SAVES THEM TO DB
			name = request.form['name']
			pwd = request.form['pwd']
			score = request.form['score']
			difficulty = request.form['difficulty']
			save_score(name, pwd, score, difficulty)
			print score
			return render_template('start.html')
	else:
		return render_template('start.html')

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/results', methods = ['GET', 'POST'])
def search():
	#SETS VAR SEARCH TO FORM VALUE
	search_name = request.form['search']
	search_pwd = request.form['pwd_search']
	#FIND SCORES IN DB WITH FORM VALUE RESULTS
	results = search_score(search_name, search_pwd)
	print results

	search = str(request.form['search'])


	custom = Style(
		background='black',
		plot_background='black',
		colors=('#7ecc72', '#56a9a7', '#d42d2d'),
		foreground='white',
	  	foreground_strong='white',
	  	foreground_subtle='white',

		)
	times = []
	scores_easy = []
	scores_med = []
	scores_hard = []
	for li in results:
		times.append(str(li[2].replace('u', '').replace("'", '')))
		if 'Easy' in li:
			scores_easy.append(li[0])
		elif 'Medium' in li:
			scores_med.append(li[0])
		else:
			scores_hard.append(li[0])
	line_chart = pygal.Line(style=custom)
	line_chart.title = None
	line_chart.x_labels = None
	line_chart.add('Easy', scores_easy)
	line_chart.add('Medium', scores_med)
	line_chart.add('Hard', scores_hard)
	chart = line_chart.render_data_uri()


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
	if len(high_easy) >= 1:
		hi_easy = max(high_easy)
	else:
		hi_easy = 0
	if len(high_med) >= 1:
		hi_med = max(high_med)
	else:
		hi_med = 0
	if len(high_hard) >= 1:
		hi_hard = max(high_hard)
	else:
		hi_hard = 0
	
	return render_template('results.html', search = search, final_results_easy = final_results_easy, final_results_med = final_results_med, final_results_hard = final_results_hard, hi_easy = hi_easy, hi_med = hi_med, hi_hard = hi_hard, chart = chart)


