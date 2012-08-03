#! /usr/bin/env python
#coding=utf-8

import time
import urllib2
import web
from web import form
from config.settings import render
from flib.geturl import FetchYKURL

vurl = form.regexp(r'http://.*youku.com/v_show/*', '目前仅支持"http://v.youku.com/v_show/"类地址')
url_form = form.Form(form.Textbox('userurl', form.notnull, vurl, description = ''))
                        #form.Button('开始捕获', type = 'submit', value = 'OK'))

class SmartRedirectHandler(urllib2.HTTPRedirectHandler): 
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)              
        result.status = code                                 
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers): 
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        print result.url
        return result 

class index:
    def GET(self):
        #return render.index(render.player(), url_form())
        #return render.player()
        return render.index(content = r'waiting...', form = url_form(), urllist = '')


    def POST(self):
        #u = fetchFetchYKURLp://v.youku.com/v_show/id_XMjUyODAzNDg0.html')
        f = url_form()
        if not f.validates():
            return render.index(content = r'waiting...',form = f, urllist = [])
        else:
            u = FetchYKURL(web.input().get('userurl'))
            urllist = u.get_real_url()
            return render.index(content = render.player(urllist), form = f, urllist = urllist)
        
