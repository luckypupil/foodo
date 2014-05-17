function sendloco (loc) {	
	var baseUrl = window.location;
	var fct = ''+'?';
	var lat = loc.coords.latitude;
	var lng	= loc.coords.longitude;
	window.location = baseUrl+fct+'lat='+lat+'&lng='+lng;
	};
	



