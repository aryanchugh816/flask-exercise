from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db
# import mockdb.dummy_data as db

app = Flask(__name__)


def create_response(
    data= None, status: int = 200, message: str = ""
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


@app.route('/users',methods = ['GET'])
def users():
    users=db.get('users')
    # print(users)
    # users = db.initial_db_state
    return create_response(users)


@app.route("/users/<id>",methods = ['GET'])
def users2(id):
    users=db.get('users')
    # users = db.initial_db_state
    data={}
    # print(users)
    res=db.getById('users', int(id))
    # for i in users:

    #     if i["id"]==int(id):
    #         data=i

    #         return create_response(i)
    # return create_response({"status": 404, "message":"id not present"})
    if res:
        return create_response(res)
    return create_response({"status": 404, "message":"id not present"})

@app.route("/fnd",methods = ['GET'])
def fnd():
    team  = request.args.get('team', None)
    users=db.get('users')
    temp = []
    for user in users:
        if(user["team"] == team):
            temp.append(user)
    return create_response(temp)





#post request
@app.route("/adddata",methods = ['POST'])
def adddata():
    data=request.json
    res=db.create('users', data)
    if res:
        return create_response(res)
    # data=request.json
    # if data['id'] and data['age'] and data['team'] and data['name']:
    #     db.initial_db_state['users'].append(data)
    #     return create_response(data)
    else:
        return create_response({"status": 422, "message":"please fill all the feilds"})

@app.route("/updatedata/<id>",methods = ['PUT'])
def updatedata(id):
    data=request.json
    res=db.updateById('users', int(id), data)
    if res:
        return create_response(res)
    # print(data)
    # users = db.initial_db_state['users']
    # foo=0
    # for i in users:

    #     if i["id"]==int(id):
    #         i["age"]=data["age"]
    #         i["name"]=data["name"]
    #         i["team"]=data["team"]
    #         foo=1
    #         break
    else:
        return {"status": 404, "message":"id not present"}
    # else:
    #     return create_response(data)


@app.route("/deletedata/<id>",methods = ['DELETE'])
def deletedata(id):
    # users = db.initial_db_state
    res=db.deleteById('users', int(id))
    return create_response({"status": 404, "message":res})
    # foo=0
    # ind=-1
    # for i in range(len(users['users'])):
    #     if users['users'][i]["id"]==int(id):
    #         ind=i
    #         foo=1
    #         break
    # if ind!=-1:
    #     users['users'].pop(ind)
    #     return create_response({"content": 'delete successfully'})
    # else:
    #     return create_response({"status": 404, "message":"id not present"})

# TODO: Implement the rest of the API here

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
