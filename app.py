from typing import Tuple
from unicodedata import name

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@database:5432/users_db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UsersModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    team = db.Column(db.String())

    def __init__(self,id,name,age,team) -> None:
        self.name = name
        self.age = age
        self.id = id
        self.team = team
    

"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return ({"content": "hello world!"})


@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = UsersModel(name=data['name'], age=data['age'], team=data['team'], id=data['id'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        users = UsersModel.query.all()
        results = [
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "team": user.name
            } for user in users]

        return {"count": len(results), "users": results}

    
@app.route("/users/<id>", methods=['GET'])
def show_user(id):
    data = UsersModel.query.all()
    print(data[0].id)
    for user in data:
        if(user.id == int(id)):
             result = [
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "team": user.team
            }
             ]
             return {"user": result}
    
        
    
    return {"message":"No user found","status":404}

# @app.route("/users/teams")
# def show_user_based_on_team():
#     team  = request.args.get('team', None)
#     data = db.get("users")
#     temp = []
#     for user in data:
#         if(user["team"] == team):
#             temp.append(user)
#     print(temp)
#     return create_response(temp)
            
# @app.route('/users/createuser', methods = ['POST'])
# def createuser():
#    data  = request.json
#    print(data)
#    return create_response(db.create("users",data))


# @app.route('/users/<id>', methods=['DELETE'])
# def delete(id):
#     if(db.getById("users",int(id)) is not None):
#         db.deleteById("users",int(id))
#         return {"status": 200, "message": "User Deleted Sucessfully"}
    
#     return ({"status": 404, "message":"user not found"})

# @app.route('/users/<id>', methods=['PUT'])
# def update(id):
#     if(db.updateById("users",int(id),request.json)):
#         return create_response({"message": "User Updated"})
    
#     return ({"status": 404, "message":"user not found"})

# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
