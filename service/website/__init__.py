
from .views.devices import view_devices, view_devices_control
from .views.home import view_home
from .views.jobs import view_jobs
from .views.results import view_results
from .views.logstore import view_logstore

def register_website_blueprints(app):

    app.add_url_rule('/', 'view_home', view_home)

    app.add_url_rule('/devices', 'view_devices', view_devices)
    app.add_url_rule('/devices/control', 'view_devices_control', view_devices_control)
    app.add_url_rule('/jobs', 'view_jobs', view_jobs)
    app.add_url_rule('/results', 'view_results', view_results)
    app.add_url_rule('/logstore/<path:leafpath>', 'view_logstore', view_logstore)
    
    return
