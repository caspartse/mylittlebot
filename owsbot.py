#!/usr/bin/env python
# -*- coding:utf-8 -*
import datetime
import requests
import re
import simplejson as json


class OWS(object):

    def __init__(self):
        super(OWS, self).__init__()

    def calendar(self):
        today = datetime.date.today()
        imgUrl = 'http://img.owspace.com/Public/uploads/Download/%d/%02d%02d.jpg' % (
            today.year, today.month, today.day)
        try:
            desc = self.ocr(imgUrl)
        except:
            desc = '__'
        text = u'%s月%s日，%s。' % (today.month, today.day, desc)
        item = {
            'text': text,
            'imgurl': imgUrl
        }
        return item

    def ocr(self, imgUrl):
        url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/ocr?language=zh-Hans'
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'YOUR-SUBSCRIPTION-KEY',
        }
        payload = {'url': imgUrl}
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        data = resp.json()
        _regions = []
        for d in data['regions']:
            _lines = []
            for l in d['lines']:
                _words = []
                for w in l['words']:
                    _words.append(w['text'])
                _lines.append(''.join(_words))
            _regions.append('\n'.join(_lines))
        content = '\n'.join(_regions)
        pattern = ur'([宜忌]\S+)'
        try:
            desc = re.search(pattern, content).group(1).strip()
        except:
            desc = ''
        return desc

if __name__ == '__main__':
    o = OWS()
    item = o.calendar()
    msg = u'%s %s' % (
        item['text'],
        item['imgurl']
    )
    print msg
