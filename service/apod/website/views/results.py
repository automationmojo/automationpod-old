import os

from flask import render_template

from akit.interop.landscaping.landscape import Landscape

landscape = Landscape()

def view_results():
    template = "results_full.html"

    podname=landscape.name
    if podname is None:
        podname = "Automation Pod"

    username = "myron.walker"

    return render_template(template, podname=podname, username=username )
