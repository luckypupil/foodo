function sendloco (loc) {	
	var baseUrl = window.location;
	if (window.location.search == "") {
		var fct = ''+'?';
		var lat = loc.coords.latitude;
		var lng	= loc.coords.longitude;
		window.location = baseUrl+fct+'lat='+lat+'&lng='+lng;
	}};
	
function errorloco (loc) {
	alert("You're either outside our current coverage area or you're a spy - here's a list of the most recent inspections instead!")	
	//window.location = window.location+'noloco';
	window.location = 'noloco';
	};

	



