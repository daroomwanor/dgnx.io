const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const router  = express.Router();
const app = express();

var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('./db/vos.db');

var uuid = require('uuid');
const http = require('http');
const url = require('url');
var sess;

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
app.use(session({secret:"guid", saveUninitialized:true, resave:true}));
app.use(bodyParser.json());      
app.use(bodyParser.urlencoded({extended: true}));


router.get('/', function(request,response){
	var req = url.parse(request.url, true).query;
	sess = request.session;
	trips = [];
	if (req.userId != undefined){
		sql = "SELECT * FROM tripsTable WHERE userGuid = ?";
		db.all(sql, req.userId, function(err, rows) {
			if (rows.length > 0){
				rows.forEach(function(row){
					trips.push(row);
				});
			}
			console.log(err);
		});
	}
	sql = "select distinct(city) from placesTable order by city ASC";
	cities = [];
	db.all(sql, function(err, rows) {
		rows.forEach(function(row){
			cities.push(row);
		});
		response.render('home', {'cities': cities, 'trips':trips});
	});

});


router.get('/displayTripItinerary', function(request, response){
	sess = request.session;
	var req = url.parse(request.url, true).query;
	var sql = 'SELECT * FROM itineraryTable as itin LEFT JOIN placesTable as place ON place.Id = itin.placeId LEFT JOIN tripsTable as trip ON trip.tripGuid = itin.tripGuid  WHERE trip.tripGuid = ?';
	var places = [];
	var city = "";
	db.all(sql, req.tripId, function(err, rows) {
		if(rows.length > 0){
			city = rows[0]["city"]; 
			rows.forEach(function(row){
				places.push(row);
			});
		}
		db.all('SELECT * FROM placesTable WHERE city = ?', city, function(err,rows){
			console.log(rows);
			response.render('itinerary', {'data': places, 'new_data':rows});
		});
	});

});

router.get('/addPlaceToItinerary', function(request, response){
	sess = request.session;
	const queryObject = url.parse(request.url, true).query;
	var jsonData = JSON.parse(queryObject.data);
	var tripGuid = queryObject.tripId;
	var itemGuid = uuid.v4();
	var placeId = jsonData['placeId'];
	var reserveStartTime = jsonData['reserveStartTime'];
	var reserveEndTime = jsonData['reserveEndTime'];
	var start_am_pm = jsonData['start_am_pm'];
	var end_am_pm = jsonData['end_am_pm'];
	var start_am_pm = jsonData['start_am_pm'];
	var end_am_pm = jsonData['end_am_pm'];
	var reserveDay = jsonData['reserveDay'];
	var reserveMonth = jsonData['reserveMonth'];
	var reserveYear = jsonData['reserveYear'];
	var comment = jsonData['comment'];
	console.log(jsonData);
	var insert_into_itinerary = "INSERT INTO itineraryTable (tripGuid, placeId, itemGuid, reserveStartTime, reserveEndTime,start_am_pm, end_am_pm, reserveDay, reserveMonth, reserveYear, placeInfo) VALUES (?,?,?,?,?,?,?,?,?,?,?)";
	db.run(insert_into_itinerary, [tripGuid, placeId, itemGuid, reserveStartTime, reserveEndTime,start_am_pm, end_am_pm, reserveDay,reserveMonth,reserveYear,comment], function(err, rows) {
		if(err){
			console.log(err);
			response.write("Error");
			response.send();
		}else{
			response.write(JSON.stringify({"response":"success",}));
			response.send();
		}
	});


});

