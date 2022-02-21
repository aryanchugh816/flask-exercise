from typing import Tuple

from flask import Flask, jsonify, request, Response
# import mockdb.mockdb_interface as db
import mockdb.dummy_data as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
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
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

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


@app.route('/users',methods = ['GET','POST'])
def users():
    users = db.initial_db_state
    return create_response(users)


@app.route("/users/<id>",methods = ['GET','POST'])
def users2(id):
    users = db.initial_db_state
    data={}
    for i in users['users']:

        if i["id"]==int(id):
            data=i

            return create_response(i)
    return create_response({"status": 404, "message":"id not present"})


#post request
@app.route("/adddata",methods = ['POST'])
def adddata():
    data=request.json
    if data['id'] and data['age'] and data['team'] and data['name']:
        db.initial_db_state['users'].append(data)
        return create_response(data)
    else:
        return create_response({"status": 422, "message":"please fill all the feilds"})

@app.route("/updatedata/<id>",methods = ['PUT'])
def updatedata(id):
    data=request.json
    # print(data)
    users = db.initial_db_state['users']
    foo=0
    for i in users:

        if i["id"]==int(id):
            i["age"]=data["age"]
            i["name"]=data["name"]
            i["team"]=data["team"]
            foo=1
            break
    if foo==0:
        return create_response({"status": 404, "message":"id not present"})
    else:
        return create_response(data)


@app.route("/deletedata/<id>",methods = ['DELETE'])
def deletedata(id):
    users = db.initial_db_state
    foo=0
    ind=-1
    for i in range(len(users['users'])):
        if users['users'][i]["id"]==int(id):
            ind=i
            foo=1
            break
    if ind!=-1:
        users['users'].pop(ind)
        return create_response({"content": 'delete successfully'})
    else:
        return create_response({"status": 404, "message":"id not present"})



# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
