#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext, URLError, MIMETYPE_WEBPAGE, MIMETYPE_PLAINTEXT, HTTPError
from urlparse import urlparse as parse
import sys
import redis

EXPIRE_IN = 10800 # this is 3 hours in seconds

beanstalk = beanstalkc.Connection(host='localhost', port=14711)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
c=0 # debug counter
# output = open('test_output_redis.txt','w') # deprecated, was for debug


while True:
    # take url, add to redis URL store WITH expire time set for EXPIRE_IN seconds.
    # if result of redis INCR command is > 1, it means the URL was already there (but we still updated its TTL)
    # so if result > 1, we should also resolve the url semantically (this should be another beanstalk tube, another job?)
    # resolving the url means, fetch it in pattern and check the mimetype to ensure we only parse text -containing stuff
    # then use pattern to get chunks and noun phrases and shove them in another redis store
    # (where key is the phrase, and value is just INCR?)

    job = beanstalk.reserve() # this is blocking, waits till there's something on the stalk
    url = URL(job.body)
    pipe = r.pipeline(transaction=True)
    redis_response = pipe.incr(url).expire(url, EXPIRE_IN).execute()
    print redis_response
    isThere = redis_response[0]
    print 'trying', url
    # isThere = r.incr(url) # upsert; if great than 1, URL is 'new'
    print 'new entry in DB', url if(isThere<2) else print 'already seen this url'

    if(isThere < 2):
        print 'new url, we think', url
        try:
            s = url.download(cached=True)
            print url.mimetype
            if (url.mimetype in MIMETYPE_WEBPAGE) or (url.mimetype in MIMETYPE_PLAINTEXT):
                s = plaintext(s)
                # do noun phrase extraction, add to redis store
                # output.write(s.encode('ascii','ignore')) # deprecated, was for debug
                # print s.encode('ascii','ignore')
                c = c+1
                print c
            else:
                'we failed the mimetype test again wtf'
        except HTTPError, e:
            # e = sys.exc_info()[0]
            # print 'URLError on ', url
            print url
            print e
        # end of if(isThere < 2)
    job.delete()
# output.close()