
import os
import requests

from flask_restx import Namespace, Resource
from flask_restx.reqparse import RequestParser
from flask_restx import fields


from akit.integration.landscaping.landscape import Landscape

from apod.paths import APodPaths
from apod.web import try_download_icon_to_cache

landscape = Landscape()

LANDSCAPE_NAMESPACE_PATH = "/landscape"

landscape_ns = Namespace("Landscape v1", description="")

@landscape_ns.route("/")
class Landscape(Resource):

    linux_client_icon_url = "static/images/linuxclient.png"
    windows_client_icon_url = "static/images/windowsclient.png"
    
    unknown_icon_url = "/static/images/unknown.png"        
    
    def get(self):
        """
            Returns a list of devices
        """
        
        icon_lookup = {}

        upnp_coord = landscape.upnp_coord
        for child in upnp_coord.children:

            try:
                # Convert from a landscape device to the upnp device extension
                child = child.upnp
                child_usn = child.USN_DEV

                # Get a dictionary representation of the device
                cinfo = child.to_dict(brief=True)

                # Get and cache the icon for the device, or assign the unknown device icon
                firstIcon = cinfo.get("firstIcon", None)
                if firstIcon is not None:
                    icon_url = firstIcon["url"]
                    replacement_url = "/static/images/cached/" + icon_url.lstrip("/")
                    cinfo["cachedIcon"] = replacement_url

                    cache_dir = os.path.join(APodPaths.DIR_STATIC, "images", "cached")
                    url_base = cinfo.get("URLBase", None)
                    try_download_icon_to_cache(cache_dir, icon_url, url_base=url_base)

                    icon_lookup[child_usn] = replacement_url
                else:
                    cinfo["cachedIcon"] = self.unknown_icon_url
                    icon_lookup[child_usn] = self.unknown_icon_url
            except:
                pass

        lsinfo = landscape.landscape_info

        if "pod" in lsinfo:
            pod = lsinfo["pod"]
            if "devices" in pod:
                device_list = pod["devices"]

                for nxtdev in device_list:
                    icon_url = self.unknown_icon_url

                    device_type = nxtdev["deviceType"]
                    if device_type == "network/upnp":
                        dev_usn = nxtdev["upnp"]["USN"]
                        if dev_usn in icon_lookup:
                            icon_url = icon_lookup[dev_usn]

                    elif device_type == "network/ssh":
                        if "platform" in nxtdev:
                            platform = nxtdev["platform"].lower()
                            if platform == "linux":
                                icon_url = self.linux_client_icon_url

                    nxtdev["cachedIcon"] = icon_url

        return lsinfo


def publish_namespaces(version_prefix):
    ns_list = [
        (landscape_ns, "".join([version_prefix, LANDSCAPE_NAMESPACE_PATH]))
    ]
    return ns_list
