
import json
import operator
import os

from flask_restplus import Namespace, Resource
from flask_restplus.reqparse import RequestParser

from akit.environment.context import Context
from akit.integration.agents.upnpagent import UpnpAgent
from akit.integration.landscaping import Landscape

context = Context()
landscape = Landscape()
upnp_agent = UpnpAgent()

RESULTS_NAMESPACE_PATH = "/results"

DIR_RESULTS = os.path.expanduser(context.lookup("/environment/configuration/paths/results"))
DIR_TESTRESULTS = os.path.join(DIR_RESULTS, "testresults")

results_ns = Namespace("Results v1", description="APIs for information about results.")

@results_ns.route("/")
class ResultsSummary(Resource):

   def get(self):
        """
            Returns a job queue summary
        """

        results = []

        base_len = len(DIR_RESULTS)

        for dirpath, dirnames, filenames in os.walk(DIR_TESTRESULTS):
            if "testrun_summary.json" in filenames and "testsummary.html" in filenames:
                testrun_summary_html_fullpath = os.path.join(dirpath, "testsummary.html")
                testrun_summary_json_fullpath = os.path.join(dirpath, "testrun_summary.json")

                summary_data = None
                with open(testrun_summary_json_fullpath, 'r') as jf:
                    summary_content = jf.read()
                    summary_data = json.loads(summary_content)

                if summary_data is not None:
                    testrun_summary_html_leaf = "/logstore/" + testrun_summary_html_fullpath[base_len:].lstrip("/")
                    summary_data["htmlreport"] = testrun_summary_html_leaf
                    results.append(summary_data)

        results = sorted(results, key=operator.itemgetter("start"), reverse=True)

        rtndata = {
            "status": "success",
            "results": results
        }

        return rtndata

def publish_namespaces(version_prefix):
    ns_list = [
        (results_ns, "".join([version_prefix, RESULTS_NAMESPACE_PATH]))
    ]
    return ns_list
