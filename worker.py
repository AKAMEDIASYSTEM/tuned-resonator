#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext, URLError, MIMETYPE_WEBPAGE, MIMETYPE_PLAINTEXT
from urlparse import urlparse as parse


beanstalk = beanstalkc.Connection(host='localhost', port=14711)
while beanstalk.peek_ready():
    job = beanstalk.reserve()
    output = open('test_output_redis.txt','w')
    # print url
    url = URL(job.body)
    try:
        # s = url.download(timeout=2500)
        s = url.download(cache=True,timeout=100)
        the_type = url.mimetype
        print the_type
        if url.mimetype==MIMETYPE_WEBPAGE or url.mimetype==MIMETYPE_PLAINTEXT:
            s = plaintext(s)
            output.write(s.encode('ascii','ignore'))
            print s
            c = c+1
            print c
    except URLError, e:
        # print 'URLError on ', url
        print e
    output.close()
    job.delete()
