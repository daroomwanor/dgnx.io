var express = require('express');
var app = express();

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
	sql = "SELECT * FROM placesTable";
	resp= []
	db.all(sql, function(error, rows){
		rows.forEach(function(row){
			resp.push(row);
		});
		if(error){
			console.log(error);
		}
		console.log(resp)
		render('home', {'places': resp})
	});
});

app.listen(8080, '0.0.0.0');
console.log("Server is running on port 8080");


