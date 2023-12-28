from app import app
from model.user_model import user_model 
from flask import request,send_file
from datetime import datetime
from model.Authentication import Auth_model
auth= Auth_model()
obj= user_model()

@app.route('/user/getall')
@auth.token_Auth()
def user_signup_controller():
    return obj.user_getall()

@app.route('/user/add', methods=["POST"])
@auth.token_Auth()
def addone():
    
    return obj.user_addone(request.form)

@app.route('/multiuser/add', methods=["POST"])
def multiuser():

    print(request.json)
    
    return obj.multiuser_add(request.json)

@app.route('/user/update', methods=['PUT'])
def update():
    return obj.user_update(request.form)

@app.route('/user/delete/<id>', methods=['DELETE'])
def delt(id):
    return obj.user_delete(id)

@app.route('/user/patch/<id>', methods=['PATCH'])
def patch(id):
    return obj.user_patch(request.form, id)

@app.route('/user/getall/limit/<limit>/page/<page>',methods=['GET'])
def pagination(limit,page):
    return obj.user_pagination(limit,page)

@app.route('/user/<uid>/upload/avatar',methods=['PUT'])
def user_upload_avatar_controller(uid):


    file=(request.files['avatar'])
    unique_filename=str(datetime.now().timestamp()).replace(".","")
    splitfile=file.filename.split('.')
    extension=splitfile[len(splitfile)-1]
    final_file_path= f"uploads/{unique_filename}.{extension}"
    file.save(f"uploads/{unique_filename}.{extension}")
    return obj.user_upload_avatar_model(uid,final_file_path)

@app.route('/uploads/<filename>')
def upload_filename_controller(filename):
    return send_file(f"uploads/{filename}")


@app.route('/user/login', methods=['POST'])
def user_controller_login():
    return obj.user_login_model(request.form)    

