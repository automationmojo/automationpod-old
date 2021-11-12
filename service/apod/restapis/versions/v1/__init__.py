
from flask_restx import Api, Namespace

VERSION_INTEGER = 1

VERSION_NAMESPACE_PATH = "/%d" % VERSION_INTEGER

API_TITLE = "Automation Pod"

from apod.restapis.versions.v1.devices import publish_namespaces as devices_publish_namespaces
from apod.restapis.versions.v1.jobqueue import publish_namespaces as jobqueue_publish_namespaces
from apod.restapis.versions.v1.landscape import publish_namespaces as landscape_publish_namespaces
from apod.restapis.versions.v1.results import publish_namespaces as results_publish_namespaces
from apod.restapis.versions.v1.status import publish_namespaces as status_publish_namespaces

def apply_namespaces(bp):

    api = Api(bp,
        title="%s APIs" % API_TITLE,
        version="%d.0" % VERSION_INTEGER,
        description="These APIs can be utilized to interact with the %s system." % API_TITLE,
        doc="/%d/doc" % VERSION_INTEGER)

    ver_ns = Namespace('v%d_base' % VERSION_INTEGER, description="The %s API v%d" % (API_TITLE, VERSION_INTEGER))
    api.add_namespace(ver_ns, VERSION_NAMESPACE_PATH)

    for ns_obj, ns_path in devices_publish_namespaces(VERSION_NAMESPACE_PATH):
        api.add_namespace(ns_obj, ns_path)
    
    for ns_obj, ns_path in jobqueue_publish_namespaces(VERSION_NAMESPACE_PATH):
        api.add_namespace(ns_obj, ns_path)

    for ns_obj, ns_path in landscape_publish_namespaces(VERSION_NAMESPACE_PATH):
        api.add_namespace(ns_obj, ns_path)

    for ns_obj, ns_path in results_publish_namespaces(VERSION_NAMESPACE_PATH):
        api.add_namespace(ns_obj, ns_path)

    for ns_obj, ns_path in status_publish_namespaces(VERSION_NAMESPACE_PATH):
        api.add_namespace(ns_obj, ns_path)

    return