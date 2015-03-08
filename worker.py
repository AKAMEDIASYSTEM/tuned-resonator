#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext, URLError, MIMETYPE_WEBPAGE, MIMETYPE_PLAINTEXT, HTTPError
from urlparse import urlparse as parse
import sys
import redis



beanstalk = beanstalkc.Connection(host='localhost', port=14711)
c=0
output = open('test_output_redis.txt','w')
while True:
    # take url, add to redis URL store WITH expire time set for EXPIRE_IN seconds.
    # if result of redis INCR command is > 1, it means the URL was already there (but we still updated its TTL)
    # so if result > 1, we should also resolve the url semantically (this should be another beanstalk tube, another job?)
    # resolving the url means, fetch it in pattern and check the mimetype to ensure we only parse text -containing stuff
    # then use pattern to get chunks and noun phrases and shove them in another redis store
    # (where key is the phrase, and value is just INCR?)
    job = beanstalk.reserve()
    url = URL(job.body)
    try:
        # s = url.download(timeout=2500)
        # s = url.download(user_agent='Mozilla/5.0')
        s = url.download(cached=True)
        # the_type = url.mimetype
        print url.mimetype
        if (url.mimetype in MIMETYPE_WEBPAGE) or (url.mimetype in MIMETYPE_PLAINTEXT):
            s = plaintext(s)
            output.write(s.encode('ascii','ignore'))
            # print s.encode('ascii','ignore')
            c = c+1
            print c
        else:
            'we failed the mimetype test again wtf'
    # except URLError, e:
    except HTTPError, e:
        # e = sys.exc_info()[0]
        # print 'URLError on ', url
        print url
        print e
    
    job.delete()
output.close()