router.get('/editTripItinerary', function(request, response){
	sess = request.session;
	const queryObject = url.parse(request.url, true).query;
	var jsonData = JSON.parse(queryObject.data);
	var tripGuid = jsonData['tripGuid'];
	var itemGuid = queryObject.itemGuid;
	var placeId = jsonData['placeId'];
	var reserveStartTime = jsonData['reserveStartTime'];
	var reserveEndTime = jsonData['reserveEndTime'];
	var start_am_pm = jsonData['start_am_pm'];
	var end_am_pm = jsonData['end_am_pm'];
	var reserveDay = jsonData['reserveDay'];
	var reserveMonth = jsonData['reserveMonth'];
	var reserveYear = jsonData['reserveYear'];
	var userId = queryObject.userId;
	var comment = jsonData['comment'];
	console.log(jsonData);
	update_sql = "UPDATE itineraryTable SET tripGuid =?,placeId=?,reserveStartTime=?,reserveEndTime=?,start_am_pm=?, end_am_pm=?,reserveDay=?,reserveMonth=?,reserveYear=?,placeInfo=? WHERE itemGuid=?";
	db.run(update_sql, [tripGuid, placeId, reserveStartTime, reserveEndTime,start_am_pm, end_am_pm,reserveDay,reserveMonth,reserveYear,comment, itemGuid], function(err, rows) {
		if(err){
			console.log(err);
			response.write(JSON.stringify({"response":"failed", "userId":userId}));
			response.send();
		}else{
			response.write(JSON.stringify({"response":"success", "userId":userId}))
			response.send();
		}
	});


});

router.post('/login', function(request, response) {
	var email = request.body.email;
	var password = request.body.pass;
	sess = request.session;
	sess.email = email;
	response.write("Found")
});

router.get('/getPlaceInfo', function (request, response) {
	sess = request.session;
	var req = url.parse(request.url, true).query;
	var placeId = req.placeId;
	var userId = req.userId;
	sql = "SELECT * FROM tripsTable WHERE userGuid = ?";
	trips = [];
	db.all(sql, userId, function(err, rows) {
		if (rows.length > 0){
			rows.forEach(function(row){
				trips.push(row);
			});
		}
	});
	sql = 'SELECT * FROM placesTable WHERE Id = ?';
	place= [];
	db.all(sql,placeId, function(error, rows){
		rows.forEach(function(row){
			place.push(row);
		});
		response.render('displayPlace', {'data':[place, trips]});
	});
	
});

router.get('/findPlaces', function(request,response){
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

router.get("/createItineraryAction", function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var jsonData = JSON.parse(queryObject.data);
	var placeId = queryObject.placeId;
	var userId = queryObject.userId;
	var tripGuid = uuid.v4();
	var startDay = jsonData['startDay'];
	var startMonth = jsonData['startMonth'];
	var startYear = jsonData['startYear'];
	var endDay = jsonData['endDay'];
	var endMonth = jsonData['endMonth'];
	var endYear = jsonData['endYear'];
	var reserveStartTime = jsonData['reserveStartTime'];
	var reserveEndTime = jsonData['reserveEndTime'];
	var start_am_pm = jsonData['start_am_pm'];
	var end_am_pm = jsonData['end_am_pm'];
	var reserveDay = jsonData['reserveDay'];
	var reserveMonth = jsonData['reserveMonth'];
	var reserveYear = jsonData['reserveYear'];
	var comment = jsonData['comment'];

	if (jsonData['tripName'] != ""){
		var sql = 'SELECT * FROM tripsTable WHERE tripName = ? AND userGuid = ?';
		db.all(sql, [jsonData['tripName'], userId], function(error, row) {
			if (row.length < 1 ){
				sql = "INSERT INTO tripsTable (tripName, userGuid, tripGuid, startDay, startMonth, startYear, endDay,endMonth,endYear,tripInfo) VALUES (?,?,?,?,?,?,?,?,?,?)";
				db.run(sql,[jsonData['tripName'],userId,tripGuid,startDay, startMonth, startYear, endDay,endMonth,endYear,jsonData['comment']], function(err, resp){
					if (!err){
						var itemGuid = uuid.v4();
						var reserveTime = jsonData['reserveTime'];
						var reserveDate = jsonData['reserveMonth']+"/"+jsonData['reserveDay']+"/"+jsonData["reserveYear"];
						var comment = jsonData['comment']
						var insert_into_itinerary = "INSERT INTO itineraryTable(tripGuid, placeId, itemGuid, reserveStartTime, reserveEndTime,start_am_pm,end_am_pm, reserveDay, reserveMonth, reserveYear, placeInfo) VALUES (?,?,?,?,?,?,?,?,?,?,?)";
						db.run(insert_into_itinerary, [tripGuid, placeId, itemGuid, reserveStartTime, reserveEndTime,start_am_pm, end_am_pm,reserveDay,reserveMonth,reserveYear,comment], function(err, rows) {
							if(err){
								console.log(err);
								response.write(JSON.stringify({"response":"failed", "userId":userId}))
								response.send();
							}else{
								response.write(JSON.stringify({"response":"success", "userId":userId}));
								response.send();
							}
						});
						
					}else{
						console.log(err);
						response.write(JSON.stringify({"response":"failed", "userId":userId}))
						response.send();
					}
				});

			}else{
				response.write(JSON.stringify({"status":"failed"}));
				response.send();
			}
		});

	}

});


router.get('/updateTripsTable', function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var jsonData = JSON.parse(queryObject.data);
	var guid = queryObject.guid;
	var userId = queryObject.userId;
	var startDay = jsonData['startDay'];
	var startMonth = jsonData['startMonth'];
	var startYear = jsonData['startYear'];
	var endDay = jsonData['endDay'];
	var endMonth = jsonData['endMonth'];
	var endYear = jsonData['endYear'];
	var comment = jsonData['comment'];
	var sql = "UPDATE tripsTable SET tripName = ?, startDay = ?, startMonth = ?, startYear = ?, endDay = ?, endMonth = ?, endYear = ?, tripInfo = ? WHERE tripGuid = ?";
	db.run(sql, [jsonData['tripName'], startDay, startMonth, startYear, endDay, endMonth, endYear, comment, guid], function(error, rows){
		if(!error){
			response.write(JSON.stringify({"response":"success", "userId":userId}))
			response.send()
		}else{
			console.log(error);
			response.write(JSON.stringify({"response":"failed", "userId":userId}))
		}
	});
});

