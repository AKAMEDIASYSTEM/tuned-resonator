#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext

beanstalk = beanstalkc.Connection(host='localhost', port=14711)
job = beanstalk.reserve()
output = open('test_output_redis.txt','w')
url = URL(job.body)
try:
    s = url.download(timeout=25)
    the_type = url.mimetype
    if 'text/html'==the_type:
        s = plaintext(s)
        output.write(s.encode('ascii','ignore'))
        print line
        c = c+1
        print c
except:
    print 'timeout on ', line

job.delete()
