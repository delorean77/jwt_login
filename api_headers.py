from flask import Flask, request, make_response
import jwt

JWT_SECRET = 'secret'

app = Flask(__name__)

@app.route('/')
def hello_world():
    req_token = request.headers["Authorization"][7:]
    try:
        validated_token = jwt.decode(req_token, JWT_SECRET)
        response = validated_token
    except:
        response = "Something went wrong"
    return response


app.run()