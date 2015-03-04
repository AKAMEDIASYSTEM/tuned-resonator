#!/usr/bin/env python

# AKA resonator local curriculum resolver/worker

import beanstalkc
from pattern.web import URL, plaintext

def isValid(line_in):
    # check for jpeg, jpg, gif, js, etc
    # return True if it's a valid url
    if 'Host'==line_in:
        return False
    try:
        p = parse(line_in)
        for n in nixList:
            if p.path.endswith(n):
                return False
            if localhost in p.netloc:
                return False
        return True
    except:
        return False

beanstalk = beanstalkc.Connection(host='localhost', port=14711)
while beanstalk.peek_ready():
	job = beanstalk.reserve()
	print job.body
	# output = open('test_output_redis.txt','w')
	url = URL(job.body)
	if(isValid(job.body)):
	    try:
	        s = url.download(timeout=2500)
	        the_type = url.mimetype
	        if 'text/html'==the_type:
	            s = plaintext(s)
	            # output.write(s.encode('ascii','ignore'))
	            print s
	            c = c+1
	            print c
	    except:
	        print 'timeout on ', url
	# output.close()
	job.delete()
