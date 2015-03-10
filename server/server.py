#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import tornado.ioloop
import tornado.web
from handlers.BrowserHandler import BrowserHandler
import redis
# from handlers.APIHandler import APIHandler

db = redis.StrictRedis(host='localhost', port=6379, db=1)

settings = dict(
    #template_path=os.path.join(os.path.pardir(__file__), "templates"),
    # template_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'../', 'templates')),
    # static_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'../', "static")),
    debug=True
)

application = tornado.web.Application([
    (r"/api", ApiHandler),
    (r"/", BrowserHandler),
    # (r"/api", APIHandler)
], db=db, **settings)

if __name__ == "__main__":

    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()