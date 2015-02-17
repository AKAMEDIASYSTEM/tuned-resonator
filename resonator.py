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

localhost = '192.168.1.1'
local_url = '192.168.0.113'
hostname = 'bender.local'
# dump log to temp file (should also wipe log at this point to avoid overflow?)
# call(['cat', "/var/log/remote_aka.log | grep 'trans Host GET' > ~/tuned-resonator/tempGrep.txt"])
# call(["echo", "777 > /var/log/remote_aka.log"]) # deprecate this for now while testing
os.system(" cat /var/log/remote_aka.log | grep 'trans Host GET' > ~/tuned-resonator/tempGrep.txt")
nixList = ['png','jpeg','jpg','css','js','ipa','ico','gif','mov','mp4','svg','json','woff','woff2']

def isValid(line_in):
    # check for jpeg, jpg, gif, js, etc
    # return True if it's a valid url
    for suffix in nixList:
        if line_in.split('.')[-1]==suffix:
            return False
    if '?' in line_in:
        for suffix in nixList:
            line_in = line_in.split('?')[0]
            if line_in.split('.')[-1]==suffix:
                return False
    # check for localhost pages
    if localhost in line_in:
        return False
    if 'Host'==line_in:
        return False
    return True

with open('tempGrep.txt') as f:
    content = f.readlines()
    k = [line.split(' ')[-3] for line in content]
    # print k

# k = [i for i in k if i.split('.')[-1]=='jpg'] # all jpgs
# k = [i for i in k if i.split('.')[-1]!='jpg' and i.split('.')[-1]!='png' and i.split('.')[-1]!='js' and i.split('.')[-1]!='ico' and localhost not in i]
urls = [i for i in k if isValid(i)]

for url in urls:
    # print url
    try: 
        text = v2.extract(url)
        print text.encode('ascii','ignore')
    except:
        pass
    print '\n\n\n\n'



# with open('tempGrep.txt') as f:
    # content = f.readlines()
    # for line in content:
    #     last = line.split(' ')
    #     print last[-3] ## this is the URL tinyproxy reports


# create XML to update the resonator.service file
# this should update the .service file with recent data but idk what yet
# maybe last three topics or something?
'''
root = objectify.Element('service-group')
t_name = objectify.SubElement(root, 'name')
t_name.attrib['replace-wildcards'] = 'yes'
# t_name._setText('http://akamediasystem.com?total=%s' % a)
t_name._setText('http://192.168.0.113/?state=%s' % a)
t_service = objectify.SubElement(root, 'service')
tt_hostname = objectify.SubElement(t_service, 'host-name')
tt_hostname._setText(hostname)
tt_type = objectify.SubElement(t_service, 'type')
tt_type._setText('_http._tcp')
tt_port = objectify.SubElement(t_service, 'port')
tt_port._setText('80')
tt_txtrecord = objectify.SubElement(t_service, 'txt-record')
tt_txtrecord._setText('path=/?state=%s' % a)
objectify.deannotate(root, cleanup_namespaces=True)
s = '<?xml version="1.0" standalone="no"?><!--*-nxml-*--><!DOCTYPE service-group SYSTEM "avahi-service.dtd">'+etree.tostring(root, pretty_print=True)
# print s
f = open('/etc/avahi/services/resonator-avahi.service', 'w')
f.write(s)
f.close()
'''
# here we could also update the <meta> properties of the local website


'''
from google's repo:
The Physical Web is about getting URLs into the physical world.
However, this isn't limited to just Bluetooth Low Energy (BLE) beacons.
mDNS is a service broadcast technique used in Wifi networks.
It has a two advantages over BLE:

Only people logged into your wifi can see the mDNS URLs. This means that in an appartment, your neighbors can't see your devices.
It doesn't have the length restrictions of BLE has so a URL can be along as you'd like (well, at least up to 100 characters).
Below is an example of how to setup a Raspberry Pi to broadcast a Physical Web URL using mDNS. We hope others are willing to contribute and offer more versions.
If so, we'll create an mDNS directory for all the alternatives.

You'll first need a mDNS service on your RPi. Avahi is the one we use here: $ sudo apt-get install avahi-daemon

You'll then place a '.service' file into the /etc/avahi/services directory. Our sample file 'physical-web-url.service' looks like this:

<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">http://www.mycompany.com/xyz.html</name>
  <service>
    <host-name>www.mycompany.com</host-name>
    <type>_http._tcp</type>
    <port>80</port>
    <txt-record>path=/xyz.html</txt-record>
  </service>
</service-group>
Then <name> tag must be unique on your network. 
We are suggesting that you use the URL as your name to be safe.
That should be it.
If you have the latest client on your phone, the web page http://www.mycompany.com/xyz.html will now show up in your list of nearby devices.
Note: the iOS app supports mDNS, but not the Android app yet.
It will be updated within a few days for Android 5.0 devices.
If people are stuck on older versions, please let us know (or feel free add it yourself ;-)

'''
