
/**
 * Module dependencies.
 */ 
var express = require('express'),
	routes = require('./routes'),
	http = require('http'),
	path = require('path'),
	io = require('socket.io'),
	leapJSONData = require('./lib/parser'),
	Joint = require('./lib/joint'),
	i=0;
	
var app = express(); 

// all environments 
app.set('port', process.env.PORT || 3000); 
app.set('views', path.join(__dirname,'views')); 
app.set('view engine', 'jade'); 
app.use(express.favicon(path.join(__dirname, 'public/images/favicon.ico'))); 
app.use(express.json()); 
app.use(express.urlencoded()); 
app.use(express.methodOverride()); 
app.use(app.router); 
app.use(express.static(path.join(__dirname, 'public'))); 
app.get('/', routes.index);

// create a http server and attach socket.io to it, in order to send websocket messages
var server = http.createServer(app),
	io = io.listen(server); 

// log only socket.io set-up messages to console
io.set('log level',1);

// create an object for each joint
// these objects are used to translate coordinate data to its equivalent sample value on a potentiometer
var base = new Joint(true, 515, (120/235) ), 
	shoulder = new Joint(true, 660, (100/220) ),  
	elbow = new Joint(false, null, (380/720) ),
	wrist = new Joint(true, 515, (60/85) ),
	claw = new Joint(false, null, (90/100) );

	
// tell server what port to have webpage on (3000)
server.listen(app.get('port'), function(){
	console.log('Express server is listening port ' + app.get('port'));
});

// detect when server has connected with a client
console.log('Raspberry Pi Server initilised'); 
console.log('Waiting for client socket to connect...'); 
io.sockets.on('connection', function (socket) { 
	
	console.log('Client connected');
	
	// detect if leap motion websocket message recieved from client
	socket.on('message', function (data) {
  		
		i++;
		// only need to use every fourth message, as messages are being recieved at such a high rate
		if(i%4 === 0){
			
			// process leap data
			frame = new leapJSONData(data);
			
			// if frame containd valid data then proceed
			if(frame.valid) {
				
				// get x, y, z, clawDistance, and wristOrientation
				var x = frame.handPosition.x,
					y = frame.handPosition.y,
					z = frame.handPosition.z,
					clawDistance = frame.distance,
					wristOrientation = frame.fingerOrientataion.y;
				
				// translate coordinate data to its equivalent sample value on a potentiometer and log to console
				// shoulder offset by 80 millimetres, hand detection infront of leap motion not as reliable
				// claw offset to take account of its potentiometer sample range
				console.log("true "+base.translateToSample(x)+" "+shoulder.translateToSample(-z+80)+" "+elbow.translateToSample(y)+" "+(wrist.translateToSample(wristOrientation))+" "+(560-claw.translateToSample(clawDistance))+" "+frame.numOfHands);
			} 
			i=0;
		}
	});
});
