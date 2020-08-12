
import os

from flask import render_template

from akit.integration.landscaping import Landscape

landscape = Landscape()

def view_configuration():
    template = "configuration_full.html"
    
    podname=landscape.name
    if podname is None:
        podname = "Automation Pod"


    username = "myron.walker"

    return render_template( template, podname=podname, username=username )
