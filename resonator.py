#!/usr/bin/env python
# tuned-resonator curriculum-barnacle
# experiments with google physical-web mdns broadcast

'''
03/2015
this runs regularly and updates the curriculum-barnacle's exposure to users of Google Physical-Web
it queries a random term from recent browsing and updates the .service file that avahi uses to serve out mDNS info
'''

from lxml import etree
from lxml import objectify
import redis
import re

hn = open('/etc/hostname')
hostname = hn.readline()[:-1]+'.local' # drop triailing newline
hostname_text = 'http://'+hostname
r_text = redis.StrictRedis(host='localhost', port=6379, db=1)
zeitgeist = r_text.randomkey()
if zeitgeist is None:
    zeitgeist = 'redis is unavailable!'
# here zeitgeist should be made XML-compliant via a truly opaque regex because:XML is nasty
# create XML
root = objectify.Element('service-group')
t_name = objectify.SubElement(root, 'name')
t_name.attrib['replace-wildcards'] = 'yes'
t_name._setText(hostname_text)
t_service = objectify.SubElement(root, 'service')
tt_hostname = objectify.SubElement(t_service, 'host-name')
tt_hostname._setText(hostname)
tt_type = objectify.SubElement(t_service, 'type')
tt_type._setText('_http._tcp')
tt_port = objectify.SubElement(t_service, 'port')
tt_port._setText('80')
tt_txtrecord = objectify.SubElement(t_service, 'txt-record')
d = 'path=/'+zeitgeist
re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+', '', d)
tt_txtrecord._setText(d)
objectify.deannotate(root, cleanup_namespaces=True)
s = '<?xml version="1.0" standalone="no"?><!--*-nxml-*--><!DOCTYPE service-group SYSTEM "avahi-service.dtd">'+etree.tostring(root, pretty_print=True)
# print s
f = open('/etc/avahi/services/resonator-avahi.service', 'w')
f.write(s)
f.close()

