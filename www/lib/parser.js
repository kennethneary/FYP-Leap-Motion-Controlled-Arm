var parser = function(data) {

	// distance where the leap motion cannot distinguish the difference between two fingures
	var minDistanceAllowed = 18;
	
	// turn text into JSON data
	this.leapFrame = JSON.parse(data);
	
	// check if data is valid to move robot arm
	var usableData = function(leapFrame) {
	
		// check if a hand is detected
		if(leapFrame.hands && (leapFrame.hands.length>0)) {
			var handId = leapFrame.hands[0].id;
			
			// check more than one fingure is detected
			if(leapFrame.pointables && (leapFrame.pointables.length>1)) {
				var pointableId1 = leapFrame.pointables[0].handId;
				var pointableId2 = leapFrame.pointables[1].handId;
				
				// make sure the two finures detected belong to the same hand
				if(handId == pointableId1 && handId == pointableId2) {
					return true;
				}
			}
		}
		return false;
	}; 
	
	// get hand coordinates
	var handPosition = function(leapFrame) {
		return {
			x : leapFrame.hands[0].palmPosition[0],
			y : leapFrame.hands[0].palmPosition[1],
			z : leapFrame.hands[0].palmPosition[2]
		};
	};

	// get fingure 1 coordinates
	var finger1Position = function(leapFrame) {
        return {
			x : leapFrame.pointables[0].tipPosition[0],
			y : leapFrame.pointables[0].tipPosition[1],
            z : leapFrame.pointables[0].tipPosition[2]
		};
	};
	
	// get fingure 2 coordinates
	var finger2Position = function(leapFrame) {
        return {
			x : leapFrame.pointables[1].tipPosition[0],
			y : leapFrame.pointables[1].tipPosition[1],
            z : leapFrame.pointables[1].tipPosition[2]
		};
	};
		
	// get distance between fingures
	var distance = function(finger1Position, finger2Position) {
		var xDistance = (finger1Position.x-finger2Position.x);
		var yDistance = (finger1Position.y-finger2Position.y);
		var zDistance = (finger1Position.z-finger2Position.z);
		var totalDistance = Math.sqrt(xDistance*xDistance + yDistance*yDistance + zDistance*zDistance);
		
		if (totalDistance-minDistanceAllowed<0) {
			return 0;
		}else {
			return totalDistance-minDistanceAllowed;
		}
	}
	
	// get finger orientataion to move wrist (average height of fingures used)
	var fingerOrientataion = function(handPosition, finger1Position, finger2Position) {
        return {
			x : (finger1Position.x + finger2Position.x)/2 - handPosition.x,
			y : (finger1Position.y + finger2Position.y)/2 - handPosition.y,
			z : (finger1Position.z + finger2Position.z)/2 - handPosition.z 
        };
	};
	
	// calculate data if valid
	if (usableData(this.leapFrame)) {
		this.valid = true;
		this.numOfHands = this.leapFrame.hands.length;
		this.handPosition = handPosition(this.leapFrame);
		this.finger1Position = finger1Position(this.leapFrame);
		this.finger2Position = finger2Position(this.leapFrame);
		this.distance = distance(this.finger1Position, this.finger2Position);
		this.fingerOrientataion = fingerOrientataion(this.handPosition, this.finger1Position, this.finger2Position);
    }
	else {
        this.valid = false;
    } 
	
};
module.exports = parser;
