
import re

from werkzeug.routing import BaseConverter, Rule
from werkzeug.exceptions import InternalServerError

from .views.configuration import view_configuration

from .views.devices import view_devices
from .views.devices import view_devices_control
from .views.devices import view_devices_direct_review_js
from .views.devices import view_devices_direct_status
from .views.devices import view_devices_direct_xml

from .views.home import view_home
from .views.jobs import view_jobs
from .views.results import view_results
from .views.logstore import view_logstore

class RegExConverter(BaseConverter):
    def __init__(self, url_map, exp=None, errmsg="Invalid "):
        super(RegExConverter, self).__init__(url_map)
        self.expression = re.compile(exp)
        self.errmsg = errmsg
        return

    def to_python(self, value):
        match = self.expression.match(value)
        if match is None:
            raise InternalServerError(self.errmsg)
        return value

    def to_url(self, value):
        return value

def register_website_blueprints(app):

    app.url_map.converters['regex'] = RegExConverter

    app.add_url_rule('/', 'view_home', view_home)

    app.add_url_rule('/configuration', 'view_configuration', view_configuration)
    app.add_url_rule('/devices', 'view_devices', view_devices)
    app.add_url_rule(
        '/devices/direct/<regex(exp="[A-F0-9]{12}", errmsg="Invalid MAC address passed as device id."):target>/review.js',
        'view_devices_direct_review_js', 
        view_devices_direct_review_js)
    app.add_url_rule(
        '/devices/direct/<regex(exp="[A-F0-9]{12}", errmsg="Invalid MAC address passed as device id."):target>/status',
        'view_devices_direct_status', 
        view_devices_direct_status)
    app.add_url_rule(
        '/devices/direct/<regex(exp="[A-F0-9]{12}", errmsg="Invalid MAC address passed as device id."):target>/status/<path:targeturl>',
        'view_devices_direct_status', 
        view_devices_direct_status)
    app.add_url_rule(
        '/devices/direct/<regex(exp="[A-F0-9]{12}", errmsg="Invalid MAC address passed as device id."):target>/xml/<path:targeturl>',
        'view_devices_direct_xml', 
        view_devices_direct_xml)
    app.add_url_rule('/devices/control', 'view_devices_control', view_devices_control)
    app.add_url_rule('/jobs', 'view_jobs', view_jobs)
    app.add_url_rule('/results', 'view_results', view_results)
    app.add_url_rule('/logstore/<path:leafpath>', 'view_logstore', view_logstore)
    
    return
