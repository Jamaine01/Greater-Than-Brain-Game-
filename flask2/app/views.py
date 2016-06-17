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
