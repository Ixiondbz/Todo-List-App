import re
from werkzeug.utils import redirect
from app import app,db
from flask import render_template,request
from models import Task

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        if request.form['content'] is not "":
            task_content = request.form['content']
        else:
            return redirect('/')
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'Error posting task'

    else:
        TASKS=Task.query.order_by(Task.dateCreated).all()
        return render_template('home.html', title='Home Page',tasks=TASKS)


@app.route('/delete/<int:ID>')
def delete(ID):
    task_to_delete = Task.query.get(ID)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Error deleting task'

@app.route('/update/<int:ID>', methods=['GET','POST'])
def update(ID):
    task = Task.query.get(ID)

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating task"

    else:
        return render_template('update.html',task=task)
