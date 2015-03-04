#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext, URLError, MIMETYPE_WEBPAGE, MIMETYPE_PLAINTEXT, HTTPError
from urlparse import urlparse as parse
import sys


beanstalk = beanstalkc.Connection(host='localhost', port=14711)
c=0
while beanstalk.peek_ready():
    job = beanstalk.reserve()
    output = open('test_output_redis.txt','w')
    # print url
    url = URL(job.body)

    try:
        # s = url.download(timeout=2500)
        # s = url.download(user_agent='Mozilla/5.0')
        s = url.download(cache=True)
        # the_type = url.mimetype
        print url.mimetype
        if (url.mimetype in MIMETYPE_WEBPAGE) or (url.mimetype in MIMETYPE_PLAINTEXT):
            s = plaintext(s)
            output.write(s.encode('ascii','ignore'))
            # print s.encode('ascii','ignore')
            c = c+1
            print c
            output.close()
        else:
            'we failed the mimetype test again wtf'
            output.close()
    # except URLError, e:
    except HTTPError, e:
        # e = sys.exc_info()[0]
        # print 'URLError on ', url
        print e
        output.close()
    
    job.delete()
