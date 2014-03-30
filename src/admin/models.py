#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 6 Mar 2014 10:40:35

@author: tianjie
'''

from hashlib import sha1

from sqlalchemy import (Column, VARCHAR,Text,SmallInteger, Integer, Boolean,DateTime, ForeignKey)
from sqlalchemy.orm import (synonym, relationship, backref)
from flask_sqlalchemy import (SQLAlchemy)
from flask_login import UserMixin
from auth import login_serializer
from hash_passwords import (make_hash, check_hash)  
from webapp import app

class QueuePool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(QueuePool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        del options['pool_size']

db = QueuePool_SQLAlchemy(app)

class HasUniqueName(object):
    name = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.name)

group_permission_table = db.Table(
    'group_permission', 
    Column(
        'group_id', Integer,
        db.ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'permission_id', Integer,
        db.ForeignKey('permissions.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)

user_group_table = db.Table(
    'user_group',
    Column(
        'user_id', Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'group_id', Integer,
        db.ForeignKey('groups.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)


class User(UserMixin, db.Model):
    id = Column( db.Integer, primary_key=True)
    __tablename__ = 'users'
    username = Column(VARCHAR(255), nullable=False, unique=True)
    name = Column(VARCHAR(50), nullable=False, unique=True)
    _password = Column('password', VARCHAR(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def get_auth_token(self):
        data = (self.id, sha1(self.password).hexdigest())
        return login_serializer.dumps(data)

    def _set_password(self, password):
        self._password = make_hash(password)

    def _get_password(self):
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def valid_password(self, password):
        """Check if provided password is valid."""
        return check_hash(password, self.password)

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id,
                                 self.username)

    def in_groups(self):
        """Return set of groups which user belongs to."""
        return set(r[0] for r in db.session.query(Group.name).join(
            Group.users
        ).filter(User.id == self.id))

    def has_permissions(self):
        """Return set of permissions which user has."""
        return set(r[0] for r in db.session.query(Permission.name).join(
            Permission.groups, Group.users
        ).filter(User.id == self.id))

class Group(HasUniqueName, db.Model):
    __tablename__ = 'groups'
    id = Column( db.Integer, primary_key=True)
    users = relationship(
        'User', backref=backref('groups', collection_class=set),
        secondary=user_group_table, collection_class=set
    )

class Permission(HasUniqueName, db.Model):
    id = Column( db.Integer, primary_key=True)
    __tablename__ = 'permissions'
    groups = relationship(
        'Group', backref=backref('permissions', collection_class=set),
        secondary=group_permission_table, collection_class=set
    )

####################
# 文章,评论,类别,TAG #
####################
tag_article_table = db.Table(
    't_tag_article_rel', 
    Column(
        'tag_id', Integer,
        ForeignKey('t_tags.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'article_id', Integer,
        ForeignKey('t_articles.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)

category_article_table = db.Table(
    't_category_article_rel', 
    Column(
        'category_id', Integer,
        ForeignKey('t_categories.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'article_id', Integer,
        ForeignKey('t_articles.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)

class Category(HasUniqueName, db.Model):
    __tablename__ = 't_categories'
    id = Column( db.Integer, primary_key=True)
    name = Column(VARCHAR(17), nullable=False, unique=True)
    id_num = Column(SmallInteger, nullable=False)
    content = Column(Text, nullable=False)
    articles = relationship(
        'Article', backref=backref('t_categories', collection_class=set),
        secondary=category_article_table, collection_class=set
    )
    
    def get_page(self):
        return  Category.query.paginate()
    def remove(self):
        Category.query
    
class Comment(db.Model):
    __tablename__='t_comments'
    id = Column( db.Integer, primary_key=True)
    #postid=Column() 外键关联到POSTS大表
    author=Column(VARCHAR(20),nullable=False)
    email=Column(VARCHAR(30),nullable=False)
    url=Column(VARCHAR(75))
    visible=Column(Boolean)
    add_time=Column(DateTime)
    content=Column(Text)
    
class Article(db.Model):
    __tablename__="t_articles"
    id = Column( db.Integer, primary_key=True)
    title=Column(VARCHAR(100),nullable=False )
    content=Column(Text,nullable=False)
    comment_num=Column(SmallInteger)
    add_time=Column(DateTime)
    edit_time=Column(DateTime)
    tags = relationship(
        'Tag', backref=backref('t_articles', collection_class=set),
        secondary=tag_article_table, collection_class=set,cascade="all" )
    categories = relationship(
        'Category', backref=backref('t_categories', collection_class=set),
        secondary=category_article_table, collection_class=set,cascade="all" )
    
    def init_tag(self,_tags):
#         self.tags.clear()
        for t in _tags:
            self.tags.add(Tag.query.get(int(t)))
    
    def init_category(self,_categories):
#         self.categories.clear()
        for t in _categories:
            self.categories.add(Tag.query.get(int(t)))
    
class Tag(HasUniqueName,db.Model):
    __tablename__='t_tags'
    id = Column( db.Integer, primary_key=True)
    sort=Column(SmallInteger)
    articles = relationship(
        'Article', backref=backref('t_tags', collection_class=set),
        secondary=tag_article_table, collection_class=set,cascade="all"
    )
    
    
'''
飞信活动表
'''
class Inviter(db.Model):
    __tablename__='t_inviters'
    id = Column( db.Integer, primary_key=True)
    uid = Column( db.Integer)
    tel = Column( db.BIGINT)
    sid = Column( db.Integer)
    sendTime = Column( db.DateTime)
    invitees = relationship(
        'Invitee', backref=backref('t_invitees', collection_class=set),
        collection_class=set
    )

class Invitee(db.Model):
    __tablename__='t_invitees'
    id = Column( db.Integer, primary_key=True)
    uid = Column( db.Integer)
    tel = Column( db.BIGINT)
    sid = Column( db.Integer)
    invite_id = Column(db.Integer,db.ForeignKey("t_inviters.id"))
    
class VisitInfo(db.Model):
    __tablename__='t_visitinfo'
    id = Column(db.Integer,primary_key=True)
    type = Column(db.SMALLINT)
    ip = Column(db.BigInteger)#将IP转换为LONG存放
    visit_date = Column(db.DateTime)
    channel = Column( db.VARCHAR(50))


    
    