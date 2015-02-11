#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import logging
import datetime
import tornado
import random
from ResponseObject import ResponseObject

class BrowserHandler(tornado.web.RequestHandler):
    """HTML display of Keywords browsed in the last day"""

    def get(self):
        logging.debug('hit the BrowserHandler endpoint')
        self.response = ResponseObject('200','Success', 'tuned-resonator server test')
        self.write_response()
        self.finish()