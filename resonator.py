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
from nltk.corpus import brown

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

url_out = open('test_urls.txt','w')
for url in urls:
    url_out.write(url)
    url_out.write('\n')
url_out.close()

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

