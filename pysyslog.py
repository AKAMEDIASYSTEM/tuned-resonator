#!/usr/bin/env python
 
## Tiny Syslog Server in Python.
## from a rad gist at https://gist.github.com/marcelom/4218010
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.
 
LOG_FILE = 'remote_aka.log'
HOST, PORT = "192.168.1.2", 514
 
#
# NO USER SERVICEABLE PARTS BELOW HERE...
#
 
# import logging
import SocketServer
 
# logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')
 
class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        if 'trans Host GET' in str(data):
            url = str(data).split(' ')[-3]
            print(url)
        # logging.info(str(data))
 
if __name__ == "__main__":
    try:
        server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")