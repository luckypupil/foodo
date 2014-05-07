function initialize (rests,center) {    
    var center = new google.maps.LatLng(center.coords.latitude, center.coords.longitude);
        		
    var mapOptions = {
	    center: center,
	    zoom: 14
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);	

    var homeMarker = new google.maps.Marker({
		    position: center,
		    map: map,
		    title: 'Foodo HQ'
	    });
    
    var i = 0;
    var restLen = rests.length;
    
    for (i;i<restLen;i++) {
	    var locale = new google.maps.LatLng(rests[i]['lat'], rests[i]['lng']);
     	
     	var homeMarker2 = new google.maps.Marker({
        		position: locale,
        		map: map,
        		tite: rests[i]['name']
	    });
	}//end for
    
    }
