import mysql.connector
import sys
import json
from datetime import datetime, timedelta
from config.config import db_data
from flask import make_response
import jwt

class user_model():

    def __init__(self):
        try:
            self.conn=mysql.connector.connect(host=db_data['host'], user=db_data['user'],password=db_data['password'],database=db_data['database'])
            self.conn.autocommit=True
            self.mycursor= self.conn.cursor(dictionary=True) 
        except:
            print("connection to database cannot be made")
            sys.exit(0)
        else:
            print("connection to database is made")

        
    def user_getall(self):
        self.mycursor.execute("SELECT * FROM users")
        response=self.mycursor.fetchall()
        if len(response)>0:
            res=make_response({'payload': response},200)
            res.headers['Access-Control-Allow-Origin']= "*"
            return  res
        else:
            return make_response({'message': "No Data found"},204)
    
    def user_addone(self,data):
        self.mycursor.execute(f"INSERT INTO users (name,email,phone,role_id,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role_id']}','{data['password']}')")
        return make_response({'message':"user created successfuly"},201)
    
    def multiuser_add(self, data):
        query= "INSERT INTO users (name,email,phone,role_id,password) VALUES"
        for userdata in data:
            query += f"('{userdata['name']}','{userdata['email']}','{userdata['phone']}',{userdata['role_id']},'{userdata['password']}'),"
        f_query= query.rstrip(',')
        self.mycursor.execute(f_query)
        return make_response({'messages':'Multipleuser created successfully'}, 401)
    
    def user_update(self,data):
        self.mycursor.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}',phone='{data['phone']}',role_id='{data['role_id']}',password='{data['password']}' WHERE id= {data['id']}")
        if self.mycursor.rowcount>0:
            return make_response({'message':"user updated"},201)
        else:
            return make_response({'message':'Nothing to update'},202)    

    def user_delete(self,id):
        self.mycursor.execute(f"DELETE FROM  users WHERE id={id}") 
        if self.mycursor.rowcount>0:
            return make_response({'message':"User deleted succesfully"},200)
        else:
            return make_response({'message':"Noting to delete"},202)
    
    
    def user_patch(self,data,id):

        qry= "UPDATE users SET "
        for key in data:
            qry+= f"{key}='{data[key]}',"
        qry= qry[:-1] + f' WHERE id={id}'
        
        self.mycursor.execute(qry)
        if self.mycursor.rowcount>0:
            return make_response({'message': 'Updated Successfully'},200)
        else:
            return make_response({'message':'Nothing to update' },202)
    

    def user_pagination(self,limit,page):
        limit=int(limit)
        page=int(page)
        start= (page*limit)-limit
        qry= f"SELECT * FROM users LIMIT {start}, {limit}"
        self.mycursor.execute(qry)
        response=self.mycursor.fetchall()
        if len(response)>0:
            res=make_response({'payload': response,'page_no': page, 'limit': limit},200)
            return  res
        else:
            return make_response({'message': "No Data found"},204)
    
    def user_upload_avatar_model(self,uid,filepath):
        self.mycursor.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")

        if self.mycursor.rowcount>0:
            return make_response({'message':'avatar uploaded succesfully'}, 201)
        else:
            return  make_response({'message':'Nothing to update'},202)
        
    
    def user_login_model(self,data):
        self.mycursor.execute(f"SELECT id,name,email,phone,avatar,role_id FROM users WHERE email='{data['email']}' AND password='{data['password']}'"  )
        result  =self.mycursor.fetchall()
        user_data= result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time= int(exp_time.timestamp())
        payload={
            'payload': user_data,
            'exp': exp_epoch_time
        }
        jwt_token=jwt.encode(payload,'talha', algorithm='HS256')
        print(jwt_token)
        return make_response({'token': jwt_token}, 200)
    

        


        