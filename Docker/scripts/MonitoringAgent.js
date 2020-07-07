var http = require('http');
var fs = require('fs');
const register = require('prom-client').register;
const client = require('prom-client');
const gaugeMetrics =new client.Gauge({
	name: 'nodered_logs',
	help: 'Logs for nodered',
	labelNames: ['time', 'message','type'],
});

const gaugeMetricsSum =new client.Gauge({
	name: 'nodered_logs_count',
	help: 'Count of nodered logs',
	labelNames: ['type'],
});

var logLevelMap = new Map([[10,'Fatal'], [20 , 'Error'], [30, 'Warning'], [40 ,'Info' ]]);
var offset=0;
var fileSize=0;
var message="";
var logType="";
var time="";
var msg="";
var fatalCounter=0, errorCounter=0, infoCounter=0, warningCounter=0;
var fstat;
var bytesToRead;
http.createServer(function (req, res) {

        if (req.url== "/metrics") {
            try{
				var fd=fs.openSync('/var/log/node-red/nodered.log', 'r');
				fsstat=fs.fstatSync(fd);
				fileSize=fsstat.size;
				bytesToRead=fileSize-offset;
				var buffer=Buffer.alloc(bytesToRead);
				var read=fs.readSync(fd, buffer, 0, bytesToRead, offset);
				var arrayOfLogs=buffer.toString('utf8').split("\n");
				for ( let element of arrayOfLogs){
					if (element != ""){
						msg = JSON.parse(element);
                        logType=logLevelMap.get(msg.level);
						switch (msg.level) {
							case 10:
								message=JSON.stringify(msg.msg);
								fatalCounter=fatalCounter+1;
								break;
							case 20:
								message=JSON.stringify(msg.msg);
								errorCounter=errorCounter+1;
								break;
							case 30:
								message=msg.msg;
								warningCounter=warningCounter+1;
								break;
							case 40:
								message=msg.msg;
								infoCounter=infoCounter+1;
								break;
						}
                        time=(new Date(msg.timestamp)).toLocaleString();
                        gaugeMetrics.labels(time, message, logType).set(msg.level);
                    }
				}
				
                gaugeMetricsSum.labels("Fatal").set(fatalCounter);
				gaugeMetricsSum.labels("Error").set(errorCounter);
				gaugeMetricsSum.labels("Warning").set(warningCounter);
				gaugeMetricsSum.labels("Info").set(infoCounter);

                fs.closeSync(fd);

			catch(err){
				console.error("Error generating metric.");
			}
			finally {
                res.setHeader('Content-Type', register.contentType);
                res.end(register.metrics());
                //Flush out all data
				register.resetMetrics();
				//Reset counters
				offset = fileSize;
			    fatalCounter=0;
				errorCounter=0;
				infoCounter=0;
				warningCounter=0;				
			}
        }
        else{
            res.writeHead(200);
            res.end(JSON.stringify({message:"Append /metrics to get Prometheus metrics "}));
        }
}).listen(1885);
