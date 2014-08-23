function sendloco (loc) {	
	var baseUrl = window.location;
	if (window.location.search == "") {
		var fct = ''+'?';
		var lat = loc.coords.latitude;
		var lng	= loc.coords.longitude;
		window.location = baseUrl+fct+'lat='+lat+'&lng='+lng;
		console.log(window.location);		
	}};
	
function errorloco (loc) {
	alert("You're either outside our current coverage area or you're a spy - here's a list of the most recent inspections instead!")	
	//window.location = window.location+'noloco';
	window.location = 'noloco';
	};

function geocode (addy,restNm) {
	//set geo bounds for Philly
	var swCorn = new google.maps.LatLng(40.1379919,-75.280303);
	var neCorn = new google.maps.LatLng(39.8670041,-74.95576289999997);
	var philBounds = new google.maps.LatLngBounds(swCorn,neCorn);
	var geocoder = new google.maps.Geocoder();
	if (addy) {
	var answer = geocoder.geocode( {'address':addy, 'bounds':philBounds }, function(results,status) {
		if (status == google.maps.GeocoderStatus.OK) {
			var lng = results[0].geometry.location.B;
			var lat = results[0].geometry.location.k;
			baseUrl = window.location.origin;
			window.location = baseUrl+'/?lat='+lat+'&lng='+lng+'&search='+restNm;
		}
		})
	}
	};
