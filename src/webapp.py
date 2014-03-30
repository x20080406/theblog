#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 6 Mar 2014 09:36:41

@author: tianjie
'''

# import sys
# import os
# abspath = os.path.abspath(__file__)
# app_root = os.path.dirname(abspath)
# path = os.path.join(app_root, 'site_packages/lib/python2.7/site-packages')
# sys.path.insert(0, path)
# sys.path.insert(0, app_root)

from flask import Flask
from flask_login import LoginManager
from config import SECRET_KEY

import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = SECRET_KEY
#login manager
loginManager = LoginManager()
loginManager.init_app(app)

from admin.controllers import *
from blog.controllers import *

app.add_url_rule('/', view_func= blog_index)
app.add_url_rule('/admin/', view_func= login)

app.config["SQLALCHEMY_ECHO"] = False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)