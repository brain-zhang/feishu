#!/usr/bin/env python
# coding: utf-8
import os
import web

#如果是在本地调试，请打开此开关，如果上传到sae，请置为False
LOCAL_DEBUG = True 

if LOCAL_DEBUG:
    templates_root = 'templates'
else:
    import sae
    app_root = os.path.dirname(__file__)
    templates_root = os.path.join(app_root, '../templates')
    
render = web.template.render(templates_root, cache=False)
