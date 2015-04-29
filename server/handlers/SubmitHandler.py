#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

from handlers.BaseHandler import BaseHandler
from ResponseObject import ResponseObject
import beanstalkc


class SubmitHandler(BaseHandler):
    """json submission to curriculum-insular store"""

    def post(self):
        beanstalk = beanstalkc.Connection(host='localhost', port=14711, parse_yaml=False)
        url = self.get_argument('url', None)
        print 'inside curriculum-insular SubmitHandler', url
        if url is not None:
            try:
                beanstalk.put(str(url))
            except:
                print 'there was a big problem with ', url
        self.response = ResponseObject('200', 'Success')
        self.write_response()
        self.finish()
