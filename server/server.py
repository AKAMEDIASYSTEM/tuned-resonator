#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import tornado.ioloop
import tornado.web
from handlers.BrowserHandler import BrowserHandler
# from handlers.APIHandler import APIHandler

application = tornado.web.Application([
    (r"/", BrowserHandler),
    # (r"/api", APIHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()