
Vue.component('physical-connections-viewer', {
    // The todo-item component now accepts a
    // "prop", which is like a custom attribute.
    // This prop is called todo.
    data: function () {
        var dobj  = {
            device_filter_selection: null
        }

        return dobj;
    },
    props: {
        title: {
            type: String,
            default: "Physical Connections"
        }, 
        landscape: {
            default: function() {
                return {}
            }
        } 
    },
    watch: {
        landscape: function(lscape) {

            if ("pod" in lscape) {
                var diagram = new go.Diagram("diagramConnections");

                diagram.initialAutoScale = go.Diagram.Uniform;
                diagram.allowCopy = false;
                diagram.nodeTemplate = go.GraphObject.make(
                    go.Node,
                    "Auto",  // the Shape automatically fits around the TextBlock
                    go.GraphObject.make(
                        go.Shape,
                        "RoundedRectangle",  // use this kind of figure for the Shape
                        // bind Shape.fill to Node.data.color
                        new go.Binding("fill", "color")),
                    go.GraphObject.make(
                        go.TextBlock,
                        { margin: 3 , alignment: go.Spot.Bottom},  // some room around the text
                        // bind TextBlock.text to Node.data.key
                        new go.Binding("text", "key")),
                    go.GraphObject.make(
                        go.Picture,
                        { desiredSize: new go.Size(100, 100) },
                        new go.Binding("source", "icon"))
                );

                var graphNodes = [];

                // Create all of the device nodes
                for (const device of lscape.pod.devices) {
                    var nodeInfo = null;
                    iconUri = "static/images/unknown.png";
                    if (device.cachedIcon != undefined) {
                        iconUri = device.cachedIcon;
                    }
                    if (device.deviceType == "network/upnp") {
                        nodeInfo = {
                            "key": device.upnp.modelName,
                            "icon": iconUri,
                            "color": "lightgray"
                        };
                    }
                    else if (device.deviceType == "network/ssh") {
                        nodeInfo = {"key": device.host, "color": "pink"};
                    }
                    else {
                        nodeInfo = {"key": "ERROR", "color": "pink"};
                    }

                    if (nodeInfo != null) {
                        graphNodes.push(nodeInfo)
                    }
                }

                var graphLinks = [];

                diagram.model = new go.GraphLinksModel(
                    graphNodes,
                    graphLinks  // one link data, in an Array
                );
            }
        }
    },
    methods: {
        
    },
    template: `
    <b-container style='margin-left: 0px; margin-right: 0px; max-width: 100%;'>
        <div id="diagramConnections" style="border: solid 1px blue; width:100%; height:800px"></div>
    </b-container>
        ` // End of Template
});
