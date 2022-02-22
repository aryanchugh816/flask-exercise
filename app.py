from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db
import mockdb.dummy_data as users
app = Flask(__name__)


def create_response(
    data = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is None:
        raise TypeError("Data should be a dictionary 😞")
    # print(users.initial_db_state)
    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.get("/users")
def show_users():
    data = db.get("users")
    return create_response(data)
    
@app.get("/users/<id>")
def show_user(id):
    data = db.getById("users",int(id))
    if data is not None:
        return create_response(data)
    
    return {"message":"No user found","status":404}

@app.route("/users/teams")
def show_user_based_on_team():
    team  = request.args.get('team', None)
    data = db.get("users")
    temp = []
    for user in data:
        if(user["team"] == team):
            temp.append(user)
    print(temp)
    return create_response(temp)
            
@app.route('/users/createuser', methods = ['POST'])
def createuser():
   data  = request.json
   print(data)
   return create_response(db.create("users",data))


@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    if(db.getById("users",int(id)) is not None):
        db.deleteById("users",int(id))
        return {"status": 200, "message": "User Deleted Sucessfully"}
    
    return ({"status": 404, "message":"user not found"})

@app.route('/users/<id>', methods=['PUT'])
def update(id):
    if(db.updateById("users",int(id),request.json)):
        return create_response({"message": "User Updated"})
    
    return ({"status": 404, "message":"user not found"})

# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
