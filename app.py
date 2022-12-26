from flask import Flask ,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime  import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db"
# db= SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()



        #test code
class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    desc = db.Column ( db.String(500),nullable = False)
    date_create = db.Column( db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        # return super().__repr__()
        return f"{self.sn}-{self.title}"

@app.route('/', methods= ['GET','POST'])
def main():
    if request.method == 'POST':
        title = ( request.form['title'])
        desc = ( request.form['desc'])
        if len(title)>1:
            todo = Todo(title =title, desc = desc )
            db.session.add(todo)
            db.session.commit()
    all_todo = Todo.query.all()
    return  render_template ( 'index.html', all_todo = all_todo)

@app.route('/update/<int:sn>', methods = ['GET','POST'])
def update (sn):
    if request.method =='POST':
        title = request.form['title']
        desc =  request.form['desc']
        todo = Todo.query.filter_by(sn = sn).first()
        todo.title = title 
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect ('/')   
    todo = Todo.query.filter_by(sn = sn).first()
    return render_template ('update.html', todo = todo) 

    # if request.method == 'POST':
    #     # db.session.delete(todo)
    #     # title = request.form['title']
    #     # desc =  request.form['desc']
    #     # todo = Todo.query.filter_by(sn = sn).first()
    #     todo.title = request.form['title'] 
    #     todo.desc = request.form['desc']
    #     # db.session.add(todo)
    #     todo.verified = True
    #     db.session.commit()
    #     return redirect ('/')
 


@app.route('/delete/<int:sn>')
def delete (sn): 
    todo = Todo.query.filter_by(sn = sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/')


if __name__ =='__main__':
    app.run(debug = True, port=80)


