import os

from flask import render_template

def view_results():
    template = "results_full.html"

    username = "myron.walker"

    return render_template(template, username=username )
