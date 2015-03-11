#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import tornado
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject

class ApiHandler(BaseHandler):
    """json access to local curriculum store"""

    def get(self):
        try:
            n = self.get_argument('n')
        except:
            n = 3 # three hours, should be global EXPIRE_IN from worker.py
        db = self.settings['db']
        print 'hit the BrowserHandler endpoint with n=', n
        keywords = []
        found = 0
        while found < int(n):
            k = db.randomkey()
            if k is not None:
                if k not in keywords:
                    keywords.append(k)
                    found += 1
            else:
                keywords = ['no recent results']
        d = {'title':'tuned-resonator curriculum-barnacle test',
        'noun_phrase':keywords}
        self.response = ResponseObject('200','Success', d)
        self.write_response()
        self.finish()