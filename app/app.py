from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

#app = Flask(__name__)
app=Flask(__name__, template_folder='../templates')

# Absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "project.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Taskflow model
class Tasks(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    Desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Home route
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
       
       title=request.form['title']
       Desc=request.form['Desc']
       tasks = Tasks(title=title, Desc=Desc)
       db.session.add(tasks)
       db.session.commit()
    
    allTasks = Tasks.query.all()
    return render_template("index.html", allTasks=allTasks)
    
       
    
@app.route('/show')
def show():
    allTasks=Tasks.query.all()
    print(allTasks)
    return"this is show page"

# @app.route('/update/<int:sno>', methods=['GET', 'POST'])
# def update(sno):
#     if request.method=="POST":
#         title=request.form['title']
#         Desc=request.form['Desc']
#         todo=Todo.query.filter_by(sno=sno).first()
#         todo.title=title
#         todo.desc=Desc
#         db.session.add(todo)
#         db.session.commit()
#         return redirect("/")
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    tasks = Tasks.query.filter_by(sno=sno).first()
    
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['Desc']  # usually lowercase for consistency
        
        tasks.title = title
        tasks.Desc = desc
        
        db.session.commit()  # no need for db.session.add(todo), since it's already in the session
        return redirect("/")
    
    # For GET request: render the update form with the current data
    return render_template('update.html', tasks=tasks)

    
    # todo=Todo.query.filter_by(sno=sno).first()
    # return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    tasks=Tasks.query.filter_by(sno=sno).first()
    db.session.delete(tasks)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print('tables created successfully!')
    app.run(debug=True, port=9000)
