#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 25 Mar 2014 10:19:03

@author: tianjie
'''


def printdebug(func):
    def __decorator(*args,**kwargs):
        print('enter the login[%s%s]' % (args[0],kwargs['name']))
        func()
        print('exit the login')
    return __decorator 
 
# combine the printdebug and login
@printdebug  
def login():
    print('in login')
@printdebug  
def login1():
    print('in login')
# make the calling point more intuitive

if __name__=='__main__':
    login('aaa',name='bbb')  
    login1('aaa',name='bbb')  
