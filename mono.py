#!/usr/bin/env python
# -*- coding:utf-8 -*
import requests
import re


class Mono(object):

    def __init__(self):
        super(Mono, self).__init__()

    def qian(self):
        url = 'http://mmmono.com/group/100044/'
        headers = {
            'Host': 'mmmono.com',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate'
        }
        sess = requests.Session()
        sess.headers.update(headers)
        resp = sess.get(url)
        content = resp.content
        pattern = r'<li><a href="http://mmmono\.com/g/meow/(\d{6,})/" target="_blank">[\s\S]+?<h3 class="name">MONO日签</h3>[\s\S]+?<div class="cover"><img src="([^\s]+?)"/>\s+</div>\s+<div class="meow-time"><span class="date">([\s\S]+?)</span>[\s\S]+?</li>'
        meowId, imgUrl, date = re.findall(pattern, content)[0]
        meowUrl = 'http://mmmono.com/g/meow/%s' % (meowId)
        resp = sess.get(meowUrl)
        content = resp.content
        pattern = r'<title>([\s\S]+?)</title>'
        title = re.search(pattern, content).group(
            1).replace('- MONO猫弄', '').strip()
        item = {
            'meowid': str(meowId),
            'title': title,
            'imgurl': imgUrl,
            'monodate': date
        }
        return item

if __name__ == '__main__':
    m = Mono()
    item = m.qian()
    msg = '%s。%s' % (
        item['title'],
        item['imgurl']
    )
    print msg
