#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 6 Mar 2014 09:39:08

@author: tianjie
'''
from datetime import datetime
from hashlib import sha1
from flask import (Flask, render_template as view, request, \
                   redirect, url_for, flash, session,jsonify, current_app, abort)
from flask_login import (login_user, logout_user, \
                         current_user, login_required)
from sqlalchemy.exc import DatabaseError
from itsdangerous import constant_time_compare, BadData
from config import *
from models import (User,Category,db,Tag,Article)
from .forms import (LoginForm,CategoryForm,TagForm,ArticleForm)
from .auth import (authorized, require, IsUser,\
                    InGroups, HasPermissions, Any, login_serializer)

from webapp import app 

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() 
        if user is not None and user.valid_password(form.passwd.data):
            if login_user(user, remember=form.remember.data):
                # Enable session expiration only if user hasn't chosen to be
                # remembered.
                session.permanent = not form.remember.data
                flash('登陆成功!', 'success')
                return redirect(request.args.get('next') or url_for('.index'))
            else:
                flash('账户已禁用!', 'error')
        else:
            flash('用户名或密码错误!', 'error')
    return view("admin/login.html",form=form)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('.login'))


@app.route("/admin/index")
@login_required
def index():
    #return view('admin/index.html')
    return redirect(url_for(".article",page=1))


'''''''''''''''''''''''''''''
category 类别
'''''''''''''''''''''''''''''
@app.route("/admin/category/<int:page>")
@login_required
def category(page=1):
    p = Category.query.order_by(Category.id_num.desc()).paginate(page,PER_PAGE,error_out=False)
    return view('admin/category.html', paginate = p,page=page)

@app.route('/admin/category/<int:id>/modify', methods=['GET'])
@login_required
def category_modify(id=1):
    c = Category.query.get(id)
    form = CategoryForm(request.form,c)
    return view('/admin/category_modify.html',type=EDIT_TYPE,obj=form)

@app.route('/admin/category/add', methods=['GET'])
@login_required
def category_add():
    form = CategoryForm()
    return view('/admin/category_modify.html',type=ADD_TYPE,obj=form)

@app.route('/admin/category/save', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def category_save():
    mid = request.form.get('id','')
    name = request.form.get('name', '')
    id_num = request.form.get('id_num', '')
    content = request.form.get('content', '')
    if (mid == None or mid == ''):
        category = Category(name=name,id_num=id_num,\
                            content=content)
        db.session.add(category)
    else:
        category = Category(id=mid,name=name,\
                            id_num=id_num,content=content)
        db.session.merge(category)
    db.session.commit()
    flash('保存成功!', 'success')
    return redirect(url_for('.category',page=1))
    
@app.route('/admin/category/remove', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def category_remove():
    ids = request.form.getlist('id')
#     import pdb
#     pdb.set_trace()
    Category.query.filter(Category.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('操作成功!', 'success')
    return jsonify(message="success")


'''''''''''''''''''''''''''''
tag 类别
'''''''''''''''''''''''''''''
@app.route("/admin/tag/<int:page>")
@login_required
def tag(page=1):
    p = Tag.query.order_by(Tag.id.desc()).paginate(page,PER_PAGE,error_out=False)
    return view('admin/tag.html', paginate = p,page=page)

@app.route('/admin/tag/<int:id>/modify', methods=['GET'])
@login_required
def tag_modify(id=1):
    c = Tag.query.get(id)
    form = TagForm(request.form,c)
    return view('/admin/tag_modify.html',type=EDIT_TYPE,obj=form)

@app.route('/admin/tag/add', methods=['GET'])
@login_required
def tag_add():
    form = TagForm()
    return view('/admin/tag_modify.html',type=ADD_TYPE,obj=form)

@app.route('/admin/tag/save', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def tag_save():
    mid = request.form.get('id')
    name = request.form.get('name', '')
    sort = request.form.get('sort', '')
    if (mid == None or mid == ''):
        tag = Tag(name=name, sort=sort)
        db.session.add(tag)
    else:
        tag = Tag(id=mid,name=name, sort=sort)
        db.session.merge(tag)
    db.session.commit()
    flash('保存成功!', 'success')
    return redirect(url_for('.tag',page=1))
    
@app.route('/admin/tag/remove', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def tag_remove():
    ids = request.form.getlist('id')
#     import pdb
#     pdb.set_trace()
    Tag.query.filter(Tag.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('操作成功!', 'success')
    return jsonify(message="success")


'''''''''''''''''''''''''''''
文章管理
'''''''''''''''''''''''''''''
@app.route("/admin/article/<int:page>")
@login_required
def article(page=1):
    p = Article.query.order_by(Article.id.desc()).paginate(page,PER_PAGE,error_out=False)
    return view('admin/article.html', paginate = p,page=page)

@app.route('/admin/article/<int:id>/modify', methods=['GET'])
@login_required
def article_modify(id=1):
    c = Article.query.get(id)
#     c.tags = [t.id for t in c.tags]
#     c.categories = [t.id for t in c.categories]
#     form = ArticleForm()
#     form.categories.default=[88,90]
#     form.tags.default=[16,17,18]
    form=ArticleForm(id=c.id,title=c.title,content=c.content,\
                     tags=[t.id for t in c.tags],\
                     categories=str([t.id for t in c.categories][0]))
    form.tags.choices=[(t.id, t.name) for t in Tag.query.order_by('id')]
    form.categories. choices=[(c.id, c.name) for c in Category.query.order_by('id')]
    return view('/admin/article_modify.html',type=EDIT_TYPE,obj=form)

@app.route('/admin/article/add', methods=['GET'])
@login_required
def article_add():
    form = ArticleForm()
    form.tags.choices=[(t.id, t.name) for t in Tag.query.order_by('id')]
    form.categories. choices=[(c.id, c.name) for c in Category.query.order_by('id')]
    return view('/admin/article_modify.html',type=ADD_TYPE,obj=form)

@app.route('/admin/article/save', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def article_save():
    mid = request.form.get('id')
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    
    if (mid == None or mid == ''):
        article = Article(title=title, content=content, add_time=datetime.now(), edit_time=datetime.now())
        for cid in request.form.getlist("tags"):
            article.tags.add(Tag.query.get(cid))
        for cid in request.form.getlist("categories"):
            article.categories.add(Category.query.get(cid))
        db.session.add(article)
    else:
        article = Article.query.get(int(mid))
        article.title=title
        article.content=content
        article.edit_time=datetime.now()
        article.categories.clear()
        article.tags.clear()
        for cid in request.form.getlist("tags"):
            article.tags.add(Tag.query.get(cid))
        for cid in request.form.getlist("categories"):
            article.categories.add(Category.query.get(cid))
            
    db.session.commit()
    flash('保存成功!', 'success')
    return redirect(url_for('.article',page=1))
    
@app.route('/admin/article/remove', methods=['POST'])
@login_required
@require(Any(IsUser('tianjie'), InGroups('admins')))
def article_remove():
    ids = request.form.getlist('id')
#     import pdb
#     pdb.set_trace()
    Article.query.filter(Article.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('操作成功!', 'success')
    return jsonify(message="success")






