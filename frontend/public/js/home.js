
function getPlaces(){
	var city = document.getElementById('cities').value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("trip").value = "Select Trip";
       		document.getElementById("main").innerHTML = xhttp.responseText;
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/findPlaces?city="+city, true);
	xhttp.send();
	clearTab()
}

function clearTab() {
	tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-gray", "");
    }
    document.getElementById("foodTab").className += " w3-gray";
}


function addPlace(e) {
	var placeId = e.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
       		document.getElementById("main_modal").innerHTML = xhttp.responseText;
       		document.getElementById("main_modal").style.display = "Block";
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/getPlaceInfo?placeId="+placeId+"&userId="+userId, true);
	xhttp.send();
}


function displayTrip(){

	var tripId = document.getElementById("selectTrip").value;
	if (tripId == "New"){
		document.getElementById("displayAction").style.display = "grid";
		document.getElementById("addTrip").style.display = "None";
	}else{
		if (tripId != ""){
			document.getElementById("displayAction").style.display = "None";
			document.getElementById("addTrip").style.display = "grid";
		}else{
			document.getElementById("displayAction").style.display = "None";
			document.getElementById("addTrip").style.display = "None";
		}
	}; 
}


function createItinerary(evt) {
	var placeId = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var tripName = document.getElementById("tripName").value;
	tripName = escape(tripName);
	console.log(tripName);
	var reserveStartTime = document.getElementById("reserveStartTime").value;
	var reserveEndTime = document.getElementById("reserveEndTime").value;
	var start_am_pm = document.getElementById("start_am_pm").value;
	var end_am_pm = document.getElementById("end_am_pm").value;
	var reserveDay = document.getElementById("reserveDay").value;
	var reserveMonth = document.getElementById("reserveMonth").value;
	var reserveYear = document.getElementById("reserveYear").value;
	var startDay = document.getElementById("startDay").value;
	var startMonth = document.getElementById("startMonth").value;
	var startYear = document.getElementById("startYear").value;
	var endDay = document.getElementById("endDay").value;
	var endMonth = document.getElementById("endMonth").value;
	var endYear = document.getElementById("endYear").value;
	var comment = escape(document.getElementById("comment").value);
	var data = {
		tripName:tripName,
		reserveStartTime:reserveStartTime,
		reserveEndTime:reserveEndTime,
		start_am_pm:start_am_pm,
		end_am_pm:end_am_pm, 
		reserveDay:reserveDay, 
		reserveMonth:reserveMonth, 
		reserveYear:reserveYear, 
		startDay:startDay, 
		startMonth:startMonth, 
		startYear:startYear, 
		endDay:endDay, 
		endMonth:endMonth, 
		endYear:endYear, 
		comment:comment
	}
	var isTrip = document.getElementById("selectTrip").value;
	if (isTrip == "New"){
		var xhttp = new XMLHttpRequest();
	    xhttp.onreadystatechange = function() {
	    	if (this.readyState == 4 && this.status == 200) {
	    		var resp = JSON.parse(xhttp.responseText);
	    		console.log(resp);
	    		window.location.href = "/?userId="+resp['userId'];
	    	}
		};
		xhttp.open("GET", "http://127.0.0.1:8080/createItineraryAction?placeId="+placeId+"&userId="+userId+"&data="+JSON.stringify(data), true);
		xhttp.send();
	}
}

