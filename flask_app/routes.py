# Author: Harshit Kandpal <hkandpal944@gmail.com>
from flask import current_app as app, send_from_directory
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
	@functools.wraps(func)
	def secure_function(*args, **kwargs):
		if "email" not in session:
			return redirect(url_for("login", next=request.url))
		return func(*args, **kwargs)
	return secure_function

def getUser():
	return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	status = db.authenticate(form_fields['email'], form_fields['password'])
	
	if 'success' in status:
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
	
	return json.dumps(status)

@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/processregister', methods=["POST", "GET"])
def processregister():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	status = db.notExists('users', 'email', form_fields['email'])

	if 'success' in status:
		db.createUser(form_fields['email'], form_fields['password'])

	return json.dumps(status)

#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
	return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(content):
	join_room('main')
	user = getUser()

	if db.isOwner(user):
		emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'color:grey;'}, room='main')


@socketio.on('message', namespace='/chat')
def message(content):
	user = getUser()

	if db.isOwner(user):
		emit('messaged', {'msg': content['content'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('messaged', {'msg': content['content'], 'style': 'color:grey;'}, room='main')

@socketio.on('leave', namespace='/chat')
def leave(content):
	leave_room('main')
	user = getUser()

	if db.isOwner(user):
		emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': getUser() + ' has left the room.', 'style': 'color:grey;'}, room='main')

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x = random.choice(["I study software development and have worked in IT Support and Wireless Testing, so whether it's debugging code, fixing tech issues, or testing signals, I've probably done it.",
					   "I'm powered by curiosity. If something breaks, I need to know why—it’s a personality trait at this point.",
					   "I build across platforms—from full stack web apps to Android mobile experiences."])
	return render_template('home.html', user=getUser(), fun_fact = x)

@app.route('/projects')
def projects():
	return render_template('projects.html', user=getUser())

@app.route('/piano')
def piano():
	return render_template('piano.html', user=getUser())

@app.route("/static/<path:path>")
def static_dir(path):
	return send_from_directory("static", path)

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "public, max-age=3600"
	return r
