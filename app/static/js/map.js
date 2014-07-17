function sendloco (loc) {	
	var baseUrl = window.location;
	if (window.location.search == "") {
		var fct = ''+'?';
		var lat = loc.coords.latitude;
		var lng	= loc.coords.longitude;
		window.location = baseUrl+fct+'lat='+lat+'&lng='+lng;
	}};
	
function errorloco (loc) {
	alert("Tisk was unable to obtain your location to send you the closest inspections to your current location but here's a list of the most recent PHl food inspections!")	
	window.location = window.location+'noloco';
	};

	



