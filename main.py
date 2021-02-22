from flask import Flask, request, make_response, jsonify
import uuid
import jwt
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import jwt_validation, db_tasks



JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    userName = req_data["user"]
    userPwd = req_data["password"]

    sqlcommand = "SELECT user_id, user_password FROM users WHERE user_name=?"
    searchValues = (userName,)

    fetchedUserDetails = db_tasks.findDbRecords(sqlcommand, searchValues)

    storedPwd = fetchedUserDetails[1]
    fetchedUserId = fetchedUserDetails[0]

    try:
        pwdMatch = sha256_crypt.verify(userPwd, storedPwd)

        if pwdMatch is True:
            newTokenId = uuid.uuid4()
            TokenExpiration = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            newTokenPayload = {"user": userName,
                               "userId": fetchedUserId,
                               "tokenID" : str(newTokenId),
                               "exp" : TokenExpiration
                               }
            newToken = jwt.encode(newTokenPayload, JWT_SECRET, JWT_ALGORITHM).decode('utf-8')

            sqlcommand = "INSERT INTO tokens (token_id, user_id) VALUES(?,?)"
            newDbRecord = (str(newTokenId),fetchedUserId)
            db_tasks.createNewDbRecord(sqlcommand,newDbRecord)
            responsePayload = {
                "user" : userName,
                "user_Id" : fetchedUserId,
                "token_ID" : newTokenId,
                "auth_token" : str(newToken),
                "passwordMatch" : pwdMatch
                           }
            responseMsg = make_response(responsePayload, 200)
            responseMsg.headers["Content-Type"] = "application/json"
        else:
            responseMsg = make_response('Incorrect password',401)
    except:
        responseMsg = make_response('You need to specify the user name and the password', 400)
    return responseMsg

@app.route('/logout', methods=['POST'])
def logout():
    request_toq = request.headers["Authorization"][7:]
    tokenValidation = jwt_validation.validateToken(request_toq)
    if tokenValidation['validation']:
        db_tasks.tokenLogOut(tokenValidation["token"])
        responseMsg = make_response("Logged Out.", 200)
    else:
        responseMsg = make_response("Authorization failed", 400)
    return responseMsg

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        req_data = request.get_json()
        userName = req_data["userName"]

        sqlcommand = "SELECT user_id FROM users where user_name=?"
        searchValues = (userName,)
        if db_tasks.findDbRecords(sqlcommand,searchValues) is None:
            userExists = False
        else:
            userExists = True

        if not userExists:
            userEmail = req_data["userEmail"]
            userPwd = req_data["password"]
            NewUserPwd = sha256_crypt.encrypt(userPwd)
            newUserId = uuid.uuid4()
            welcomeMsg = 'Hello new user ' + userName + '. Your new user ID is ' + str(
            newUserId) + '. An email has been sent to the address ' + userEmail + '. The hashed password is ' + NewUserPwd + ';-)'
            responseMsg = make_response(welcomeMsg, 201)
            newDbRecord = (str(newUserId),userName,userEmail,NewUserPwd)
            sql_command = "INSERT INTO users (user_id,user_name,user_email,user_password) VALUES (?,?,?,?)"
            db_tasks.createNewDbRecord(sql_command,newDbRecord)
        else:
            responseMsg = make_response('User name already exists',409)
            # responseMsg = make_response('You need to specify all user details',400)

        return responseMsg
    else:
        return 'User details'

@app.route('/mealplans', methods=['GET'])
def weekly_plans():
    req_data = request.get_json()
    request_toq = request.headers["Authorization"][7:]
    tokenValidation = jwt_validation.validateToken(request_toq)
    if tokenValidation['validation']:
        responseMsg = make_response(req_data,200)
    else:
        responseMsg = make_response("Authorization failed", 400)
    return responseMsg

@app.route('/meals', methods=['GET'])
def meals():
    request_toq = request.headers["Authorization"][7:]
    tokenValidation = jwt_validation.validateToken(request_toq)
    if tokenValidation['validation']:
        sqlcommand = "SELECT * FROM meals"
        searchvalues = ""
        foundRecords = db_tasks.findAllDbRecords(sqlcommand,searchvalues)
        response = jsonify(foundRecords)

        responseMsg = make_response(response, 200)
    else:
        responseMsg = make_response("Authorization failed", 400)
    return responseMsg


if __name__ == '__main__':
    app.run(debug=True)