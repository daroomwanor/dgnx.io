function getPlaces(){
	var city = document.getElementById('cities').value;
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
       		document.getElementById("main").innerHTML = xhttp.responseText;
    	}
	};
	xhttp.open("GET", "http://127.0.0.1:8080/findPlaces?city="+city, true);
	xhttp.send();
}
