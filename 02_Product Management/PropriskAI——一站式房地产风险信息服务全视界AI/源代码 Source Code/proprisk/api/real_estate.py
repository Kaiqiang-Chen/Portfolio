from flask import Blueprint, jsonify, request, current_app, redirect
import json
import jwt
from datetime import datetime,timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


real_estate_api = Blueprint('real_estate_api', __name__)


# �ǻ�Ա�ܹ��鿴
# ��ʾ���ز���˾�Ļ�����Ϣ
@real_estate_api.route('/base_info', methods=['POST'])
def found_real_estate_base_info():
    pass

