
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
                diagram.layout = go.GraphObject.make(
                    go.LayeredDigraphLayout,
                    {
                        direction: 90,
                        layerSpacing: 10,
                        columnSpacing: 15,
                        setsPortSpots: false
                    }
                );

                var lookup_power_server = {};
                var lookup_serial_server = {};

                var graphNodes = [];
                var graphLinks = [];

                var nodeIndex = 0;

                var linuxHostIconUri = "static/images/unknown.png";
                var windowsHostIconUri = "static/images/unknown.png";
                var unknownHostIconUri = "static/images/unknown.png";

                var serialServerIconUri = "static/images/unknown.png";
                var serialPowerIconUri = "static/images/unknown.png";

                if (lscape.pod.power != undefined) {
                    for (const pwrsvr of lscape.pod.power) {

                        nodeInfo = {
                            "key": pwrsvr.name,
                            "iconUri": serialPowerIconUri,
                            "color": "lightgray",
                            "nodeIndex": nodeIndex
                        };

                        lookup_power_server[pwrsvr.name] = nodeInfo

                        pwrsvr.nodeIndex = nodeIndex;
                        graphNodes.push(nodeInfo);
                        nodeIndex += 1;
                    }
                }

                if (lscape.pod.serial != undefined) {
                    for (const sersvr of lscape.pod.serial) {

                        nodeInfo = {
                            "key": sersvr.name,
                            "iconUri": serialServerIconUri,
                            "color": "lightgray",
                            "nodeIndex": nodeIndex
                        };

                        lookup_serial_server[sersvr.name] = nodeInfo

                        sersvr.nodeIndex = nodeIndex;
                        graphNodes.push(nodeInfo);
                        nodeIndex += 1;
                    }
                }

                if (lscape.pod.devices != undefined) {
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
                            nodeInfo = {
                                "key": device.host,
                                "iconUri": iconUri,
                                "color": "pink"
                            };
                        }
                        else {
                            nodeInfo = {
                                "key": "ERROR",
                                "iconUri": iconUri,
                                "color": "pink"
                            };
                        }

                        if (device.features != undefined) {
                            if(lscape.pod.power != undefined)
                            {
                                if (device.features.power != undefined) {
                                    power_mapping = device.features.power;

                                    pwrname = power_mapping.name;
                                    pwrswitch = power_mapping.switch;

                                    portId = pwrname + "/" + pwrswitch;
                                    if ("bottomArray" in nodeInfo) {
                                        nodeInfo["bottomArray"].push(
                                            {
                                                "portColor":"#ebe3fc",
                                                "portId": portId
                                            }
                                        );
                                    } else {
                                        nodeInfo["bottomArray"] = [
                                            {
                                                "portColor":"#ebe3fc",
                                                "portId": portId
                                            }
                                        ];
                                    }

                                    if (pwrname in lookup_power_server) {
                                        pwrsvr = lookup_power_server[pwrname];
                                        pwrsvridx = pwrsvr.nodeIndex;

                                        if ("topArray" in pwrsvr) {
                                            pwrsvr["topArray"].push(
                                                {
                                                    "portColor":"#ebe3fc",
                                                    "portId": portId
                                                }
                                            );
                                        } else {
                                            pwrsvr["topArray"] = [
                                                {
                                                    "portColor":"#ebe3fc",
                                                    "portId": portId
                                                }
                                            ]
                                        }

                                        linkNode = {
                                            "from": pwrsvridx,
                                            "to": nodeIndex,
                                            "fromPort": pwrswitch,
                                            "toPort": portId
                                        };
                                        graphLinks.push(linkNode)
                                    }
                                }
                            }

                            if(lscape.pod.serial != undefined)
                            {
                                if (device.features.serial != undefined) {
                                    serial_mapping = device.features.serial;

                                    sername = power_mapping.name;
                                    serswitch = power_mapping.port;

                                    portId = sername + "/" + serswitch;
                                    if ("bottomArray" in nodeInfo) {
                                        nodeInfo["bottomArray"].push(
                                            {
                                                "portColor":"#ebe3fc",
                                                "portId": portId
                                            }
                                        );
                                    } else {
                                        nodeInfo["bottomArray"] = [
                                            {
                                                "portColor":"#ebe3fc",
                                                "portId": portId
                                            }
                                        ];
                                    }

                                    if (sername in lookup_serial_server) {
                                        sersvr = lookup_serial_server[sername];
                                        sersvridx = sersvr.nodeIndex;

                                        if ("topArray" in sersvr) {
                                            sersvr["topArray"].push(
                                                {
                                                    "portColor":"#ebe3fc",
                                                    "portId": portId
                                                }
                                            );
                                        } else {
                                            sersvr["topArray"] = [
                                                {
                                                    "portColor":"#ebe3fc",
                                                    "portId": portId
                                                }
                                            ];
                                        }

                                        linkNode = {
                                            "from": sersvridx,
                                            "to": nodeIndex,
                                            "fromPort": serswitch,
                                            "toPort": portId
                                        };
                                        graphLinks.push(linkNode)
                                    }
                                }
                            }
                        }

                        if (nodeInfo != null) {
                            device.nodeIndex = nodeIndex;
                            graphNodes.push(nodeInfo);
                            nodeIndex += 1;
                        }
                    }
                }

                linkModel = new go.GraphLinksModel(
                    graphNodes,
                    graphLinks  // one link data, in an Array
                );
                linkModel.linkFromPortIdProperty = "fromPort";
                linkModel.linkToPortIdProperty = "toPort";

                diagram.model = linkModel
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
