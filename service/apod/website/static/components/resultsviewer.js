

Vue.component('test-result-viewer', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        title: {
            type: String,
            default: "not set"
        },
        test_result_list: {
            default: function() {
                return {}
            }
        }
    },
    template: `
        <b-container style='margin-left: 0px; margin-right: 0px; max-width: 100%;'>
            <b-row style='width: 100%;'>
                <b-col></b-col>
                <b-col cols=10><div class='h2'>{{ title }}</div></b-col>
                <b-col></b-col>
            </b-row>
            <b-row style='width: 100%;'>
                <b-col></b-col>
                <b-col cols=10>
                    <test-result-item-card v-for='pval, pidx in test_result_list'
                        v-bind:test_result='pval'>
                    </test-result-item-card>
                </b-col>
                <b-col></b-col>
            </b-row>
        </b-container>
        ` // End of Template
});

Vue.component('test-result-item-card', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        test_result: {
            default: function() {
                return {}
            }
        }
    },
    computed: {
        summary_html_report: function () {
            var report_url = window.location.protocol + "//" + window.location.host + this.test_result.htmlreport;
            return report_url;
        }
    },
    template: `
        <b-card>
            <b-card-title class="text-center">{{ test_result.title }}</b-card-title>
            <b-card-body style="margin-left: 0px; margin-right: 0px;" >
                <table style="width:100%;">
                    <tr>
                        <td  style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Branch:</td>
                        <td  style="width: 260px; text-align: left; padding-left: 10px;">{{ test_result.branch }}</td>
                        <td  style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Build:</td>
                        <td  style="width: 260px; text-align: left; padding-left: 10px;">{{ test_result.build }}</td>
                        <td  style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Flavor:</td>
                        <td  >{{ test_result.flavor }}</td>
                    </tr>
                </table>
                <table style="width:100%;">
                    <tr>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Start:</td>
                        <td style="width: 260px; text-align: left; padding-left: 10px;">{{ test_result.start.substring(0, test_result.start.length - 7 ) }}</td>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Stop:</td>
                        <td style="width: 260px; text-align: left; padding-left: 10px;">{{ test_result.stop.substring(0, test_result.stop.length - 7 ) }}</td>
                        <td></td>
                    </tr>
                </table>
                <table style="width:100%;">
                    <tr>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Errors:</td>
                        <td style="width: 90px; text-align: left; padding-left: 10px;" class="text-danger">{{ test_result.detail.errors }}</td>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Failed:</td>
                        <td style="width: 90px; text-align: left; padding-left: 10px;" class="text-danger">{{ test_result.detail.failed }}</td>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Skipped:</td>
                        <td style="width: 90px; text-align: left; padding-left: 10px;" class="text-danger">{{ test_result.detail.skipped }}</td>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Passed:</td>
                        <td style="width: 90px; text-align: left; padding-left: 10px;" class="text-danger">{{ test_result.detail.passed }}</td>
                        <td style="background: gainsboro; width: 80px; text-align: right;" class="font-weight-bold">Total:</td>
                        <td style="width: 90px; text-align: left; padding-left: 10px;" >{{ test_result.detail.total }}</td>
                        <td></td>
                    </tr>
                </table>
                <table style="width:100%;">
                    <tr>
                        <td>
                            <b-badge class="w-100" v-if='test_result.result.toLowerCase() == "error"' variant="danger">{{ test_result.result }}</b-badge>
                            <b-badge class="w-100" v-else-if='test_result.result.toLowerCase() == "failed"' variant="danger">{{ test_result.result }}</b-badge>
                            <b-badge class="w-100" v-else-if='test_result.result.toLowerCase() == "passed"' variant="success">{{ test_result.result }}</b-badge>
                            <b-badge class="w-100" v-else-if='test_result.result.toLowerCase() == "skipped"' variant="secondary">{{ test_result.result }}</b-badge>
                            <b-badge class="w-100" v-else >{{ test_result.result }}</b-badge>
                        </td>
                    </tr>
                </table>
                <table style="width:100%;">
                    <tr>
                        <td><b-link v-bind:href="summary_html_report">{{ summary_html_report }}</b-link></td>
                    </tr>
                </table>
            </b-card-body>
        </b-card>
        ` // End of Template
});

/*
    {
      "title": "Automation Test Run",
      "runid": "1d30b3b5-8774-42ff-ad88-86e4571b5f08",
      "branch": null,
      "build": null,
      "flavor": null,
      "start": "2020-03-20 23:18:48.335152",
      "stop": "2020-03-20 23:18:48.362281",
      "result": "FAILED",
      "landscape": null,
      "detail": {
        "errors": 0,
        "failed": 1,
        "skipped": 0,
        "passed": 3,
        "total": 4
      },
      "htmlreport": "/home/myron/akit/results/testresults/2020-03-20T23:18:48.335152/testsummary.html"
    },
*/

