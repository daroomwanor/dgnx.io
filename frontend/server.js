var express = require('express');
var app = express();

const http = require('http');
const url = require('url');

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('./db/vos.db');

app.get('/', function(req,res){
	sql = "SELECT * FROM citiesTable ORDER BY cityName ASC";
	cities = [];
	db.all(sql, function(err, rows) {
		rows.forEach(function(row){
			cities.push(row);
		});
		console.log(cities)
		res.render('index', {'cities': cities});
	});

});

app.get('/findPlaces', function(request,response){
	const queryObject = url.parse(request.url, true).query;
	city = queryObject.city;
	sql = 'SELECT * FROM placesTable WHERE city = ?';
	respData= []
	db.all(sql,city, function(error, rows){
		rows.forEach(function(row){
			respData.push(row);
		});
		response.render('places', {'places':respData});
	});
});

app.get('/backpage', function(request, response){
	sql = 'select distinct(city) from placesTable';
	cities= []
	db.all(sql, function(error, rows){
		rows.forEach(function(row){
			cities.push(row);
		});
		response.render('cities', {'cities':cities});
	});
});

app.listen(8080, '0.0.0.0');
console.log("Server is running on port 8080");


