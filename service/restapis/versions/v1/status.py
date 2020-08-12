
from flask_restplus import Namespace, Resource
from flask_restplus.reqparse import RequestParser

from akit.integration.coordinators.upnpcoordinator import UpnpCoordinator
from akit.integration.landscaping import Landscape

landscape = Landscape()

STATUS_NAMESPACE_PATH = "/status"

status_ns = Namespace("Status v1", description="APIs for obtaining the status of the test node.")

@status_ns.route("/")
class StatusSummary(Resource):

   def get(self):
        """
            Returns a status summary
        """
        upnp_coord = UpnpCoordinator()

        expected_upnp_devices = landscape.get_upnp_devices()

        found_upnp_devices = []

        for child in upnp_coord.children:
            cinfo = child.to_dict(brief=True)
            found_upnp_devices.append(cinfo)

        rtndata = {
            "status": "success",
            "jobs": {
                "current": {
                    "title": "Automation Test Run",
                    "runid": "21ec13f0-f948-4b3e-be55-9341276c93ad",
                    "branch": None,
                    "build": None,
                    "flavor": None,
                    "start": "2020-02-29 19:47:09.180623",
                    "stop": "2020-02-29 19:47:09.216462",
                    "progress": .5,
                    "result": "FAILED",
                    "landscape": None,
                    "detail": {
                        "errors": 0,
                        "failed": 1,
                        "skipped": 0,
                        "passed": 3,
                        "total": 4
                    }
                },
                "prev": {
                    "title": "Automation Test Run",
                    "runid": "3e4269b7-e08a-4cb5-bafd-a8aae79e0e2c",
                    "branch": None,
                    "build": None,
                    "flavor": None,
                    "start": "2020-02-29 19:40:54.160698",
                    "stop": "2020-02-29 19:41:16.630293",
                    "progress": 1.0,
                    "result": "FAILED",
                    "landscape": None,
                    "detail": {
                        "errors": 0,
                        "failed": 1,
                        "skipped": 0,
                        "passed": 3,
                        "total": 4
                    }
                }
            },
            "landscape":{
                "expected": expected_upnp_devices,
                "found": found_upnp_devices
            }
        }

        return rtndata

def publish_namespaces(version_prefix):
    ns_list = [
        (status_ns, "".join([version_prefix, STATUS_NAMESPACE_PATH]))
    ]
    return ns_list
