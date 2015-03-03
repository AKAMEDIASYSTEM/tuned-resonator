#!/usr/bin/env python
# tuned-resonator
# experiments with google physical-web mdns broadcast

'''
02/2015 revisit; this will now attempt to parse logfiles from tinyproxy

copy logfile into local/temp file
wipe logfile so it can be refilled
open tempfile
extract all urls form tempfile
throw away all urls that end in .[png, svg, gif, jpeg, js, ipa, css] - make this case-insensitive
'''

'''
sigh, better strategy:
tail the logfile from within python http://stackoverflow.com/questions/12523044/how-can-i-tail-a-log-file-in-python
for each incoming line from tail, test to see if it contains actionable URL (same grep pattern, maybe, as we use now)

tail -f /var/log/remote_aka.log | grep 'trans Host GET' | xargs curl localhost:8080 -d'{}'

tail the logfile (or use https://gist.github.com/marcelom/4218010 to skip syslog and have python accept UDP log messages)

for each incoming message, filter out messages without actionable URLs 

for each actionable URL, send just the URL to a queue, perhaps bitly simplehttp https://github.com/bitly/simplehttp or beanstalk

SEPARATELY, python workers are spawned to handle stuff on the queue.

Each worker gets a URL.
Using pattern.web, we resolve the URL and if it's mimetype FOO (e.g., text/html and text/plaintext) we do patter.web.plaintext()
THEN: results of pattern.web.plaintext go into redis with appropriate TTL?
OR: results of plaintext get chunked+parsed and noun phrases go into redis, with appropriate TTL

SEPARATELY STILL,
a tornado server lives on the subnet and serves out noun phrases in a manner similar to current curriculum (ie, query for X phrases from up to Y seconds ago)




'''

from lxml import etree
from lxml import objectify
import requests
# import keys
# import feedparser
import json
from subprocess import call
import eatiht.v2 as v2
import os
import time
from urlparse import urlparse as parse
import nltk
# from nltk.corpus import brown
import pattern.web

localhost = '192.168.1.1'
local_url = '192.168.0.113'
hostname = 'bender.local'
# don't make fun, this was just waaaaay quicker than making this really case-insensitive
nixList = ['png','jpeg','jpg','css','js','ipa','ico','gif','mov','mp4','svg','json','woff','woff2','pdf','mp3','crl','webp','jsonp'
'PNG','JPEG','JPG','CSS','JS','IPA','ICO','GIF','MOV','MP4','SVG','JSON','WOFF','WOFF2','PDF','MP3','CRL','WEBP','JSONP']

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

# dump log to temp file (should also wipe log at this point to avoid overflow?)
# call(['cat', "/var/log/remote_aka.log | grep 'trans Host GET' > ~/tuned-resonator/tempGrep.txt"])
# deprecate this for now while testing
# os.system('echo > /var/log/remote_aka.log')

print 'processing /var/log/remote_aka.log'

print os.system("cat /var/log/remote_aka.log | grep 'trans Host GET' > /root/tuned-resonator/tempGrep.txt")
print 'done processing /var/log/remote_aka.log into tempGrep.txt'

print os.system('echo > /var/log/remote_aka.log')
print 'wiped /var/log/remote_aka.log so now do not lose tempGrep.txt'

with open('tempGrep.txt') as f:
    # urls are reliably 3rd from last thing in line
    # here's a sample log line
    # Feb 18 11:50:27 tuned-resonator.local tinyproxy[12452]: process_request: trans Host GET http://www.tutorialspoint.com:80/favicon.ico for 1
    k = [line.split(' ')[-3] for line in f]

urls = [i for i in k if isValid(i)]
# remove duplicate URLS
urls = [u for u in set(urls)]

# this is just for debug; export all urls so you can check for junk
url_out = open('test_urls.txt','w')
for url in urls:
    url_out.write(url)
    url_out.write('\n')
url_out.close()

# dump output of all pages to file (should I shove these in a db?)
output = open('test_output.txt','w')
for url in urls:
    # print url
    try: 
        text = v2.extract(url)
        output.write(text.encode('ascii','ignore'))
        output.write('\n')
        # print '\n\n\n\n'
    except:
        pass
output.close()
print 'finished running at ', time.strftime("%a, %d %b %Y %H:%M:%S")

