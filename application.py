from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

from sqlalchemy import true

application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)
ma = Marshmallow(application)

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(300), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TodoListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date_created')


# instantiate schema objects for todolist and todolists
todolist_schema = TodoListSchema(many=False)
todolists_schema = TodoListSchema(many=True)

@application.route('/todolist',methods=["POST"])
def create_task():
    try:
        title = request.json['title']
        description = request.json['description']

        new_todo = TodoList(title = title,description = description)

        db.session.add(new_todo)
        db.session.commit()

        return todolist_schema.jsonify(new_todo)

    except Exception as e:
        return jsonify({"Error" : "Invalid Request"})

@application.route('/')
def get_tasks():
    todos = TodoList.query.all()
    result_set = todolists_schema.dump(todos)
    return jsonify(result_set)


@application.route('/todolist/<int:id>',methods=["PUT"])
def update_task(id):
    todo = TodoList.query.get_or_404(int(id))
    try:
        title = request.json['title']
        description = request.json['description']

        todo.title = title
        todo.description = description

        db.session.commit()
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})
        
    return todolist_schema.jsonify(todo)



@application.route("/todolist/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"Success" : "Todo deleted."})


if __name__ == "__main__":
    application.run(debug=true,port=8080)


