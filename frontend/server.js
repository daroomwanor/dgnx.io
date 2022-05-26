var express = require('express');
var app = express();

app.set('view engine', 'ejs');

app.get('/', function(req,res){
	res.render('index');
});

app.listen(8080, '0.0.0.0');
console.log("Server is running on port 8080");
