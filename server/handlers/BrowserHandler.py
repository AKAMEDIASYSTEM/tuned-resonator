#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import datetime
import tornado
import random
from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject

class BrowserHandler(BaseHandler):
    """HTML display of Keywords browsed in the last day"""

    def get(self):
        try:
            t = self.get_argument('t')
        except:
            t = 10800 # three hours, should be global EXPIRE_IN from worker.py
        db = self.settings['db']
        logging.debug('hit the BrowserHandler endpoint with t=', t)
        phrase = db.randomkey()
        if phrase is None:
            phrase = 'no recent results'
        d = {'title':'tuned-resonator curriculum-barnacle test',
        'noun_phrase':phrase}
        self.response = ResponseObject('200','Success', d)
        self.write_response()
        self.finish()