#!/usr/bin/env python
 
## Tiny Syslog Server in Python.
## from a rad gist at https://gist.github.com/marcelom/4218010
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.
 
LOG_FILE = 'remote_aka.log'
HOST, PORT = "192.168.1.2", 514

# import logging
import SocketServer
import beanstalkc
from urlparse import urlparse as parse
from collections import Counter

nixList = ['png','jpeg','jpg','css','js','ipa','ico','gif','mov','mp4','svg','json','woff','woff2','pdf','mp3','crl','webp','jsonp'
'PNG','JPEG','JPG','CSS','JS','IPA','ICO','GIF','MOV','MP4','SVG','JSON','WOFF','WOFF2','PDF','MP3','CRL','WEBP','JSONP']
local_host = '192.168.1.1'
cnt = Counter()

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
            if local_host in p.netloc:
                return False
            if 'gravatar.com' in p.netloc: # this domain is just nasty, all infinite redirects and fury, signifying nothing
                return False
        cnt[line_in] += 1
        if cnt[line_in] >1:
            return False
        return True
    except:
        return False

# logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')
 
class SyslogUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        if 'trans Host GET' in str(data):
            url = str(data).split(' ')[-3]
            if isValid(url):
                beanstalk.put(url)
                print(url)
            else:
                pass
        # logging.info(str(data))
 
if __name__ == "__main__":
    beanstalk = beanstalkc.Connection(host='localhost', port=14711)
    try:
        server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")