function displayItinerary() {
	var tripId = document.getElementById("trip").value;
	console.log(tripId);
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {

    		document.getElementById("cities").value = "Choose a city";
    		document.getElementById("tabBar").style.display = "None";
       		document.getElementById("main").innerHTML = xhttp.responseText;
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/displayTripItinerary?tripId="+tripId, true);
	xhttp.send();
	clearTab()
}

function addTripToItinerary(evt){

	var placeId = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var reserveStartTime = document.getElementById("reserveStartTime").value;
	var reserveEndTime = document.getElementById("reserveEndTime").value;
	var start_am_pm = document.getElementById("start_am_pm").value;
	var end_am_pm = document.getElementById("end_am_pm").value;
	var reserveDay = document.getElementById("reserveDay").value;
	var reserveMonth = document.getElementById("reserveMonth").value;
	var reserveYear = document.getElementById("reserveYear").value;
	var comment = escape(document.getElementById("comment").value);
	var tripId= document.getElementById("selectTrip").value;
	var data = {
		placeId:placeId,
		reserveStartTime:reserveStartTime,
		reserveEndTime:reserveEndTime, 
		comment:comment,
		reserveDay: reserveDay,
		reserveMonth:reserveMonth,
		reserveYear:reserveYear,
		start_am_pm:start_am_pm,
		end_am_pm:end_am_pm
	}
	console.log(data);
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("trip").value = tripId;
    		displayItinerary()
       		document.getElementById("main_modal").style.display = "None";
       		document.getElementById("trip").value = "Select Trip";
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/addPlaceToItinerary?userId="+userId+"&data="+JSON.stringify(data)+"&tripId="+tripId, true);
	xhttp.send();
}

function editTripItinerary(evt){

	var itemGuid = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var placeId = document.getElementById("placeId").value;
	var reserveStartTime = document.getElementById("reserveStartTime").value;
	var start_am_pm = document.getElementById("start_am_pm").value;
	var end_am_pm = document.getElementById("end_am_pm").value;
	var reserveEndTime = document.getElementById("reserveEndTime").value;
	var reserveDay = document.getElementById("reserveDay").value;
	var reserveMonth = document.getElementById("reserveMonth").value;
	var reserveYear = document.getElementById("reserveYear").value;
	var comment = escape(document.getElementById("comment").value);
	var tripGuid= document.getElementById("tripGuid").value;
	var data = {
		tripGuid:tripGuid,
		placeId:placeId,
		reserveStartTime:reserveStartTime,
		reserveEndTime:reserveEndTime, 
		comment:comment,
		reserveDay: reserveDay,
		reserveMonth:reserveMonth,
		reserveYear:reserveYear,
		start_am_pm:start_am_pm,
		end_am_pm:end_am_pm
	}
	console.log(data);
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("trip").value = tripGuid;
    		displayItinerary()
       		document.getElementById("main_modal").style.display = "None";
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/editTripItinerary?userId="+userId+"&data="+JSON.stringify(data)+"&itemGuid="+itemGuid, true);
	xhttp.send();
}

function editTripAction(){
	document.getElementById("tripTableDisplay").style.display = "none";
	document.getElementById("tripTableEdit").style.display = "block";
	document.getElementById("editTripButton").style.display = "none";
	document.getElementById("deleteTripButton").style.display = "none";
}

function closeTripEdit(){
	document.getElementById("tripTableDisplay").style.display = "block";
	document.getElementById("tripTableEdit").style.display = "none";
	document.getElementById("editTripButton").style.display = "block";
	document.getElementById("deleteTripButton").style.display = "block";
}

function updateTripAction(evt){
	var userId = document.getElementById("userId").value;
	var guid = evt.getAttribute("data-record");
	var tripName = document.getElementById("tripName").value;
	var startDay = document.getElementById("startDay").value;
	var startMonth = document.getElementById("startMonth").value;
	var startYear = document.getElementById("startYear").value;
	var endDay = document.getElementById("endDay").value;
	var endMonth = document.getElementById("endMonth").value;
	var endYear = document.getElementById("endYear").value;
	var data = {
		tripName: tripName,
		startDay:startDay, 
		startMonth:startMonth, 
		startYear:startYear, 
		endDay:endDay, 
		endMonth:endMonth, 
		endYear:endYear
	};
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("trip").value = guid;
			displayItinerary();
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/updateTripsTable?userId="+userId+"&data="+JSON.stringify(data)+"&guid="+guid, true);
	xhttp.send();
}

function displayTripItemAction(evt) {
	var userId = document.getElementById("userId").value;
	var id = evt.getAttribute('data-record');
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("main_modal").innerHTML = xhttp.responseText;
       		document.getElementById("main_modal").style.display = "Block";
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/displayTripItem?userId="+userId+"&id="+id, true);
	xhttp.send();

}


function deleteTripAction(evt){
	var tripGuid = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		document.getElementById("main_modal").innerHTML = xhttp.responseText;
       		document.getElementById("main_modal").style.display = "Block";
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/selectTripView?userId="+userId+"&tripGuid="+tripGuid, true);
	xhttp.send();

}

function deleteTrip(evt){
	var tripGuid = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		var response = JSON.parse(xhttp.responseText);
    		console.log(response);
    		if (response['status'] == "success"){
    			document.getElementById("main_modal").style.display = "None";
       			window.location.href = "/?userId="+response["userId"];
    		}
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/deleteTripAction?userId="+userId+"&tripGuid="+tripGuid, true);
	xhttp.send();
}


function deleteItineraryItem(evt){
	var itemGuid = evt.getAttribute("data-record");
	var userId = document.getElementById("userId").value;
	var tripGuid= document.getElementById("tripGuid").value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
    		var response = JSON.parse(xhttp.responseText);
    		console.log(response);
    		if (response['status'] == "success"){
    			document.getElementById("trip").value = tripGuid;
    			document.getElementById("main_modal").style.display = "None";
       			displayItinerary();
    		}
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/deleteItineraryItem?userId="+userId+"&itemGuid="+itemGuid, true);
	xhttp.send();
}









