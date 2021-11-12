
import os

import requests

from akit.xlogging.foundations import getAutomatonKitLogger

from apod.paths import APodPaths

logger = getAutomatonKitLogger()

def try_download_icon_to_cache(cache_dir, icon_url, url_base=None):

    try:
        ext_cache_dir = cache_dir

        icon_url_parts = icon_url.split("/")
        if len(icon_url_parts) > 1:
            ext_cache_dir = os.path.join(cache_dir, *icon_url_parts[:-1])

        if not os.path.exists(ext_cache_dir):
            os.makedirs(ext_cache_dir)

        cache_filename = os.path.join(APodPaths.DIR_STATIC, "images", "cached", *icon_url_parts)
        if not os.path.exists(cache_filename):
            full_url = icon_url
            if url_base is not None:
                full_url = url_base + icon_url

            resp = requests.get(full_url)
            if resp.status_code == 200:
                with open(cache_filename, 'wb') as iconf:
                    iconf.write(resp.content)
    except:
        logger.error("Error downloading file.")

    return
