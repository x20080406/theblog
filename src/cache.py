#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 24 Mar 2014 17:35:02

@author: tianjie
'''
from config import (PAGE_CACHE,PAGE_CACHE_TIME,DEBUG)
from flask import request
import functools
import hashlib
import logging as log
try:
    import pylibmc as memcache
except:
    import memcache

#Memcache 是否可用、用户是否在后台初始化Memcache
MC_Available = False
if PAGE_CACHE:
    if DEBUG:
        client = memcache.Client(['127.0.0.1:11211']) 
    else:
        client = memcache.Client() 
    
    if PAGE_CACHE :
        try:
            MC_Available = client.set('mc_available', '1', 3600)
        except:
            log.error("初始化缓存出错")
            pass

def pagecache(fn,key="",time=PAGE_CACHE_TIME):
    
    @functools.wraps(fn)
    def _decorate(*args,**kwargs):
        if not MC_Available :
            return fn(*args,**kwargs)
        
        _key = key
        
        if _key :
            _key = str(_key)
        else:
            _key = str(request.path)
            
        md5 = hashlib.md5(_key)
        _key = md5.hexdigest()  
                
        rs = client.get(_key)
        if rs:
            return rs
        else :
            rs = fn(*args, **kwargs)
            client.set(_key,rs,PAGE_CACHE_TIME)
            return rs
    return _decorate
        
        
