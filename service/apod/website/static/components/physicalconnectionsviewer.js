
// This custom-routing Link class tries to separate parallel links from each other.
// This assumes that ports are lined up in a row/column on a side of the node.
function CustomLink() {
    go.Link.call(this);
};

go.Diagram.inherit(CustomLink, go.Link);

CustomLink.prototype.findSidePortIndexAndCount = function(node, port) {
    var nodedata = node.data;

    if (nodedata !== null) {
        var portdata = port.data;
        var side = port._side;
        var arr = nodedata[side + "Array"];
        var len = arr.length;

        for (var i = 0; i < len; i++) {
            if (arr[i] === portdata)
                return [i, len];
        }
    }

    return [-1, len];
};

CustomLink.prototype.computeEndSegmentLength = function(node, port, spot, from) {
    var esl = go.Link.prototype.computeEndSegmentLength.call(this, node, port, spot, from);
    var other = this.getOtherPort(port);

    if (port !== null && other !== null) {
        var thispt = port.getDocumentPoint(this.computeSpot(from));
        var otherpt = other.getDocumentPoint(this.computeSpot(!from));

        if (Math.abs(thispt.x - otherpt.x) > 20 || Math.abs(thispt.y - otherpt.y) > 20) {
            var info = this.findSidePortIndexAndCount(node, port);
            var idx = info[0];
            var count = info[1];

            if (port._side == "top" || port._side == "bottom") {
                if (otherpt.x < thispt.x) {
                    return esl + 4 + idx * 8;
                } else {
                    return esl + (count - idx - 1) * 8;
                }
            } else {  // left or right
                if (otherpt.y < thispt.y) {
                    return esl + 4 + idx * 8;
                } else {
                    return esl + (count - idx - 1) * 8;
                }
            }
        }
    }

    return esl;
};

CustomLink.prototype.hasCurviness = function() {
if (isNaN(this.curviness)) return true;
return go.Link.prototype.hasCurviness.call(this);
};

CustomLink.prototype.computeCurviness = function() {
    if (isNaN(this.curviness)) {

        var fromnode = this.fromNode;
        var fromport = this.fromPort;
        var fromspot = this.computeSpot(true);
        var frompt = fromport.getDocumentPoint(fromspot);
        var tonode = this.toNode;
        var toport = this.toPort;
        var tospot = this.computeSpot(false);
        var topt = toport.getDocumentPoint(tospot);

        if (Math.abs(frompt.x - topt.x) > 20 || Math.abs(frompt.y - topt.y) > 20) {
            if ((fromspot.equals(go.Spot.Left) || fromspot.equals(go.Spot.Right)) &&
                (tospot.equals(go.Spot.Left) || tospot.equals(go.Spot.Right))) {
                var fromseglen = this.computeEndSegmentLength(fromnode, fromport, fromspot, true);
                var toseglen = this.computeEndSegmentLength(tonode, toport, tospot, false);
                var c = (fromseglen - toseglen) / 2;
                if (frompt.x + fromseglen >= topt.x - toseglen) {
                    if (frompt.y < topt.y)
                        return c;
                    if (frompt.y > topt.y)
                        return -c;
                }
            } else if ((fromspot.equals(go.Spot.Top) || fromspot.equals(go.Spot.Bottom)) &&
                (tospot.equals(go.Spot.Top) || tospot.equals(go.Spot.Bottom))) {
                var fromseglen = this.computeEndSegmentLength(fromnode, fromport, fromspot, true);
                var toseglen = this.computeEndSegmentLength(tonode, toport, tospot, false);
                var c = (fromseglen - toseglen) / 2;
                if (frompt.x + fromseglen >= topt.x - toseglen) {
                    if (frompt.y < topt.y)
                        return c;
                    if (frompt.y > topt.y)
                        return -c;
                }
            }
        }
    }

    return go.Link.prototype.computeCurviness.call(this);
};
// end CustomLink class

function createDeviceNodeInfo(key, icon, color, nodeIndex) {
    nodeInfo = {
        "key": key,
        "icon": icon,
        "color": color,
        "nodeIndex": nodeIndex,
        "leftArray": [],
        "topArray": [],
        "rightArray": [],
        "bottomArray": []
    };

    return nodeInfo;
};

