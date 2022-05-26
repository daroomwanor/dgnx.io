var express = require('express');
var app = express();

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('./db/vos.db');

app.get('/', function(req,res){
	sql = "SELECT * FROM citiesTable";
	data = []
	db.get(sql, function(err, row) {
		console.log({'city':row.cityName, 'country':row.country});
		data.push({'city':row.cityName, 'country':row.country});
	});
	res.render('index', {'data': data});
});

app.listen(8080, '0.0.0.0');
console.log("Server is running on port 8080");


