#! /usr/bin/env python
#coding=utf-8

import json
import math
import random
import time
import urllib2

class FetchYKURL:
    """获取优库视频地址"""

    def __init__(self, url):
        
        #首先判断一下是不是有效的视频地址
        self.url = url

    def _read_json(self, url):
        page = urllib2.urlopen(url).read()
        return json.loads(page)


    def _get_sid(self):
        i1 = int(1000 + math.floor(random.random() * 999))
        i2 = int(1000 + math.floor(random.random() * 9000))
        return str(int(time.time() * 1000)) + str(i1) + str(i2)

    def _create_sid(self):
        nowTime = int(time.time() * 1000)
        random1 = random.randint(1000,1998)
        random2 = random.randint(1000,9999)
        return "%d%d%d" %(nowTime,random1,random2)
     
    def _get_fileid_mixstring(self, seed):
        mixed=[]
        source=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890")
        seed=float(seed)
        for i in range(len(source)):
            seed = (seed * 211 + 30031 ) % 65536
            index = math.floor(seed / 65536 * len(source) )
            mixed.append(source[int(index)])
            source.remove(source[int(index)])
        #return ''.join(mixed)
        return mixed
     
    def _get_fileid(self, fileId,seed):
        mixed=self._get_fileid_mixstring(seed)
        ids=fileId.split('*')
        if ids[len(ids) - 1] == '':
            del ids[len(ids) - 1]
        
        realId=[]
        for ch in ids:
            realId.append(mixed[int(ch.encode('ascii'))]) 
        return ''.join(realId)

    def _get_key(key1, key2):
        key = int(key1, 16)
        key ^= 0xA55AA5A5
        res = key2 + str(key)
        return res

    def get_real_url(self):

        #先处理一下url
        const_pre_url = r'http://v.youku.com/player/getPlayList/VideoIDS/'
        begin = self.url.find(r'id_')
        end = self.url.find(r'.html')
        url = const_pre_url + self.url[begin + 3:end]

        #根据此url获取json字符串
        r_list = self._read_json(url)['data']
        
        #获取seed
        seed = r_list[0].get('seed')

        #获取sid
        inner_fileid = r_list[0].get('streamfileids').get('flv')
        ori_fileid = self._get_fileid(inner_fileid, seed)
        sid = self._get_sid()
    
        #为构造最终地址定义以下常量
        const_prefix = r'http://f.youku.com/player/getFlvPath/sid/'
        const_prefix2 = r'/st/flv/fileid/'
        const_midfix = r'_00'
        const_midfix2 = r'?K='
        const_prefix_new = r'http://f.youku.com/player/getFlvPath/sid/00_00/st/flv/fileid/'
        
        key_dict_list = r_list[0].get('segs').get('flv')
        urllist = []
        i = 0
        for keys in key_dict_list:
            fileid_list = list(ori_fileid)
            if i > 9:
                hexstr = '%02X' %(i)
                fileid_list[8:10] = hexstr.encode('ascii')
            else:
                fileid_list[9] = str(i).encode('ascii')
            i = i + 1
            fileid = ''.join(fileid_list)
            total_url = const_prefix_new + fileid + const_midfix2 + keys['k'] + r',k2:' + keys['k2']
            urllist.append(urllib2.urlopen(total_url).geturl())
            
        return urllist

if __name__ == '__main__':
    url = 'http://v.youku.com/v_show/id_XMzYzODA4MTQ4.html'
    u = FetchYKURL(url)
    print u.get_real_url()
