import os
from flask import Flask, url_for, redirect, flash, render_template,request
from flask_sqlalchemy import SQLAlchemy 

# instantiating flask
app = Flask(__name__)

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SECRET_KEY'] = 'KLOJOIKLkhkljkl'

db = SQLAlchemy(app)

# Creating Todo table
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String, nullable=False)
	task_time = db.Column(db.String)

	def __init__(self, task, task_time):
		self.task = task 
		self.task_time = task_time

	def __repr__(self):
		return "<Task> %r"% self.task

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'] )
def add_item():
	if request.method == 'POST':
		if not request.form['task'] or not request.form['task_time']:
			flash("You cant have an empty task")
		else:
			task = Todo(request.form['task'], request.form['task_time'])
			db.session.add(task)
			db.session.commit()
			flash("Successfully added an Item")
			return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/display')
def display():
	return render_template('index.html', todos=Todo.query.all())


if __name__ == '__main__':
	app.run(debug=True)
	db.create_all()