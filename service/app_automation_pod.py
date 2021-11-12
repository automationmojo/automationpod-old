
import logging
import os

os.environ["AKIT_SERVICE_NAME"] = "apod"

import akit.environment.service

from akit.coupling.upnpcoordinatorintegration import UpnpCoordinatorIntegration

from akit.integration.landscaping.landscape import Landscape


from flask import Flask, url_for, g
from flask_restx import apidoc

from apod.paths import APodPaths
from apod.restapis import register_rest_blueprints
from apod.website import register_website_blueprints


logger = logging.getLogger("apod")

app = Flask(__name__, template_folder=APodPaths.DIR_TEMPLATES, static_folder=APodPaths.DIR_STATIC)
app.config.SWAGGER_UI_JSONEDITOR = True

#if environment.DEVELOPER_MODE:
#    app.debug = True

# Prevent flask-restplus from registering docs so we
# can customize the route
app.extensions.setdefault("restplus", {
    "apidoc_registered": True
})


# Register the URL route blueprints
register_rest_blueprints(app, "api")
register_website_blueprints(app)

# Setup route redirect for the documentation
redirect_apidoc = apidoc.Apidoc('restplus_doc', apidoc.__name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/api/swaggerui')

@redirect_apidoc.add_app_template_global
def swagger_static(filename):
    static_url = url_for('restplus_doc.static', filename=filename )
    logger.critical("filename: %s" % filename)
    return static_url

@app.teardown_appcontext
def teardown_apoddb(obj):
    session = g.pop('dbsession', None)

    if session is not None:
        session.close()

    return

# When the landscape object is first created, it spins up in configuration
# mode, which allows consumers consume and query the landscape configuration
# information.
lscape = Landscape()

# Give the UpnpCoordinatorIntegration an opportunity to register itself, we are
# doing this in this way to simulate test framework startup.
UpnpCoordinatorIntegration.attach_to_framework(lscape)

# After all the coordinators have had an opportunity to register with the
# 'landscape' object, transition the landscape to the activated 'phase'
lscape.transition_to_activation()

# After we transition the the landscape to the activated phase, we give
# the different coordinators such as the UpnpCoordinatorIntegration an
# opportunity to attach to its environment and determine if the resources
# requested and the resource configuration match
UpnpCoordinatorIntegration.attach_to_environment()

# Finalize the activation process and transition the landscape
# to fully operational mode where all APIs are available.
lscape.transition_to_operational(allow_missing_devices=True)

app.register_blueprint(redirect_apidoc)

# =================================================================
# This main entry point is utilized for debug runs only, when we
# install our service into NGINX and use Green Unicorn, the service
# is launched by Green Unicorn by referencing the 'app' instance in
# this module.
def automation_pod_main():

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host='0.0.0.0', port=8888, debug=False)

    return

if __name__ == "__main__":
    automation_pod_main()
