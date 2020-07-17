
Vue.component('job-viewer', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        title: {
            type: String,
            default: "Some Job Viewer"
        }
    },
    template: `
        <b-card >
            <b-card-title class="text-center" >{{title}}</b-card-title>
            <b-row>
                <b-col xl="10" style="background: lightyellow;">
                    <job-form></job-form>
                </b-col>
            </b-row>
            <b-row style="margin-top: 40px;">
                <b-col xl="10" style="background: pink;">
                    <job-queue></job-queue>
                </b-col>
            </b-row>
        </b-card>
        ` // End of Template
});

Vue.component('job-form', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    data: function () {
        dobj = {
            form: {
                title: ''
            }
        }

        return dobj;
    },
    methods: {
        onClear(evt) {
            
        },
        onSubmit(evt) {
            
        }
    },
    template: `
    <b-form @submit="onSubmit" @clear="onClear">
        <b-form-row>
            <b-form-group
                id="input-group-title"
                label="Title:"
                label-for="input-title"
                description="The title for the job."
                >
                <b-form-input
                    id="input-title"
                    v-model="form.title"
                    required
                    placeholder="Enter title"
                ></b-form-input>
            </b-form-group>
        </b-form-row>
        <b-form-row>
            <b-form-group
                id="input-group-branch"
                label="Branch:"
                label-for="input-branch"
                description="The branch the job is running against.">
                <b-form-input
                    id="input-branch"
                    v-model="form.branch"
                    required
                    placeholder="Enter branch"
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-build"
                label="Build:"
                label-for="input-build"
                description="The build the job is running against.">
                <b-form-input
                    id="input-build"
                    v-model="form.build"
                    required
                    placeholder="Enter build"
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-flavor"
                label="Build:"
                label-for="input-flavor"
                description="The flavor the job is running against.">
                <b-form-input
                    id="input-flavor"
                    v-model="form.flavor"
                    required
                    placeholder="Enter flavor"
                ></b-form-input>
            </b-form-group>
        </b-form-row>
        <b-button type="clear" variant="danger">Clear</b-button>
        <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>` // End of Template
});

Vue.component('job-queue', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    data: function() {
        dobj = {
            jobs_list: []
        }
        return dobj;
    },
    mounted () {
        var that = this;

        var qurl = "/api/1/jobqueue";
        axios.get(qurl).then(
            (response) => {
                var jobs_list = response.data.items;
                that.jobs_list = jobs_list;
            }
        );
    },
    template: `
    <b-list-group v-bind:id="jobs_list">
        <job-card v-for="job in jobs_list" v-bind:job="job" ></job-card>
    </b-list-group>
    ` // End of Template
});

Vue.component('job-card', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    props: {
        job: {
            default: function() {
                return {}
            }
        }
    },
    template: `
        <b-card>
            <b-card-title>
                <b-container>
                    <b-row ><b-col sm="1" class="text-right">Title:</b-col><b-col lg="5">{{ job.title }}</b-col><b-col xl="6"></b-col></b-row>
                </b-container>
            </b-card-title>
            <b-card-body>
                <b-container>
                    <b-row>
                        <b-col sm="1" class="text-right">Branch:</b-col><b-col md="3">{{ job.branch }}</b-col>
                        <b-col sm="1" class="text-right">Build:</b-col><b-col md="3">{{ job.build }}</b-col>
                        <b-col sm="1" class="text-right">Flavor:</b-col><b-col md="3">{{ job.flavor }}</b-col>
                    </b-row>
                    <b-row>
                        <b-col sm="1" class="text-right">Added:</b-col><b-col md="3">{{ job.added }}</b-col>
                        <b-col sm="1" class="text-right">Status:</b-col><b-col md="3">{{ job.status }}</b-col>
                        <b-col sm="1" class="text-right">User:</b-col><b-col md="3">{{ job.username }}</b-col>
                    </b-row>
                </b-container>
            </b-card-body>
        </b-card>
        ` // End of Template
});

