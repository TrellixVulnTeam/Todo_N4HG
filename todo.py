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
	todos = Todo.query.all()
	return render_template('index.html', todos)

@app.route('/add_item', methods=['GET', 'POST'] )
def add_item():
	if request.method == 'POST':
		if not request.form['task'] or not request.form['task_time']:
			flash("You cant have an empty task")
			return redirect(url_for('index'))
		else:
			task = Todo(request.form['task'], request.form['task_time'])
			db.session.add(task)
			db.session.commit()
			flash("Successfully added an Item")
			return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	if request.method == 'GET':
		data = Todo.query.filter_by(id=Todo.id).first_or_404()
		db.session.delete(data)
		db.session.commit()
	return redirect(url_for('index'))

# @app.route('/edit/<int:id>', methods['GET', 'POST'])
# def edit(id):
# 	if request.method == 'POST':
# 		if not request.form['task'] or not request.form['task_time']:
# 			flash("You cant leave a blank task")
# 		else:
# 			task = Todo()





if __name__ == '__main__':
	app.run(debug=True)
	db.create_all()
