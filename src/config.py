#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import timedelta
#--FLASK - SQLALCHEMY--
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_USER = 'tianjie'
MYSQL_PASS = 'qqw'
MYSQL_DB = 'app2'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

DB_URI = SQLALCHEMY_DATABASE_URI
DEBUG = True
SECRET_KEY = 'PBKDF2$sha256$10000$dfuYRpDwvaFhmOU5$5E/Zu8tAQF2qhW0/4X/fd8X7kXBxoR1M'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)

PER_PAGE = 8

ADD_TYPE=u'新增'
EDIT_TYPE=u'修改'

#缓存
PAGE_CACHE = False
PAGE_CACHE_TIME = 3600

