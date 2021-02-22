import sqlite3


# conn = sqlite3.connect('db/users.db')
# c = conn.cursor()
#
# userName = ('Ocino5',)
#
#
# # c.execute("INSERT INTO users (user_id,user_name,user_email,user_password) VALUES (?,?,?,?)",("88888815","ocino1","email@email.com","asbd"))
# # sqlcommand = "SELECT user_id, user_password FROM users WHERE user_name=?"
# sqlcommand = "UPDATE tokens SET logged_out = ? where token_id = ?"
# newDbRecord = (True, "abc123")
# # newDbRecord = userName
# c.execute(sqlcommand, newDbRecord)
# # print(c.fetchone())
# c.close()

# c.execute('SELECT user_id, user_password FROM users WHERE user_name=?', userName)
# result = c.fetchone()
# userId = result[0]
# userPwd = result[1]
# print (userId)
# print (userPwd)

# c.execute('INSERT INTO tokens (token_id, user_id) VALUES (?,?)',('assa235', 'sdksla888'))

# c.execute("SELECT * FROM users WHERE user_name='Jano'")
# print(c.fetchone())

# conn.commit()
# conn.close()
def openDB():
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    return c


def findLoginStatus(tokenID):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    sqlcommand = "SELECT logged_out FROM tokens WHERE token_id=?"
    searchValue = (tokenID,)
    c.execute(sqlcommand, searchValue)
    loginInfo = c.fetchone()
    if loginInfo is None:
        returnedLoginStatus = "NoToken"
    elif loginInfo[0] == "False":
        returnedLoginStatus = "LoggedIn"
    else:
        returnedLoginStatus = "LoggedOut"
    return returnedLoginStatus

def tokenLogOut(tokenID):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    sql_command = 'UPDATE tokens SET logged_out = ? WHERE token_id = ?'
    tokenUpdateValues = (True, tokenID)
    c.execute(sql_command, tokenUpdateValues)
    conn.commit()
    conn.close()
    return

def createNewDbRecord(sql_command,newDbRecord):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute(sql_command, newDbRecord)
    conn.commit()
    conn.close()
    return

def findDbRecords(sqlcommand, searchValues):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute(sqlcommand,searchValues)
    fetchedDetails = c.fetchone()
    conn.close()
    return fetchedDetails

def findAllDbRecords(sqlcommand, searchValues):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute(sqlcommand,searchValues)
    fetchedDetails = c.fetchall()
    conn.close()
    return fetchedDetails

# test = findLoginStatus('ae39cd72-7a6e-4e57-9dbb-547e6149c3e4')
# print(test)
# test = tokenLogOut("assa235")
