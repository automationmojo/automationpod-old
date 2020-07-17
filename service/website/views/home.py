import os

from flask import render_template

def view_home():
    template = "home_full.html"

    username = "myron.walker"

    return render_template(template, username=username )
