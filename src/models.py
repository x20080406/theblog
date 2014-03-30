#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 9 Mar 2014 22:36:56

@author: tianjie
'''



from admin.models import *
from webapp import app
if __name__ == '__main__':
    engine = db.get_engine(app=app);
    db.drop_all()
    db.create_all()
    
    p1 = Permission(name=u'read')
    p2 = Permission(name=u'write')
    p3 = Permission(name=u'delete')
    g1 = Group(name=u'admins')
    g1.permissions = set([p1, p2, p3])
    g2 = Group(name=u'users')
    g2.permissions = set([p1, p2])
    u1 = User(username=u'tianjie', password=u'tianjie',name="tianj")
    u1.groups.add(g1)
    u2 = User(username=u'bar', password=u'bar',name='bar')
    u3 = User(username=u'baz', password=u'baz',name='baz姓', active=False)
    g2.users = set([u2, u3])
    db.session.add_all([u1, u2, u3])
    #article
#     a1= Article(title=u'aa1',content=u'aa')
#     a2= Article(title=u'aa2',content=u'aa')
#     a3= Article(title=u'aa3',content=u'aa')
#     db.session.add_all([a1,a2,a3])
    
    db.session.commit()
    
    #tags
#     t1=Tag(name=u"t1",sort=1)
#     t2=Tag(name=u"t2",sort=3)
#     t3=Tag(name=u"t3",sort=2)
#     
#     
#     t1.articles=set([a1,a2])
#     t2.articles=set([a1,a3])
#     t3.articles=set([a1,a3])
#     db.session.add_all([t1,t2,t3]);
#     
#     #category
#     c1 = Category(name=u"类别1",id_num=1,content=u"内容1")
#     c2 = Category(name=u"类别2",id_num=2,content=u"内容2")
#     c3 = Category(name=u"类别3",id_num=3,content=u"内容3")
#     c4 = Category(name=u"类别4",id_num=4,content=u"内容4")
#     c5 = Category(name=u"类别5",id_num=5,content=u"内容5")
#     c6 = Category(name=u"类别6",id_num=6,content=u"内容6")
#     c7 = Category(name=u"类别7",id_num=7,content=u"内容7")
#     c8 = Category(name=u"类别8",id_num=8,content=u"内容8")
#     c9 = Category(name=u"类别9",id_num=9,content=u"内容9")
#     c10 = Category(name=u"类别10",id_num=10,content=u"内容10")
#     c11 = Category(name=u"类别11",id_num=11,content=u"内容11")
#     c12 = Category(name=u"类别12",id_num=12,content=u"内容12")
#     db.session.add_all([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]);
#     '''
#     i1 = Inviter(uid=1)
#     i2 = Inviter(uid=2)
#     i3 = Inviter(uid=3)
#     
#     ie1 = Invitee(uid=2)
#     ie2 = Invitee(uid=1)
#     ie3 = Invitee(uid=3)
#     
#     i1.invitees=set([ie1,ie2,ie3])
#     
#     db.session.add_all([i1,i2,i3])
#     '''
#     
#     
#     db.session.commit()
    