function createDevicePortInfo(ptype, pcolor, pid) {
    devPortNodeInfo = {
        "portType": ptype,
        "portColor": pcolor,
        "portId": pid
    };

    return devPortNodeInfo;
};

function createConnectionNodesAndLinks(lscape) {
    var colorPowerPort = "#de3c31";
    var colorPowerLine = "#e68b85";

    var colorSerialPort = "#2a99de";
    var colorSerialLine = "#6ab2de";

    var lookup_power_server = {};
    var lookup_serial_server = {};

    var graphNodes = [];
    var graphLinks = [];

    var nodeIndex = 0;

    var unknownHostIconUri = "static/images/unknown.png";

    var serialServerIconUri = "static/images/unknown.png";
    var powerServerIconUri = "static/images/powerswitch.png";
    var powerPortCount = 8;

    if (lscape.pod.power != undefined) {
        for (const pwrsvr of lscape.pod.power) {

            nodeInfo = createDeviceNodeInfo(pwrsvr.name, powerServerIconUri, "lightgray", nodeIndex);

            lookup_power_server[pwrsvr.name] = nodeInfo

            pwrsvr.nodeIndex = nodeIndex;
            graphNodes.push(nodeInfo);
            nodeIndex += 1;
        }
    }

    if (lscape.pod.serial != undefined) {
        for (const sersvr of lscape.pod.serial) {

            nodeInfo = createDeviceNodeInfo(sersvr.name, serialServerIconUri, "lightgray", nodeIndex);

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

            var devPortBaseName =  "";
            var devPortIndex = 0;

            iconUri = "static/images/unknown.png";
            if (device.cachedIcon != undefined) {
                iconUri = device.cachedIcon;
            }

            if (device.deviceType == "network/upnp") {
                nodeInfo = createDeviceNodeInfo(device.upnp.modelName, iconUri, "lightgray", nodeIndex);
                devPortBaseName = device.upnp.USN;
            }
            else if (device.deviceType == "network/ssh") {
                nodeInfo = createDeviceNodeInfo(device.host, iconUri, "white", nodeIndex);
                devPortBaseName = device.host;
            }
            else {
                nodeInfo = createDeviceNodeInfo("ERROR", iconUri, "pink", nodeIndex);
            }

            if (device.features != undefined) {
                if(lscape.pod.power != undefined)
                {
                    if (device.features.power != undefined) {
                        power_mapping = device.features.power;

                        pwrname = power_mapping.name;
                        pwrswitch = power_mapping.switch;

                        fromPortId = devPortBaseName + "/" + devPortIndex.toString()
                        devPortIndex += 1;

                        devPortNodeInfo = createDevicePortInfo("power", colorPowerPort, fromPortId);

                        if ("bottomArray" in nodeInfo) {
                            nodeInfo["bottomArray"].push(devPortNodeInfo);
                        } else {
                            nodeInfo["bottomArray"] = [devPortNodeInfo];
                        }

                        toPortId = pwrname + "/" + pwrswitch.toString();

                        if (pwrname in lookup_power_server) {
                            pwrSvrNodeInfo = lookup_power_server[pwrname];
                            pwrSvrIdx = pwrSvrNodeInfo.nodeIndex;

                            pwrSvrPortNodeInfo = createDevicePortInfo("power", colorPowerPort, toPortId);

                            pwrSvrNodeInfo.topArray.push(pwrSvrPortNodeInfo);

                            linkNode = {
                                "from": nodeIndex,
                                "to": pwrSvrIdx,
                                "fromPort": fromPortId,
                                "toPort": toPortId,
                                "color": colorPowerLine
                            };
                            graphLinks.push(linkNode)
                        }
                    }
                }

                if(lscape.pod.serial != undefined)
                {
                    if (device.features.serial != undefined) {
                        serial_mapping = device.features.serial;

                        sername = serial_mapping.name;
                        serport = serial_mapping.port;

                        fromPortId = devPortBaseName + "/" + devPortIndex.toString()
                        devPortIndex += 1;

                        devPortNodeInfo = createDevicePortInfo("serial", colorSerialPort, fromPortId);

                        nodeInfo.bottomArray.push(devPortNodeInfo);

                        toPortId = sername + "/" + serport.toString();

                        if (sername in lookup_serial_server) {
                            serSvrNodeInfo = lookup_serial_server[sername];
                            serSvrIdx = serSvrNodeInfo.nodeIndex;

                            serSvrPortNodeInfo = createDevicePortInfo("serial", colorSerialPort, toPortId);

                            serSvrNodeInfo.topArray.push(serSvrPortNodeInfo);

                            linkNode = {
                                "from": nodeIndex,
                                "to": serSvrIdx,
                                "fromPort": fromPortId,
                                "toPort": toPortId,
                                "color": colorSerialLine
                            };

                            graphLinks.push(linkNode)
                        }
                    }
                }
            }

            if (nodeInfo != null) {
                graphNodes.push(nodeInfo);
                nodeIndex += 1;
            }
        }
    }

    return [graphNodes, graphLinks];
}

