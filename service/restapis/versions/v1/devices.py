
import os
import requests

from flask_restx import Namespace, Resource
from flask_restx.reqparse import RequestParser
from flask_restx import fields


from akit.integration.landscaping.landscape import Landscape

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
        upnp_coord = landscape.upnp_coord

        expected_upnp_devices = landscape.get_upnp_device_configs()

        expected_devices_table = {}

        for exp_dev in expected_upnp_devices:
            exp_usn = exp_dev["upnp"]["USN"]
            expected_devices_table[exp_usn] = exp_dev

        active_devices_table = {}
        inactive_devices_table = {}
        error_devices_table = {}
        other_devices_table = {}

        for child in upnp_coord.children:
            # Convert from a landscape device to the upnp device extension
            child = child.upnp

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
                cinfo["deviceDirect"] = "/devices/" + dmac

            # If this device has a USN_DEV, try to lookup the device in the
            # expected device table, otherwise it is an unexpected device
            if "USN_DEV" in cinfo:
                usn_dev = cinfo["USN_DEV"]
                if usn_dev in expected_devices_table:
                    cinfo["group"] = "expected"
                    expected_devices_table[usn_dev] = cinfo
                    active_devices_table[usn_dev] = cinfo
                else:
                    cinfo["group"] = "other"
                    other_devices_table[usn_dev] = cinfo
            else:
                cinfo["group"] = "error"

        for dinfo in expected_devices_table.values():
            usn_dev = None
            if "USN_DEV" not in dinfo:
                try:
                    upnp=dinfo["upnp"]
                    usn_dev = upnp["USN"]
                    if usn_dev.find("::") > -1:
                        usn_dev, _ = usn_dev.split("::")
                    dinfo["USN"] = usn_dev + "::upnp:rootdevice"
                    dinfo["USN_DEV"] = usn_dev
                    dinfo["USN_CLS"] = "::upnp:rootdevice"
                    if "modelName" in upnp:
                        dinfo["modelName"] = upnp["modelName"]
                    if "modelNumber" in upnp:
                        dinfo["modelNumber"] = upnp["modelNumber"]
                except KeyError:
                    dinfo["group"] = "error"
            else:
                usn_dev = dinfo["USN_DEV"]

            if usn_dev is not None and usn_dev not in active_devices_table:
                dinfo["group"] = "expected"
                inactive_devices_table[usn_dev] = dinfo
            else:
                dinfo["group"] = "error"

        all_devices = []
        all_devices.extend(active_devices_table.values())
        all_devices.extend(error_devices_table.values())
        all_devices.extend(inactive_devices_table.values())
        all_devices.extend(other_devices_table.values())

        for dinfo in all_devices:
            if "modelName" not in dinfo:
                dinfo["modelName"] = "(unknown)"
            if "modelNumber" not in dinfo:
                dinfo["modelNumber"] = "(unknown)"
            if "roomName" not in dinfo:
                dinfo["roomName"] = "(unknown)"
            if "IPAddress" not in dinfo:
                dinfo["IPAddress"] = "(unknown)"
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
        upnp_coord = landscape.upnp_coord

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


@devices_ns.route("/<mac>/files")
class DeviceFiles(Resource):

   def get(self, mac):
        """
            Returns the detailed information about a specific device
        """
        upnp_coord = landscape.upnp_coord

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

            #TODO: Get the devices files using an SSHAgent

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
