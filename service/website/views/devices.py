import os

import requests

from flask import request, render_template, Response

from akit.integration.landscaping import Landscape
from akit.integration.agents.upnpagent import UpnpAgent

landscape = Landscape()

def normalize_mac_address(mac):
    tbrief = mac.replace(":", "")
    mac = "%s%s:%s%s:%s%s:%s%s:%s%s:%s%s" % (
        tbrief[0],
        tbrief[1],
        tbrief[2],
        tbrief[3],
        tbrief[4],
        tbrief[5],
        tbrief[6],
        tbrief[7],
        tbrief[8],
        tbrief[9],
        tbrief[10],
        tbrief[11])
    return mac

def view_devices():
    template = "devices_full.html"
    
    podname=landscape.name
    if podname is None:
        podname = "Automation Pod"


    username = "myron.walker"

    return render_template(template, podname=podname, username=username )

def view_devices_control():
    template = "devices_full_control.html"

    podname=landscape.name
    if podname is None:
        podname = "Automation Pod"

    username = "myron.walker"

    devices = request.form['devices']

    return render_template(template, podname=podname, devices_ids=devices, username=username)

def view_devices_direct_review_js(target):
    username = "myron.walker"

    upnp_agent = UpnpAgent()

    target_norm = normalize_mac_address(target)

    found_child = None
    for child in upnp_agent.children:
        if target_norm == child.MACAddress:
            found_child = child
            break

    devresp = None
    if found_child is not None:
        deviceip = found_child.IPAddress
        deviceurl = "http://%s:1400/review.js" % (deviceip,)
        resp = requests.get(deviceurl)
        headers = {}
        for hkey, hval in resp.headers.items():
            headers[hkey] = hval
        content = resp.content
        devresp = Response(content, headers=headers)

    return devresp

def view_devices_direct_status(target, targeturl=None):

    username = "myron.walker"

    upnp_agent = UpnpAgent()

    if targeturl is None:
        targeturl = "status"
    else:
        targeturl = "status/%s" % targeturl

    target_norm = normalize_mac_address(target)

    found_child = None
    for child in upnp_agent.children:
        if target_norm == child.MACAddress:
            found_child = child
            break

    devresp = None
    if found_child is not None:
        deviceip = found_child.IPAddress
        deviceurl = "http://%s:1400/%s" % (deviceip, targeturl)
        resp = requests.get(deviceurl)
        headers = {}
        for hkey, hval in resp.headers.items():
            headers[hkey] = hval
        content = resp.content
        content = content.replace(b"href=\"/", b"href=\"/devices/direct/" + target.encode('utf-8') + b"/")
        content = content.replace(b"href=/", b"href=/devices/direct/" + target.encode('utf-8') + b"/")
        content = content.replace(b"src=\"/", b"src=\"/devices/direct/" + target.encode('utf-8') + b"/")
        devresp = Response(content, headers=headers)

    return devresp

def view_devices_direct_xml(target, targeturl):

    username = "myron.walker"

    upnp_agent = UpnpAgent()

    target_norm = normalize_mac_address(target)

    found_child = None
    for child in upnp_agent.children:
        if target_norm == child.MACAddress:
            found_child = child
            break

    devresp = None
    if found_child is not None:
        deviceip = found_child.IPAddress
        deviceurl = "http://%s:1400/xml/%s" % (deviceip, targeturl)
        resp = requests.get(deviceurl)
        headers = {}
        for hkey, hval in resp.headers.items():
            headers[hkey] = hval
        content = resp.content
        content = content.replace(b"href=\"/", b"href=\"/devices/direct/" + target.encode('utf-8') + b"/")
        content = content.replace(b"href=/", b"href=/devices/direct/" + target.encode('utf-8') + b"/")
        content = content.replace(b"src=\"/", b"src=\"/devices/direct/" + target.encode('utf-8') + b"/")
        devresp = Response(content, headers=headers)

    return devresp