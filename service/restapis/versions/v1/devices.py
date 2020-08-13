
import os
import requests

from flask_restplus import Namespace, Resource
from flask_restplus.reqparse import RequestParser
from flask_restplus import fields


from akit.integration.landscaping import Landscape
from akit.integration.coordinators.upnpcoordinator import UpnpCoordinator

landscape = Landscape()

DEVICES_NAMESPACE_PATH = "/devices"

devices_ns = Namespace("Devices v1", description="")

from website import static as static_module

DIR_STATIC = os.path.dirname(static_module.__file__)

def try_download_icon_to_cache(cache_dir, icon_url, url_base=None):

    try:
        ext_cache_dir = cache_dir

        icon_url_parts = icon_url.split("/")
        if len(icon_url_parts) > 1:
            ext_cache_dir = os.path.join(cache_dir, *icon_url_parts[:-1])

        if not os.path.exists(ext_cache_dir):
            os.makedirs(ext_cache_dir)

        cache_filename = os.path.join(DIR_STATIC, "images", "cached", *icon_url_parts)
        if not os.path.exists(cache_filename):
            full_url = icon_url
            if url_base is not None:
                full_url = url_base + icon_url

            resp = requests.get(full_url)
            if resp.status_code == 200:
                with open(cache_filename, 'wb') as iconf:
                    iconf.write(resp.content)
    except:
        print("Error downloading file.")

    return

@devices_ns.route("/")
class AllDevicesCollection(Resource):

   def get(self):
        """
            Returns a list of devices
        """
        upnp_coord = UpnpCoordinator()

        expected_upnp_devices = landscape.get_upnp_devices()

        expected_devices_table = {}

        for exp_dev in expected_upnp_devices:
            exp_usn = exp_dev["USN"]
            expected_devices_table[exp_usn] = exp_dev

        other_devices = []
        for child in upnp_coord.children:

            # Get a dictionary representation of the device
            cinfo = child.to_dict(brief=True)

            # Get and cache the icon for the device, or assign the unknown device icon
            firstIcon = cinfo.get("firstIcon", None)
            if firstIcon is not None:
                icon_url = firstIcon["url"]
                replacement_url = "/static/images/cached/" + icon_url.lstrip("/")
                cinfo["cachedIcon"] = replacement_url

                cache_dir = os.path.join(DIR_STATIC, "images", "cached")
                url_base = cinfo.get("URLBase", None)
                try_download_icon_to_cache(cache_dir, icon_url, url_base=url_base)
            else:
                cinfo["cachedIcon"] = "/static/images/unknown.png"

            if "MACAddress" in cinfo:
                dmac = cinfo["MACAddress"].replace(":", "").upper()
                cinfo["deviceDirect"] = "/devices/direct/" + dmac + "/status"

            # If this device has a USN, try to lookup the device in the
            # expected device table, otherwise it is an unexpected device
            if "USN" in cinfo:
                usn = cinfo["USN"]
                if usn in expected_devices_table:
                    cinfo["group"] = "expected"
                    expected_devices_table[usn] = cinfo
                else:
                    cinfo["group"] = "other"
                    other_devices.append(cinfo)
            else:
                cinfo["group"] = "other"
                other_devices.append(cinfo)

        all_devices = []
        all_devices.extend(expected_devices_table.values())
        all_devices.extend(other_devices)

        for dinfo in other_devices:
            if "MACAddress" not in dinfo:
                dinfo["MACAddress"] = "(unknown)"
            if "softwareVersion" not in dinfo:
                dinfo["softwareVersion"] = "(unknown)"
            if "household" not in dinfo:
                dinfo["household"] = "(unknown)"

        rtndata = {
            "status": "success",
            "items": all_devices
        }

        return rtndata

@devices_ns.route("/<mac>")
class DeviceDetail(Resource):

   def get(self, mac):
        """
            Returns the detailed information about a specific device
        """
        upnp_agent = UpnpCoordinator()

        rtndata = {
            "status": "failed"
        }

        found_child = None
        for child in upnp_coord.children:
            cinfo = child.to_dict(brief=True)

            if "MACAddress" in cinfo:
                cmac = cinfo["MACAddress"]
                if mac == cmac:
                    found_child = child

        if found_child is not None:
            found_dev = found_child.to_dict(brief=False)
            firstIcon = found_dev.get("firstIcon", None)
            if firstIcon is not None:
                icon_url = firstIcon["url"]
                replacement_url = "/static/images/cached/" + icon_url.lstrip("/")
                found_dev["cachedIcon"] = replacement_url


                cache_dir = os.path.join(DIR_STATIC, "images", "cached")
                url_base = found_dev.get("URLBase", None)
                try_download_icon_to_cache(cache_dir, icon_url, url_base=url_base)
            else:
                found_dev["cachedIcon"] = "/static/images/unknowndevice.png"

            rtndata = {
                "status": "success",
                "device": found_dev
            }

        return rtndata


devices_multi_invoke_model = devices_ns.model("DevicesMultiInvokePacket", {
        "packet": fields.Raw(required=True, description="The invoke packet to use on the devices.")
    })

@devices_ns.route("/multi-invoke")
class DevicesMultiInvoke(Resource):

    @devices_ns.expect(devices_multi_invoke_model)
    def post(self):
        return




def publish_namespaces(version_prefix):
    ns_list = [
        (devices_ns, "".join([version_prefix, DEVICES_NAMESPACE_PATH]))
    ]
    return ns_list