function renderConnectionDiagram(lscape, diagram) {
    var portSize = new go.Size(16, 16);

    diagram.initialAutoScale = go.Diagram.Uniform;
    diagram.allowCopy = false;
    diagram.nodeTemplate = go.GraphObject.make(
        go.Node,
        // We are using a Table so we can place small nodes around a central shape
        "Table",
        {
            locationObjectName: "BODY",
            locationSpot: go.Spot.Center,
            selectionObjectName: "BODY",
            //contextMenu: nodeMenu
        },
        new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),

        // ================== COMPONENT BODY ==================
        go.GraphObject.make(
            go.Panel, "Auto",
            {
                name: "BODY",
                row: 1,
                column: 1,
                height: 128,
                width: 128
            },
            go.GraphObject.make(
                go.Shape,
                "RoundedRectangle",  // use this kind of figure for the Shape
                // bind Shape.fill to Node.data.color
                new go.Binding("fill", "color")
            ),
            go.GraphObject.make(
                go.TextBlock,
                {
                    margin: 3,
                    alignment: go.Spot.Bottom  // some room around the text
                    // bind TextBlock.text to Node.data.key
                },
                new go.Binding("text", "key")
            ),
            go.GraphObject.make(
                go.Picture,
                { 
                    desiredSize: new go.Size(76, 76)
                },
                new go.Binding("source", "icon")
            )
        ),



        // ================== COMPONENT BODY ==================
        go.GraphObject.make(
            go.Panel,
            "Horizontal",
            new go.Binding("itemArray", "topArray"),
            {
                row: 0,
                column: 1,
                itemTemplate: go.GraphObject.make(
                    go.Panel,
                    {
                        _side: "top",
                        fromSpot: go.Spot.Top,
                        toSpot: go.Spot.Top,
                        fromLinkable: true,
                        toLinkable: true,
                        cursor: "pointer"
                        //contextMenu: portMenu
                    },
                    new go.Binding("portId", "portId"),
                    go.GraphObject.make(
                        go.Shape,
                        "Rectangle",
                        {
                            stroke: null, strokeWidth: 0,
                            desiredSize: portSize,
                            margin: new go.Margin(0, 1)
                        },
                        new go.Binding("fill", "portColor")
                    )
                )
            }
        ),


        // ================== LEFT PORT ELEMENTS ==================
        go.GraphObject.make(
            go.Panel,
            "Vertical",
            new go.Binding("itemArray", "leftArray"),
            {
                row: 1,
                column: 0,
                itemTemplate: go.GraphObject.make(
                    go.Panel,
                    {
                        _side: "left",
                        fromSpot: go.Spot.Left,
                        toSpot: go.Spot.Left,
                        fromLinkable: true,
                        toLinkable: true,
                        cursor: "pointer"
                        //contextMenu: portMenu
                    },
                    new go.Binding("portId", "portId"),
                    go.GraphObject.make(
                        go.Shape,
                        "Rectangle",
                        {
                            stroke: null, strokeWidth: 0,
                            desiredSize: portSize,
                            margin: new go.Margin(0, 1)
                        },
                        new go.Binding("fill", "portColor")
                    )
                )
            }
        ),

        // ================== TOP PORT ELEMENTS ==================
        go.GraphObject.make(
            go.Panel,
            "Horizontal",
            new go.Binding("itemArray", "topArray"),
            {
                row: 0,
                column: 1,
                itemTemplate: go.GraphObject.make(
                    go.Panel,
                    {
                        _side: "bottom",
                        fromSpot: go.Spot.Top,
                        toSpot: go.Spot.Top,
                        fromLinkable: true,
                        toLinkable: true,
                        cursor: "pointer"
                        //contextMenu: portMenu
                    },
                    new go.Binding("portId", "portId"),
                    go.GraphObject.make(
                        go.Shape,
                        "Rectangle",
                        {
                            stroke: null, strokeWidth: 0,
                            desiredSize: portSize,
                            margin: new go.Margin(0, 1)
                        },
                        new go.Binding("fill", "portColor")
                    )
                )
            }
        ),

        // ================= RIGHT PORT ELEMENTS ==================
        go.GraphObject.make(
            go.Panel,
            "Vertical",
            new go.Binding("itemArray", "rightArray"),
            {
                row: 1,
                column: 0,
                itemTemplate: go.GraphObject.make(
                    go.Panel,
                    {
                        _side: "right",
                        fromSpot: go.Spot.Right,
                        toSpot: go.Spot.Right,
                        fromLinkable: true,
                        toLinkable: true,
                        cursor: "pointer"
                        //contextMenu: portMenu
                    },
                    new go.Binding("portId", "portId"),
                    go.GraphObject.make(
                        go.Shape,
                        "Rectangle",
                        {
                            stroke: null, strokeWidth: 0,
                            desiredSize: portSize,
                            margin: new go.Margin(0, 1)
                        },
                        new go.Binding("fill", "portColor")
                    )
                )
            }
        ),

        // ================= BOTTOM PORT ELEMENTS ==================
        go.GraphObject.make(
            go.Panel,
            "Horizontal",
            new go.Binding("itemArray", "bottomArray"),
            {
                row: 2,
                column: 1,
                itemTemplate: go.GraphObject.make(
                    go.Panel,
                    {
                        _side: "bottom",
                        fromSpot: go.Spot.Bottom,
                        toSpot: go.Spot.Bottom,
                        fromLinkable: true,
                        toLinkable: true,
                        cursor: "pointer"
                        //contextMenu: portMenu
                    },
                    new go.Binding("portId", "portId"),
                    go.GraphObject.make(
                        go.Shape,
                        "Rectangle",
                        {
                            stroke: null, strokeWidth: 0,
                            desiredSize: portSize,
                            margin: new go.Margin(0, 1)
                        },
                        new go.Binding("fill", "portColor")
                    )
                )
            }
        )
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

    // an orthogonal link template, reshapable and relinkable
    diagram.linkTemplate = go.GraphObject.make(
        CustomLink,
        {
            routing: go.Link.AvoidsNodes,
            corner: 4,
            curve: go.Link.JumpGap,
            reshapable: true,
            resegmentable: true,
            relinkableFrom: true,
            relinkableTo: true
        },
        new go.Binding("points").makeTwoWay(),
        go.GraphObject.make(
            go.Shape,
            {
                strokeWidth: 2,
            },
            new go.Binding("stroke", "color")
        )
    );

    const [graphNodes, graphLinks] = createConnectionNodesAndLinks(lscape);

    console.log(graphNodes);
    console.log(graphLinks);

    linkModel = go.GraphObject.make(
        go.GraphLinksModel,
        {
            copiesArrays: true,
            copiesArrayObjects: true,
            linkFromPortIdProperty: "fromPort",
            linkToPortIdProperty: "toPort",
            nodeDataArray: graphNodes,
            linkDataArray: graphLinks  // one link data, in an Array
        }
    );

    diagram.model = linkModel;

    diagram.requestUpdate();
}

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
                
                var portSize = new go.Size(16, 16);

                var diagram = new go.Diagram("diagramConnections");

                renderConnectionDiagram(lscape, diagram);
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
