import jwt
import db_tasks
from datetime import datetime, timedelta

# invalidToken = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlck5hbWUiLCJleHAiOjE2MDkxNjk1OTZ9.Hv-cruCUldN5LtlH-mus0niByxHTFgfllWLck_t3QhM'
# invalidToken1 = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibHVjaW5vIiwidG9rZW5JRCI6ImNlMWFiMGQyLWE4NDQtNGE1MS05NzYzLTJhY2M3OWQ4NGNhMiIsImV4cCI6MTYwOTE3MzE3Mn0.BX7JbJymvZTW7X28pjaA9vgltMYyXqIdH6yPC7Y0Tmg'
#
# token2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiT2Npbm8yIiwidXNlcklkIjoiNDA0ZWE5ZDYtMDEzMi00ZWJjLWI4ZjQtNGUxOTRkYmU4ZjNiIiwidG9rZW5JRCI6IjM2MWU4YzdiLTk5MDYtNDhkNy04ZDBkLWYxODZhZWI3Y2VkMSIsImV4cCI6MTYxMDAwMDk4Nn0.ZtPbBrBa5xsHKE2tacCIkVhu7qO4dlpix3vq3P1lPJg"
# token3 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiT2Npbm8yIiwidXNlcklkIjoiNDA0ZWE5ZDYtMDEzMi00ZWJjLWI4ZjQtNGUxOTRkYmU4ZjNiIiwidG9rZW5JRCI6IjM2MWU4YzdiLTk5MDYtNDhkNy04ZDBkLWYxODZhZWI3Y2VkMSIsImV4cCI6MTYxMDAwMDk4Nn0.ZtPbBrBa5xsHKE2tacCIkVhu7qO4dlpix3vq3P1lPJg"
#
JWT_SECRET = 'secret'


# JWT_ALGORITHM = 'HS256'
# JWT_EXP_DELTA_SECONDS = 60

# TokenExpiration = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
# newTokenPayload = {
#     "user": "userName",
#      "exp" : TokenExpiration
#                 }
# newToken = jwt.encode(newTokenPayload, JWT_SECRET, JWT_ALGORITHM)

# print(newToken)
# print()
#
# decodedToken = jwt.decode(newToken,JWT_SECRET)
#
# print(decodedToken)
def validateToken(tokenToValidate):
    try:
        decodedToken = jwt.decode(tokenToValidate, JWT_SECRET)
        decodedTokenID=decodedToken["tokenID"]
        tokenLoginStatus = db_tasks.findLoginStatus(decodedTokenID)
        if tokenLoginStatus == "LoggedIn":
            validatedToken = {"validation": True, "token": decodedToken["tokenID"]}
        elif tokenLoginStatus == "LoggedOut":
            validatedToken = {"validation": False, "token": decodedToken["tokenID"]}
        else:
            validatedToken = {"validation": False, "token": "Token does not exist."}
    except jwt.exceptions.ExpiredSignatureError:
        decodedToken = jwt.decode(tokenToValidate, JWT_SECRET, options={"verify_exp": False})
        validatedToken = {"validation": False, "token": decodedToken["tokenID"]}
    except:
        validatedToken = {"validation": False, "token": "Error"}

    return validatedToken

    # try:
    #     print(tokenToValidate)
    #     decodedToken = jwt.decode(tokenToValidate, JWT_SECRET)
    #     tokenLoginStatus = db_tasks.findLoginStatus(decodedToken["token_ID"])
    #     if tokenLoginStatus == "LoggedIn":
    #         validatedToken = {"validation": True, "token": decodedToken}
    #     elif tokenLoginStatus == "LoggedOut":
    #         validatedToken = {"validation": False, "token": decodedToken}
    #     else:
    #         validatedToken = {"validation": False, "token": "Token does not exist."}
    # except jwt.exceptions.ExpiredSignatureError:
    #     decodedToken = jwt.decode(token, JWT_SECRET, options={"verify_exp": False})
    #     validatedToken = {"validation": False, "token": decodedToken}
    # except:
    #     validatedToken = {"validation": False, "token": "Error"}

    # return validatedToken





# token3 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiT2Npbm8yIiwidXNlcklkIjoiNDA0ZWE5ZDYtMDEzMi00ZWJjLWI4ZjQtNGUxOTRkYmU4ZjNiIiwidG9rZW5JRCI6IjcwNGE1ODNjLTM3NGYtNGFhNy05YzM3LTBkMDgzMzE0ZmY2MyIsImV4cCI6MTYxMDA5OTg1NH0.nyZEu4m2kHSHQimMakqb9X0ko22RkUzjwwYosV-R4lI"
# print(validateToken(token3))
# decoded = jwt.decode(token3, JWT_SECRET)
# print(decoded)
# print(validate2(token3))
