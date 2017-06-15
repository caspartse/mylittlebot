#!/usr/bin/env python
# -*- coding:utf-8 -*
import requests
import re


class Solibot(object):

    def __init__(self):
        super(Solibot, self).__init__()

    def fetchArticles(self):
        url = 'http://www.solidot.org/'
        headers = {
            'Host': 'www.solidot.org',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        resp = requests.get(url, headers=headers)
        content = resp.text
        pattern = ur'<h2><a href="/story\?sid=(\d+?)">([\s\S]+?)</a></h2>[\s\S]+?<span>来自<strong>([\s\S]*?)</strong></span>'
        mass = re.findall(pattern, content)
        articles = []
        for item in mass:
            sid, title, dept = item
            story = {
                'title': title,
                'dept': dept,
                'url': 'http://www.solidot.org/story?sid=%s' % (sid)
            }
            articles.append(story)
        return articles


if __name__ == '__main__':
    s = Solibot()
    articles = s.fetchArticles()
    for story in articles:
        msg = u'《%s》 %s -- 来自%s部门' % (
            story['title'],
            story['url'],
            story.get('dept') or u'名字被小鲸鱼吃了'
        )
        print msg