router.get('/displayTripItem', function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var id = queryObject.id;
	var userId = queryObject.userId;
	console.log(id);
	sql = 'SELECT * FROM itineraryTable as itin LEFT JOIN placesTable as place ON place.Id = itin.placeId LEFT JOIN tripsTable as trip ON trip.tripGuid = itin.tripGuid WHERE itin.itemGuid = ?';
	db.all(sql, id, function(error, rows){
		if(!error){
			console.log(rows);
			response.render('displayTripItem', {'data':rows});
		}else{
			console.log(error);
			response.write(JSON.stringify({"response":"failed", "userId":userId}));
			response.send();
		}
	});
});

router.get('/selectTripView', function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var userId = queryObject.userId;
	var tripGuid = queryObject.tripGuid;

	sql = 'SELECT * FROM tripsTable WHERE tripGuid = ?';

	db.all(sql, tripGuid, function (error, rows) {
		if(!error){
			response.render("deleteTripView", {'data':rows});
		}else{
			console.log(error);
		}
	});

});

router.get('/deleteTripAction', function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var userId = queryObject.userId;
	var tripGuid = queryObject.tripGuid;

	sql = 'DELETE FROM tripsTable WHERE tripGuid = ?';

	db.run(sql, tripGuid, function (error, rows) {
		if(!error){
			console.log("Delete Trip Action")
			response.write(JSON.stringify({"status":"success", "userId": userId}));
			response.send();
		}else{
			console.log(error);
			response.write(JSON.stringify({"status":"failed", "userId": userId}));
			response.send();
		}
	});

});

router.get('/deleteItineraryItem', function(request, response){
	const queryObject = url.parse(request.url, true).query;
	var userId = queryObject.userId;
	var itemGuid = queryObject.itemGuid;

	sql = 'DELETE FROM itineraryTable WHERE itemGuid = ?';

	db.run(sql, itemGuid, function (error, rows) {
		if(!error){
			console.log("Delete itinerary Action")
			response.write(JSON.stringify({"status":"success", "userId": userId}));
			response.send();
		}else{
			console.log(error);
			response.write(JSON.stringify({"status":"failed", "userId": userId}));
			response.send();
		}
	});

});


app.use('/', router);
app.listen(8080, '0.0.0.0');
console.log("Server is running on port 8080");
