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
        minutes = self.get_argument('t')
        db = self.settings['db']
        logging.debug('hit the BrowserHandler endpoint with t=', t)
        phrase = db.randomkey()
        d = {'title':'tuned-resonator curriculum-barnacle test',
        'noun_phrase':phrase}
        self.response = ResponseObject('200','Success', d)
        self.write_response()
        self.finish()