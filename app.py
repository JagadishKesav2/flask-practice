from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration of SQL Lite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# End of SQL Lite Database Configuration

# Database Model Creation
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
# End of Database Model Creation

# Render HTML Template with the help of Route
@app.route('/')
def index():
    # Show all todo items
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list = todo_list)
# End of HTML Template

# Add New Item
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))
# End of New Item

# Delete Item
@app.route('/delete/<int:id>')
def delete(id):
    id = Todo.query.filter_by(id=id).first()
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for("index"))
# End of Delete Item

# Basic Routes without HTML Template
@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello, {name}</h1>'

@app.route('/<int:urlname>')
def hello_world(urlname):
    return f'<h1>Hello, World {urlname}</h1>'
# End of Route

# Main Function
if __name__ == '__main__':
    # Create all Query
    db.create_all()
    # End of Query
    app.run(debug=True)