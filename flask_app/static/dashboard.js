
// edges: [{sourceID: "BremainInSpain", targetID: "BremainInSpain"}, {sourceID: "BremainInSpain", targetID: "londonyc"}, {sourceID: "NephiLaxmus", targetID: "NephiLaxmus"}, {sourceID: "NephiLaxmus", targetID: "g4m4r333"}, {sourceID: "SarahBurnett", targetID: "SarahBurnett"}, {sourceID: "SarahBurnett", targetID: "WildnightinB"}, {sourceID: "giiomarchesin", targetID: "giiomarchesin"}, {sourceID: "giiomarchesin", targetID: "gabl1ma"}, {sourceID: "TV9Marathi", targetID: "gSiddharth51"}, {sourceID: "TV9Marathi", targetID: "TV9Marathi"}, …] (18)
// isVerified: false 'verified-display'
// maxFollowers: 0 'max-follower-count-display'
// minFollowers: 0 'min-follower-count-display'
// nodes: [Object, Object, Object, Object, Object, Object, Object, Object, Object, Object, …] (18)
// top_k: 10 'influencers-display'
// window_size: 1  'duration-display'
// Object Prototype


let currentLoadRequest = null;
let currentWaitRequest = null;
let nodes = null
let edges = null
let metaData = null

$(document).ready(function () {
    load_data()
    $('.collapse-link').on('click', function () {
        var $BOX_PANEL = $(this).closest('.card'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function () {
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }

        $ICON.toggleClass('fa-chevron-up fa-chevron-down');

    });

    $('.close-link').click(function () {
        var $BOX_PANEL = $(this).closest('.card');

        $BOX_PANEL.remove();
    });

    document.getElementById("search-icon").addEventListener('click', () => {
        $.ajax({
            url: '/terminate',
            success: function (response) {
                console.log(response);
            }
        });
    })

})



function wait_for_update() {
    /**
     * Creates a GET requests to route '/updated' and waits for response
     * upon which calls load_data()
     */
    console.log('waiting ....');
    currentWaitRequest = $.ajax({
        url: '/updated',
        beforeSend: function () {
            if (currentWaitRequest != null) {
                currentWaitRequest.abort();
            }
        },
        success: function (response) {
            console.log('data updated successfully');
            load_data()
        }
    });

}

function load_data() {
    /**
     * Creates a GET request to route '/data' and receives latest results
     */
    console.log('loading ....');
    var url = '/data'
    currentLoadRequest = $.ajax({
        url: url,
        beforeSend: function () {
            if (currentLoadRequest != null) {
                currentLoadRequest.abort();
            }
        },
        success: function (data) {
            console.log(data);
            nodes = data.nodes
            edges = data.edges
            if (data.updateInterval) {
                console.log(data.updateInterval);
            }
            metaData = {
                isVerified: data.isVerified,
                minFollowers: data.minFollowers,
                maxFollowers: data.maxFollowers,
                windowSize: data.window_size,
                updateInterval: data.update_interval,
                topK: data.top_k
            }
            updateMetaData(metaData)
            draw()
            wait_for_update();
        },
        error: function () {
            console.error('error loading data');
            wait_for_update();
        }
    });
    return true;
}

function updateMetaData(metaData) {
    if (metaData.isVerified) {
        document.querySelector('#verified-display').textContent = 'ON'
    }
    if (metaData.minFollowers) {
        document.querySelector('#min-follower-count-display').textContent = metaData.minFollowers.toString()
    }
    if (metaData.maxFollowers) {
        document.querySelector('#max-follower-count-display').textContent = metaData.maxFollowers.toString()
    }
    if (metaData.windowSize) {
        if (metaData.windowSize > 10) {
            document.querySelector('#duration-display').textContent = metaData.windowSize.toString() + ':00mins'
        } else {
            document.querySelector('#duration-display').textContent = '0' + metaData.windowSize.toString() + ':00mins'
        }
    }

    document.querySelector('#influencers-display').textContent = metaData.topK.toString()
    let timeToRefresh = 30

    if (metaData.updateInterval) {
        timeToRefresh = metaData.updateInterval * 60
    }
    document.querySelector('#refresh-display').textContent = ''
    var seconds = timeToRefresh - 1,
        display = document.querySelector('#refresh-display');
    startTimer(seconds, display);
}


function draw() {

    var theme = {
        color: [
            '#6ab88a', '#34495E', '#BDC3C7', '#3498DB',
            '#1E7A74', '#8abb6f', '#759c6a', '#bfd3b7'
        ],

        title: {
            itemGap: 8,
            textStyle: {
                fontWeight: 'normal',
                color: '#34495E'
            }
        },

        dataRange: {
            color: ['#1f610a', '#97b58d']
        },

        toolbox: {
            color: ['#408829', '#408829', '#408829', '#408829']
        },

        tooltip: {
            backgroundColor: 'rgba(0,0,0,0.5)',
            axisPointer: {
                type: 'line',
                lineStyle: {
                    color: '#408829',
                    type: 'dashed'
                },
                crossStyle: {
                    color: '#408829'
                },
                shadowStyle: {
                    color: 'rgba(200,200,200,0.3)'
                }
            }
        },

        dataZoom: {
            dataBackgroundColor: '#eee',
            fillerColor: 'rgba(64,136,41,0.2)',
            handleColor: '#408829'
        },
        grid: {
            borderWidth: 0
        },

        categoryAxis: {
            axisLine: {
                lineStyle: {
                    color: '#6ab88a'
                }
            },
            splitLine: {
                lineStyle: {
                    color: ['#eee']
                }
            }
        },

        valueAxis: {
            axisLine: {
                lineStyle: {
                    color: '#6ab88a'
                }
            },
            splitArea: {
                show: true,
                areaStyle: {
                    color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
                }
            },
            splitLine: {
                lineStyle: {
                    color: ['#eee']
                }
            }
        },
        timeline: {
            lineStyle: {
                color: '#408829'
            },
            controlStyle: {
                normal: { color: '#408829' },
                emphasis: { color: '#408829' }
            }
        },

        k: {
            itemStyle: {
                normal: {
                    color: '#68a54a',
                    color0: '#a9cba2',
                    lineStyle: {
                        width: 1,
                        color: '#408829',
                        color0: '#86b379'
                    }
                }
            }
        },
        map: {
            itemStyle: {
                normal: {
                    areaStyle: {
                        color: '#ddd'
                    },
                    label: {
                        textStyle: {
                            color: '#c12e34'
                        }
                    }
                },
                emphasis: {
                    areaStyle: {
                        color: '#99d2dd'
                    },
                    label: {
                        textStyle: {
                            color: '#c12e34'
                        }
                    }
                }
            }
        },
        textStyle: {
            fontFamily: 'Open sans, sans-serif'
        }
    };



    var echartLine = echarts.init(document.getElementById('line'), theme);

    echartLine.setOption({
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            x: 220,
            y: 40,
            data: ['Influence Scores']
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    show: true,
                    title: "Raw",
                    lang: [
                        "Raw Data View",
                        "Close",
                        "Refresh",
                    ],
                    readOnly: false,
                    buttonColor: '#6ab88a'
                },
                magicType: {
                    show: true,
                    title: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                    },
                    type: ['line', 'bar', 'stack']
                },
                restore: {
                    show: true,
                    title: "Restore"
                },
                saveAsImage: {
                    show: true,
                    title: "Save Image"
                }
            }
        },
        calculable: true,
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLabel: {
                rotate: 15,
                color: '#1e1e1e',
                showMaxLabel: true
            },
            data: nodes.map((node) => node.name)
        }],
        yAxis: [{
            type: 'value'
        }],
        series: [{
            name: 'Influence Scores',
            type: 'line',
            smooth: true,
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data: nodes.map((node) => node.score),
            markPoint: {
                data: [{
                    type: 'max',
                    name: '???'
                }, {
                    type: 'min',
                    name: '???'
                }]
            }
        }
        ]
    });


    var echartGraph = echarts.init(document.getElementById("inf"), theme);
    echartGraph.showLoading();

    let match = []

    edges.forEach((edge) => {
        match = nodes.filter((node) => node.id == edge.targetID)
        if (!match.length) {
            let newNode = {
                "id": edge.targetID,
                "name": edge.targetID,
                "score": 1
            }
            nodes.push(newNode)
        }
    })

    let arr = nodes.map((node) => {
        return {
            x: Math.floor(Math.random() * 1000), //generate random x position for node
            y: Math.floor(Math.random() * 400), //generate random y position for node
            id: node.id,
            name: node.name,
            symbolSize: node.score + 5,
            itemStyle: {
                color: '#' + Math.floor(Math.random() * 16777215).toString(16) // generate random colors for node
            }
        };
    })


    echartGraph.hideLoading();
    echartGraph.setOption({
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    show: true,
                    title: "Raw",
                    lang: [
                        "Raw Data View",
                        "Close",
                        "Refresh",
                    ],
                    readOnly: false,
                    buttonColor: '#6ab88a'
                },
                restore: {
                    show: true,
                    title: "Restore"
                },
                saveAsImage: {
                    show: true,
                    title: "Save Image"
                }
            }
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                type: 'graph',
                layout: 'none',
                data: arr,
                edges: edges.map((edge) => {
                    return {
                        source: edge.sourceID,
                        target: edge.targetID
                    };
                }),
                emphasis: {
                    label: {
                        show: true
                    }
                },
                roam: true,
                focusNodeAdjacency: true,
                lineStyle: {
                    width: 0.5,
                    curveness: 0.3,
                    opacity: 1
                }
            }
        ]
    }, true);




}


function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var x = setInterval(() => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds + "mins";

        if (--timer < 0) {
            timer = duration;
            clearInterval(x)
        }
    }, 1000);
}
