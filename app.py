from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///farneet.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    #This is a class, we will use this template to make the To-do list
    sno = db.Column(db.Integer, primary_key = True)
    title =  db.Column(db.String(200), nullable = False)
    desc =  db.Column(db.String(500), nullable = False)
    date_created =  db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return (f"{self.sno} - {self.title}")


# The index function is just for understanding, in items() we will try add the text entered by the user in the to do list.
# def index():
#     if request.method == 'POST':
#         print(request.form['title']) # We would like to get the information that user entered, we will call the name attribute of the form
#         print(request.form['desc'])
#     todo = Todo(title = "First Todo item", desc = "Invest in the Stark industries")
#     db.session.add(todo)
#     db.session.commit()
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return render_template('index.html', allTodo=allTodo)

@app.route('/', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        title = (request.form['title']) # We would like to get the information that user entered, we will call the name attribute of the form
        description = (request.form['desc'])
        todo = Todo(title = title , desc = description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



# Now lets see an another example query.all()
# @app.route('/show')
# def printtodo():
#     print(Todo.query.all()) # I think it collects all the todos queries
#     return 'This is printtodo bitch'


# Lets make the functions to delete and update the information in the databases
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = (request.form['title']) 
        description = (request.form['desc'])
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo);


@app.route('/delete/<int:sno>') #We will delete the specific serial number

def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)


# If we want the queries to be shown on the website instead of the file, we need to add something to the index.html