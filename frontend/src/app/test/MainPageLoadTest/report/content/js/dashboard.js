/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 98.66666666666667, "KoPercent": 1.3333333333333333};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.286, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.19, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-8"], "isController": false}, {"data": [0.55, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-11"], "isController": false}, {"data": [0.0, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/"], "isController": false}, {"data": [0.52, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-7"], "isController": false}, {"data": [0.58, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-10"], "isController": false}, {"data": [0.25, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-6"], "isController": false}, {"data": [0.12, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-13"], "isController": false}, {"data": [0.1, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-5"], "isController": false}, {"data": [0.4, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-12"], "isController": false}, {"data": [0.31, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-9"], "isController": false}, {"data": [0.48, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-0"], "isController": false}, {"data": [0.24, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-4"], "isController": false}, {"data": [0.13, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-3"], "isController": false}, {"data": [0.36, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-2"], "isController": false}, {"data": [0.06, 500, 1500, "https://ping-pong-king-666.uc.r.appspot.com/-1"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 750, 10, 1.3333333333333333, 2255.729333333334, 43, 7947, 1548.0, 5361.599999999999, 6620.049999999999, 7364.93, 92.9944203347799, 9762.97465902046, 107.1365952417855], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["https://ping-pong-king-666.uc.r.appspot.com/-8", 50, 2, 4.0, 2432.14, 134, 3837, 2909.0, 3679.9, 3756.65, 3837.0, 9.938382031405288, 872.6811735986881, 5.95371198568873], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-11", 50, 0, 0.0, 870.4399999999999, 43, 1612, 900.5, 1222.6, 1377.699999999999, 1612.0, 11.241007194244604, 16.55413950089928, 7.058562134667265], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/", 50, 5, 10.0, 6775.0, 4714, 7947, 6825.0, 7480.0, 7660.65, 7947.0, 6.199628022318661, 4881.48732951023, 53.56829762089275], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-7", 50, 0, 0.0, 1081.5200000000004, 73, 1617, 1144.5, 1421.1, 1582.1499999999999, 1617.0, 12.333497779970399, 112.90450018500246, 7.744569406758756], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-10", 50, 0, 0.0, 920.6400000000001, 48, 1302, 1085.5, 1218.6, 1252.7499999999998, 1302.0, 11.032656663724625, 71.71226831421006, 6.776895548323036], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-6", 50, 0, 0.0, 1403.32, 180, 1960, 1541.0, 1857.3999999999999, 1910.1, 1960.0, 13.583265417006247, 194.4768108190709, 8.383421624558544], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-13", 50, 2, 4.0, 2262.4199999999996, 114, 4430, 2327.5, 3280.3, 3887.2, 4430.0, 9.127418765972983, 1698.2143773959474, 5.47645125958379], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-5", 50, 0, 0.0, 2825.600000000001, 487, 3894, 3140.0, 3800.5, 3880.5499999999997, 3894.0, 9.710623422023694, 547.8915808894931, 6.050173577393669], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-12", 50, 1, 2.0, 1228.82, 71, 2657, 1390.0, 2044.6999999999998, 2344.949999999999, 2657.0, 10.479983232026829, 376.939615646615, 6.469138086879061], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-9", 50, 0, 0.0, 1473.36, 91, 2738, 1662.0, 2165.0, 2342.9999999999995, 2738.0, 11.022927689594356, 318.125568369709, 6.975446428571429], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-0", 50, 0, 0.0, 1094.4000000000003, 277, 2567, 1026.5, 1529.8999999999999, 2170.9999999999973, 2567.0, 14.44669170759896, 320.959215183473, 8.63415559086969], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-4", 50, 0, 0.0, 1745.98, 93, 3020, 1808.0, 2901.4, 2951.25, 3020.0, 13.007284079084286, 269.2279160704995, 8.167659827003122], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-3", 50, 0, 0.0, 3653.1400000000003, 276, 5169, 4293.5, 5068.8, 5153.1, 5169.0, 7.73754255648406, 919.2487692471371, 4.881301261219437], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-2", 50, 0, 0.0, 1247.2799999999995, 92, 1875, 1447.0, 1780.4, 1797.6, 1875.0, 13.557483731019524, 8.711742475596528, 8.354269760032537], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-1", 50, 0, 0.0, 4821.880000000001, 504, 6812, 5451.5, 6339.099999999999, 6610.15, 6812.0, 7.028394714647174, 1394.8755315223502, 4.2760643625245995], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Non HTTP response code: javax.net.ssl.SSLException/Non HTTP response message: java.net.SocketException: Socket closed", 5, 50.0, 0.6666666666666666], "isController": false}, {"data": ["Assertion failed", 5, 50.0, 0.6666666666666666], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 750, 10, "Non HTTP response code: javax.net.ssl.SSLException/Non HTTP response message: java.net.SocketException: Socket closed", 5, "Assertion failed", 5, null, null, null, null, null, null], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["https://ping-pong-king-666.uc.r.appspot.com/-8", 50, 2, "Non HTTP response code: javax.net.ssl.SSLException/Non HTTP response message: java.net.SocketException: Socket closed", 2, null, null, null, null, null, null, null, null], "isController": false}, {"data": [], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/", 50, 5, "Assertion failed", 5, null, null, null, null, null, null, null, null], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-13", 50, 2, "Non HTTP response code: javax.net.ssl.SSLException/Non HTTP response message: java.net.SocketException: Socket closed", 2, null, null, null, null, null, null, null, null], "isController": false}, {"data": [], "isController": false}, {"data": ["https://ping-pong-king-666.uc.r.appspot.com/-12", 50, 1, "Non HTTP response code: javax.net.ssl.SSLException/Non HTTP response message: java.net.SocketException: Socket closed", 1, null, null, null, null, null, null, null, null], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
