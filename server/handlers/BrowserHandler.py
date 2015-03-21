#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import datetime
import tornado
import random
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
from tornado.template import Template
from tornado.template import Loader

class BrowserHandler(BaseHandler):
    """HTML display of Keywords browsed in the last day"""

    def get(self):
        loader = tornado.template.Loader('../server/templates')
        n = self.get_argument('n', 3)
        db = self.settings['db']
        logging.debug('hit the BrowserHandler endpoint with n=', n)
        keywords = []
        found = 0
        while found < int(n):
            k = db.randomkey()
            if k not in keywords:
                keywords.append(k)
                found += 1
        self.write(loader.load("zen.html").generate(keywords=keywords))
        self.finish()