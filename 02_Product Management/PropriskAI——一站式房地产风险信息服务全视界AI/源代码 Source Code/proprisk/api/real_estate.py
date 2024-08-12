from flask import Blueprint, jsonify, request, current_app, redirect
import json
import jwt
from datetime import datetime,timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


real_estate_api = Blueprint('real_estate_api', __name__)


# 非会员能够查看
# 显示房地产公司的基本信息
@real_estate_api.route('/base_info', methods=['POST'])
def found_real_estate_base_info():
    pass

