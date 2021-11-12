
import json
import os
import time

from akit.environment.context import Context

from flask import Response, render_template, request

context = Context()

TEMPLATE_LISTING_ROW = '<tr valign="top"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
TEMPLATE_MD_ICON = '<i class="material-icons">%s</i>'
TEMPLATE_BS_ICON = '<b-icon icon="%s"></b-icon>'
TEMPLATE_LINK = '<a href="%s">%s</a>'

DIR_RESULTS = os.path.expanduser(context.lookup("/environment/configuration/paths/results"))

MIME_TYPES = {
    ".css": "text/css",
    ".html": "text/html",
    ".log": "text/plain",
    ".js": "application/javascript",
    ".json": "application/json",
    ".jsos": "application/json",
    ".txt": "text/plain"
}

TABLE_MD_ICON = {
    ".css": TEMPLATE_BS_ICON % "file-code",
    ".html": TEMPLATE_BS_ICON % "file-code",
    ".log": TEMPLATE_BS_ICON % "file-text",
    ".js": TEMPLATE_BS_ICON % "file-text",
    ".json": TEMPLATE_BS_ICON % "file-text",
    ".jsos": TEMPLATE_BS_ICON % "file-text",
    ".txt": TEMPLATE_BS_ICON % "file-text"
}

def customize_folder_description(directory):
    desc = ""

    try:
        # Look to see if this directory is a test results folder
        testrun_summary_file = os.path.join(directory, "testrun_summary.json")
        if os.path.exists(testrun_summary_file):
            with open(testrun_summary_file, 'r') as sf:
                summary_data = json.load(sf)
                title = "<td>%s</td>" % summary_data["title"]

                result = summary_data["result"]
                detail = summary_data["detail"]
                errors = "<td style='color: #CC0099;'>%s</td>" % detail["errors"]
                failed = "<td style='color: #CC0000;'>%s</td>" % detail["failed"]
                skipped = "<td style='color: #666666;'>%s</td>" % detail["skipped"]
                passed = "<td style='color: #669900;'>%s</td>" % detail["passed"]
                total = "<td>%s</td>" % detail["total"]
                totals_cells = "".join((title, "<td>-</td>", errors, failed, skipped, passed, total))

                branch = summary_data["branch"]
                build = summary_data["build"]
                flavor = summary_data["flavor"]

                if (branch is not None) or (build is not None) or (flavor is not None):
                    totals_cells = "<table><tr>%s</tr></table>" % (totals_cells)
                    build_info = []
                    if branch is not None:
                        build_info.append(branch)
                    if build is not None:
                        build_info.append(build)
                    if flavor is not None:
                        build_info.append(flavor)

                    build_info_cells = "<table><tr>%s</tr></table>" % " - ".join(build_info)
                    desc = "<table><tr><td>%s</td></tr><tr><td>%s</td></tr></table>" % (totals_cells, build_info_cells)
                else:
                    desc = "<table><tr>%s</tr></table>" % (totals_cells)

    except Exception as ex:
        print("bummer, we had an exception while trying to create a customized folder description")

    return desc

def view_logstore(leafpath):
    content = None

    leafpath = leafpath.strip("/")
    leaf_parts = leafpath.split("/")

    logstore_baseurl = request.scheme + "://" + request.host + "/" + "logstore"

    full_path = DIR_RESULTS.rstrip("/") + "/" + leafpath
    if os.path.isfile(full_path):
        base, ext = os.path.splitext(full_path)

        with open(full_path, 'r') as cf:
            content = cf.read()

        mimetype = "text/plain"
        if ext in MIME_TYPES:
            mimetype = MIME_TYPES[ext]
        response = Response(content, mimetype=mimetype)

    elif os.path.isdir(full_path):
        template = "directory_listing.html"
        mimetype = "text/html"

        thisdir_name = os.path.basename(full_path)
        
        
        nxticon = "<td></td>"

        parentdir_label = "-"
        parentdir_link = ""
        if len(leaf_parts) > 1:
            parentdir_label = "Parent Directory"
            parentdir_link = logstore_baseurl + "/" + "/".join(leaf_parts[:-1])
            nxticon = TEMPLATE_MD_ICON % "arrow_back"

        directory_rows = []

        nxtlink = TEMPLATE_LINK % (parentdir_link, parentdir_label)
        nxtlastmod = ""
        nxtsize = "-"
        nxtdesc = ""

        nxtrow = TEMPLATE_LISTING_ROW % (nxticon, nxtlink, nxtlastmod, nxtsize, nxtdesc)
        directory_rows.append(nxtrow)

        for dirpath, dirnames, filenames in os.walk(full_path, topdown=True):
            
            dirnames.sort()
            nxticon = TEMPLATE_MD_ICON % "folder"
            for nxtdir in dirnames:
                nxtdir_full = os.path.join(dirpath, nxtdir)
                nxtdir_url = logstore_baseurl + "/" + leafpath  + "/" + nxtdir
                nxtlink = TEMPLATE_LINK % (nxtdir_url, nxtdir)
                nxtlastmod = time.ctime(os.path.getmtime(nxtdir_full))
                nxtsize = os.path.getsize(nxtdir_full)
                nxtdesc = customize_folder_description(nxtdir_full)

                nxtrow = TEMPLATE_LISTING_ROW % (nxticon, nxtlink, nxtlastmod, nxtsize, nxtdesc)
                directory_rows.append(nxtrow)

            fileicon_default = TEMPLATE_MD_ICON % "file"
            filenames.sort()
            for nxtfile in filenames:
                nxticon = fileicon_default
                base, ext = os.path.splitext(nxtfile)
                if ext in TABLE_MD_ICON:
                    nxticon = TABLE_MD_ICON[ext] 
                nxtfile_full = os.path.join(dirpath, nxtfile)
                nxtfile_url = logstore_baseurl + "/" + leafpath  + "/" + nxtfile
                nxtlink = TEMPLATE_LINK % (nxtfile_url, nxtfile)
                nxtlastmod = time.ctime(os.path.getmtime(nxtfile_full))
                nxtsize = os.path.getsize(nxtfile_full)
                nxtdesc = ""

                nxtrow = TEMPLATE_LISTING_ROW % (nxticon, nxtlink, nxtlastmod, nxtsize, nxtdesc)
                directory_rows.append(nxtrow)

            #We only want the info in the top dir
            break

        directory_rows = os.linesep.join(directory_rows)

        content = render_template(template, directory=thisdir_name, directory_rows=directory_rows)
        response = Response(content, mimetype=mimetype)

    return response
