#! /usr/bin/env python
#coding=utf-8
from config.urls import urls
from config import settings
import os
import web
import sae

def notfound():
    render = settings.render
    return web.notfound(render.notfound())

app = web.application(urls, globals())
app.notfound = notfound
application = sae.create_wsgi_app(app.wsgifunc())    
