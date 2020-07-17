
import datetime

from flask import request

from flask_restplus import Namespace, Resource
from flask_restplus.reqparse import RequestParser
from flask_restplus import fields

from akit.datum.orm import WorkQueue

from akit.integration.agents.upnpagent import UpnpAgent
from akit.integration.landscaping import Landscape

from apoddb import get_apoddb_session

landscape = Landscape()
upnp_agent = UpnpAgent()

JOBQUEUE_NAMESPACE_PATH = "/jobqueue"

jobqueue_ns = Namespace("Job Queue v1", description="APIs for information about the pending jobs.")

jobqueue_model = jobqueue_ns.model("WorkItem", {
        "title": fields.String(required=True, description="The title of the job."),
        "description": fields.String(required=False, description="A short description of the job."),
        "branch": fields.String(required=False, description="The branch to associate with the job."),
        "build": fields.String(required=False, description="The build to associate with the job."),
        "flavor": fields.String(required=False, description="The flavor to associate with the job."),
        "packet": fields.Raw(required=True, description="The JSON work packet that will be used to run the job.")
    })

@jobqueue_ns.route("/")
class JobQueueSummary(Resource):

   @jobqueue_ns.expect(jobqueue_model)
   def post(self):

        work_item = request.json

        title = work_item["title"]
        description = work_item["description"]
        branch = work_item["branch"]
        build = work_item["build"]
        flavor = work_item["flavor"]
        packet = work_item["packet"]

        added = datetime.datetime.now()
        status = "WAITING"
        user_id = 0

        wqitem = WorkQueue(title=title, description=description, branch=branch, build=build,
                           flavor=flavor, added=added, status=status, packet=packet, user_id=user_id)

        session = get_apoddb_session()
        session.add(wqitem)
        session.commit()

        return

   def get(self):
        """
            Returns a job queue summary
        """

        qitems_list = []

        session = get_apoddb_session()
        for wqitem in session.query(WorkQueue).all():
            item = wqitem.to_dict()
            item["username"] = "someuser"
            qitems_list.append(item)

        rtndata = {
            "status": "success",
            "items": qitems_list
        }

        return rtndata

def publish_namespaces(version_prefix):
    ns_list = [
        (jobqueue_ns, "".join([version_prefix, JOBQUEUE_NAMESPACE_PATH]))
    ]
    return ns_list
