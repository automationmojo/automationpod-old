
Vue.component('summary-viewer', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        current: {
            type: Object,
            default: function() {
                return {}
            }
        },
        queue_list: {
            type: Object,
            default: function() {
                return {}
            }
        }
    },
    template: `
        <b-container>
            <b-row style="margin-top: 20px;">
                <b-card style="width: 100%">
                    <b-card-title >Current Job</b-card-title>
                    <b-body>
                        <b-row>
                            <b-col>Jobname:</b-col>
                            <b-col>{{ current.jobname }}</b-col>
                            <b-col>Started:</b-col>
                            <b-col>{{ current.started }}</b-col>
                        </b-row>
                        <b-row></b-row>
                        <b-row>
                            <b-col>Progress:</b-col>
                            <b-col>
                                <b-progress-bar :value="current.progress" variant="success">
                                    <h5 v-if="value > 0">Loading</h5>
                                </b-progress-bar>
                            </b-col>
                        </b-row>
                    </b-body>
                </b-card>
            </b-row>
            <b-row style="margin-top: 20px;">
                <b-card style="width: 100%">
                    <b-card-title>Job Queue</b-card-title>
                    <b-body>
                        <b-container>
                            <summary-job-queue-item v-for="qival, qikey, qiidx in queue_list" 
                                v-bind:qival="queueitem">
                            </summary-job-queue-item>
                        </b-container>
                    </b-body>
                </b-card>
            </b-row>
        </b-container>
        ` // End of Template
});


Vue.component('summary-job-queue-item', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        queueitem: {
            type: Object,
            default: function() {
                return {}
            }
        }
    },
    template: `
        <b-container>
            
        </b-container>
        ` // End of Template
});
