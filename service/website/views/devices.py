import os

from flask import request, render_template

def view_devices():
    template = "devices_full.html"

    username = "myron.walker"

    return render_template(template, username=username )

def view_devices_control():
    template = "devices_full_control.html"

    username = "myron.walker"

    devices = request.form['devices']

    return render_template(template, devices_ids=devices, username=username)