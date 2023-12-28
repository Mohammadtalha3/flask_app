from typing import Any
from flask import make_response,request
from jwt.exceptions import DecodeError
from config.config import db_data 
from functools import wraps
import json
import mysql.connector
import sys
import re
import jwt
class Auth_model():
    def __init__(self):
        try:
            self.conn=mysql.connector.connect(host='localhost', user='root',password='mysql',database='flaskdb')
            self.conn.autocommit=True
            self.mycursor= self.conn.cursor(dictionary=True)
        except:
            print("Cannot made  connection to Database:")
            
        else:
            print('Connection to Database  been made: ')
            

    
    def token_Auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            
            def inner2(*args):
                endpoint= request.url_rule
                print(endpoint)
                authorization= request.headers.get('Authorization')
                if re.match('^Bearer *([^ ]+) *$', authorization, flags=0):
                    token=authorization.split(" ")[1]
                    
                    
                    
                    print(token)
                    try:
                        jwtdecoded=jwt.decode(token, 'talha', algorithms='HS256')
                        
                    except jwt.ExpiredSignatureError:
                        return make_response({'ERROR':'Token expired'}, 401)
                    roleid= jwtdecoded['payload']['role_id']
                    self.mycursor.execute(f"SELECT roles FROM accessebilty_ciew WHERE  endpoint= '{endpoint}' ")
                    result=self.mycursor.fetchall()
                    if len(result)>0:
                        roles_allowed=json.loads(result[0]['roles'])
                        if roleid in roles_allowed:

                            return func(*args)
                        else:
                            return make_response({"Error":'No roles Found'},404)

                    else:
                        return make_response({'ERROR': "No  Results"}, 404)

                    
                else:
                    return make_response({'Error': 'Invalid Token '}, 401)
                
            return inner2
        return inner1
    

    



