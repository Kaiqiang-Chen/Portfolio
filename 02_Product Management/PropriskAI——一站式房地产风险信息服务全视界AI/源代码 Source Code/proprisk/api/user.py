from flask import Blueprint, jsonify, request, current_app, redirect
import json
import jwt
from datetime import datetime,timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import pdb

user_api=Blueprint('user_api',__name__)
from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017/')
db=client['user']
users=db['user']


def token_required(func):
    @wraps(func)
    def _verify(*args,**kwargs):
        # auth_headers=request.headers.get('Authorization','').split()
        auth_headers=request.headers.get('Authorization')
        invalid_msg = {
            'message': '您需要先登录',
            'authenticated': False
        }
        expired_msg = {
            'message': '登录信息过期，您需要重新登录',
            'authenticated': False
        }
        try:
            # token = auth_headers[1]
            token = auth_headers
            print(token)
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms='HS256')
            cur_user = users.find_one({'username':data['sub']})
            if not cur_user:
                raise RuntimeError('User not found')
            return func(cur_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            print(expired_msg)
            return jsonify(expired_msg), 401
        except jwt.InvalidTokenError as e:
            print(e)
            print(invalid_msg)
            return jsonify(invalid_msg), 401

    return _verify

@user_api.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    user=users.find_one({"username":data['username']})
    inputPassword=data['password']
    if not user:
        return jsonify({'message':'用户名或密码错误'}),401

    password=user['password']
    if inputPassword!=password:
        return jsonify({'message':'用户名或密码错误'}),401
    token=jwt.encode({
        'sub':user['username'],
        'iat':datetime.utcnow(),
        'exp':datetime.utcnow()+timedelta(minutes=60)},
        current_app.config['SECRET_KEY'],algorithm='HS256'
    )
    return jsonify({'token':token,'username':user['username'],'role':user['role']})

@user_api.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    user=users.find_one({'username':data['username']})
    if user:
        return jsonify({'message':'用户名已存在'}),401
    try:
        # print(type(current_app.config['SECRET_KEY']))
        # print(current_app.config['SECRET_KEY'])

        token = jwt.encode({
            'sub': data['username'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60)},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
        # pdb.set_trace()
        users.insert_one({'username':data['username'],'password':data['password'],'role':0})
        userlist = users.find({})
        for u in userlist:
            print(u)
        return jsonify({'token': token, 'username': data['username'], 'role': 0}),200
    except Exception:
        return jsonify('message','注册失败'),401
