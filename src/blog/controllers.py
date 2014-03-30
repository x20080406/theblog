#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 21 Mar 2014 20:15:46

@author: tianjie
'''
import markdown
from flask import (render_template as view,abort,Markup)
from webapp import app 
from config import *
from cache import pagecache
from admin.models import Article,db
from collections import OrderedDict

@app.route('/<int:page>')
@pagecache
def blog_index(page=1):
    prefix='/'
    suffix=''
    p = Article.query.order_by(Article.add_time.desc()) \
            .paginate(page,PER_PAGE,error_out=False)
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view('index.html', paginate = p,page=page,tags=tags,categories=categories)

@app.route('/topic/<int:id>/<string:title>')
@pagecache
def blog_topic(id=1,title=''):
    article = Article.query.get(id)
    if(article==None):
        abort(404)
    content = content = Markup(markdown.markdown(article.content))
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view("topic.html", **locals())


@app.route('/tag/<int:page>/<string:param>')
@pagecache
def blog_tag(page=1,param=''):
    if(param==''):
        abort(404)
        
    paginate = Article.query.filter(Article.tags.any(name = param)) \
            .order_by(Article.add_time.desc()) \
            .paginate(page,PER_PAGE,error_out=False)
            
    prefix='/tag/'
    suffix='/'+param
    
    tags = group_tag_with_count()
    categories = group_category_with_count()
    return view("index.html", **locals())


'category'
@app.route('/category/<int:page>/<string:param>')
@pagecache
def blog_category(page=1,param=''):
    if(param==''):
        abort(404)
#     import pdb
#     pdb.set_trace()    
    paginate = Article.query.filter(Article.categories.any(name = param)) \
            .order_by(Article.add_time.desc()) \
            .paginate(page,PER_PAGE,error_out=False)
            
    tags = group_tag_with_count()
    categories = group_category_with_count()
    prefix='/category/'
    suffix='/'+param
    return view("index.html", **locals())


@app.route('/tags')
@pagecache
def blog_tags():
    _endpoint='blog_tag'
    items = group_tag_with_count()
    return view('tags_and_categories.html',**locals()) 
@app.route('/categories')
@pagecache
def blog_categories():
    _endpoint='blog_category'
    items = group_category_with_count()
    return view('tags_and_categories.html',**locals()) 

'''
util
'''
# @pagecache
def group_category_with_count():
        rs=OrderedDict()
        for a in db.session.execute(
                                    '''SELECT a. name, ifnull(b.count, 0) count FROM t_categories a
                                    LEFT JOIN (
                                        SELECT count(*) count, t.category_id FROM        
                                        t_category_article_rel t GROUP BY t.category_id
                                    ) b ON a.id = b.category_id order by a.id_num'''):
            rs[a.name] = a.count
        return rs
# @pagecache
def group_tag_with_count():
        rs=OrderedDict()
        for a in db.session.execute(
                                    '''SELECT a. name, ifnull(b.count, 0) count FROM t_tags a
                                    LEFT JOIN (
                                        SELECT count(*) count, t.tag_id FROM        
                                        t_tag_article_rel t GROUP BY t.tag_id
                                    ) b ON a.id = b.tag_id order by a.sort'''):
            rs[a.name] = a.count
        return rs