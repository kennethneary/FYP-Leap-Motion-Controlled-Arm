var Joint = function(symmetricJoint, midPoint, sampleRate) {
	
	// function to translate coordinate data to its equivalent sample value on a potentiometer
	var translateToSample = function(pos) {
	
		if(symmetricJoint) {
			return Math.round(midPoint + (pos/sampleRate));    
		}
		return Math.round(pos/sampleRate);      
    };
	
	// return function
	return {
		translateToSample: translateToSample
    };
		
};

module.exports = Joint;