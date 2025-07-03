from flask import Flask, render_template, request, redirect, url_for;
from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # ? /// indicates a relative path, //// indicates an absolute path
db = SQLAlchemy(app)
# ? Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy, a powerful ORM (Object Relational Mapper) for Python.
# ? Flask is a micro web framework for Python, and it allows you to build web applications easily.

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self): # ? __repr__ is a special method in Python that defines how an object is represented as a string.
        return f'Todo({self.title}, {self.completed})'

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        task_title = request.form.get('title')
        print(task_title)
        new_todo = Todo(title=task_title)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error adding todo: {e}")
            return redirect(url_for('index'))
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# ? python app.py
