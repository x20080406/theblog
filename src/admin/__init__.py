#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 6 Mar 2014 11:51:08

@author: tianjie
'''

from hashlib import sha1
from webapp import loginManager,app
from .models import User,db
from itsdangerous import constant_time_compare, BadData
from .auth import login_serializer
from flask import (render_template as view)
from sqlalchemy.exc import (DatabaseError,IntegrityError)
from werkzeug.routing import *
from blog.controllers import (group_category_with_count,group_tag_with_count)

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  # @UndefinedVariable
#     pass

@loginManager.token_loader
def load_token(token):
    try:
        max_age = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
        user_id, hash_a = login_serializer.loads(token, max_age=max_age)
    except BadData:
        return None
    user = User.query.get(user_id)  # @UndefinedVariable
    if user is not None:
        hash_a = hash_a.encode('utf-8')
        hash_b = sha1(user.password).hexdigest()
        if constant_time_compare(hash_a, hash_b):
            return user
    return None

@app.errorhandler(403)
def forbidden_403(exception):
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view('403.html',tags=tags,categories=categories) ,403

@app.errorhandler(401)
def forbidden_401(exception):
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view('403.html',tags=tags,categories=categories) ,401

@app.errorhandler(404)
def error_404(exception):
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view('404.html',error=exception,tags=tags,categories=categories) ,404
  
@app.errorhandler(Exception)
def internal_error(error):
    tags = group_tag_with_count()
    categories = group_category_with_count()
    db.session.rollback()
#     import pdb
#     pdb.set_trace()    
    return view('500.html',error=error,tags=tags,categories=categories), 500
