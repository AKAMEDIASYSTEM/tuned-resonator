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
        logging.debug('hit the BrowserHandler endpoint')
        self.response = ResponseObject('200','Success', 'tuned-resonator server test')
        self.write_response()
        self.finish()