$(function () {
	var socket = io.connect(),
	controller = new Leap.Controller(),
	firstFrame = true;

	// default, assume a leap motion device is not connected to the PC
	$('.tg-center-status-1').text('Disconnected').css('background-color','red'); 

	// create a websocket
	if ((typeof(WebSocket) == 'undefined') && (typeof(MozWebSocket) != 'undefined')) {
		WebSocket = MozWebSocket;
	}

	// connect to the leap motion with the websocket
	var ws = new WebSocket("ws://127.0.0.1:6437/");

	// detect if the leap motion device was connected to the PC
	// indicate this on the table on the webpage
	controller.on( 'deviceConnected' , function() {
		$('.tg-center-status-1').text('Connected').css('background-color','green');
	});

	// detect if the leap motion device was disconnected form the PC
	// indicate this on the table on the webpage
	controller.on( 'deviceDisconnected' , function() {
		$('.tg-center-status-1').text('Disconnected').css('background-color','red');
	});

	// detect if the leap motion websocket is open
	// indicate this on the table on the webpage
	ws.onopen = function(event){      
		$('.tg-center-status-2').text('Connected').css('background-color','green');
	};

	// send leap data to server
	ws.onmessage = function(frame) {
		if(firstFrame){
			$('.tg-center-status-1').text('Connected').css('background-color','green');
			firstFrame = false;
		}
		socket.emit('message', frame.data);
	};

	// detect if the leap motion websocket closed
	// indicate this on the table on the webpage
	ws.onclose = function(event) {
		$('.tg-center-status-2').text('Disconnected').css('background-color','red');
	}

	// detect if the leap motion websocket encountered and error
	// indicate this on the table on the webpage
	ws.onerror = function(event) {
		$('.tg-center-status-2').text('Error').css('background-color','orange');
	};

	// detect if the client and server disconnected
	// indicate this on the table on the webpage
	socket.on('disconnect', function() {
		$('.tg-center-status-3').text('Disconnected').css('background-color','red');
	});

	// detect if the client and server are connected
	// indicate this on the table on the webpage
	socket.on('connect', function() {
		$('.tg-center-status-3').text('Connected').css('background-color','green');
	});

	// detect if the client and server encountered an error
	// indicate this on the table on the webpage
	socket.on('error', function() {
		$('.tg-center-status-3').text('Error').css('background-color','orange');
	});
        
	// turn on controller to detect if a leap is connected/disconnected
	controller.connect();

	// pause function to stop/start video stream and show/hide play icon 
	function pause() {

	 	if ( document.getElementById('webcam').src.indexOf('/?action=stream') != -1 ) {
	    		document.getElementById('webcam').src = $('#webcam').attr('src').split("?")[0]+"?action=snapshot&"+Math.random();
	    		$('#play').addClass('playImage');
			
	 	} else {
	    		document.getElementById('webcam').src = $('#webcam').attr('src').split("?")[0]+"?action=stream";
	    		$('#play').removeClass('playImage');
	  	}
	}

	// exectute play function when video container is clicked 
	$('#play').click(function() {
  		pause();
	})
});