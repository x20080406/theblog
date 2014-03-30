#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 6 Mar 2014 11:01:07

@author: tianjie
'''


from flask_wtf import Form
from wtforms.fields import (TextField, PasswordField, BooleanField, HiddenField, \
                             TextAreaField, SelectMultipleField,SelectField)
from wtforms.validators import Required
from admin.models import (Tag, Category)
'''
创建表时需要将初始化choices的语句注释掉
'''
class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    passwd = PasswordField('passwd', validators=[Required()])
    remember = BooleanField('记住我', default=False)
    
class CategoryForm(Form):
    id = HiddenField('id')
    name = TextField('name', validators=[Required()])
    id_num = TextField('id_num', validators=[Required()])
    content = TextAreaField('content', validators=[Required()])
    
class TagForm(Form):
    id = HiddenField('id')
    name = TextField('name', validators=[Required()])
    sort = TextField('sort', validators=[Required()])
    
class ArticleForm(Form):
    id = HiddenField('id')
    title = TextField('name', validators=[Required()])
    content = TextAreaField('content', validators=[Required()])
    tags = SelectMultipleField('tags', validators=[Required()])
    '''choices=[(t.id, t.name) for t in Tag.query.order_by('id')]'''
    categories = SelectField('categories', validators=[Required()])
    '''choices=[(c.id, c.name) for c in Category.query.order_by('id')]'''
