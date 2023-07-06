from flask import Flask,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.secret_key = "super secret key"
app.app_context().push()
# uri used to connect to the db.. sqlite here
# these are configuration keys
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
     
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    error = ''
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        
        if title == '' or desc == '':
            flash('Error: Title and Description cannot be empty')
            # error = 'Please fill the title and description'
            return redirect('/')
            # print("error")
        else:
            flash('Successfully added')
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
    alltodos = Todo.query.all()
    
    return render_template('index.html',alltodos=alltodos,error=error)


@app.route('/show')
def show():
    alltodos = Todo.query.all()
    print(alltodos)
    return 'show fn working check terminal'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')    
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',update_todo=todo)

@app.route('/delete/<int:sno1>')
def delete(sno1):
    delete_todo = Todo.query.filter_by(sno=sno1).first()
    print(delete_todo)
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)