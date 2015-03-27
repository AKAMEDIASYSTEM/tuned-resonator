#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

import tornado.ioloop
import tornado.web
from handlers.BrowserHandler import BrowserHandler
from handlers.ApiHandler import ApiHandler
import redis

settings = {'debug':True}
db = redis.StrictRedis(host='localhost', port=6379, db=1)

application = tornado.web.Application([
    (r"/api", ApiHandler),
    (r"/", BrowserHandler),
], db=db, **settings)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()