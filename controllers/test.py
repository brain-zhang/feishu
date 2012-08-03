
import web
import mimetypes
import urllib2
from config.settings import render

class index:
    def GET(self):
        return render.test(urllib2.urlopen("http://www.baidu.com").geturl())
