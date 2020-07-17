import os

from flask import render_template

def view_jobs():
    template = "jobs_full.html"

    username = "myron.walker"

    return render_template(template, username=username )
