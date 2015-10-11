var timeout = require('connect-timeout');
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var fs = require('fs');
var path = require('path');
var jsonParser = bodyParser.json();

var port = 80;

app.get('/lookup', function(req, res) {
	console.log('Lookup endpoint');
	var query = req.query.q;
	console.log('Spawning spotify.py');
	var spawn = require("child_process").spawn;
	var process = spawn('python', ["scripts/Spotify.py", query]);
	process.stdout.on('data', function (data) {
		console.log("[Spotify.py stdout] " + data.toString());
		if (/^\s*$/.test(data.toString())) {
			res.setHeader('Content-Type', 'text/html');
			res.send('Not found');
		} else {
			res.setHeader('Content-Type', 'application/json');
			res.send(data);
		}
	});
	process.stderr.on('data', function(data) {
		console.log("[Spotify.py stderr] " + data.toString());
	});
});

app.post('/initiate', jsonParser, function(req, res) {
	//console.log(req.body);
	//console.log('Initiate endpoint');
	str = JSON.stringify(req.body);
	console.log(str);
	var hash = require('crypto').createHash('md5').update(str).digest('hex');
	console.log('Spawning KAT.py');
	var spawn = require("child_process").spawn;
	var process = spawn('python', ["scripts/KAT.py", str, hash]);
	process.stdout.on('data', function (tor) {
		console.log("[KAT.py stdout] " + tor.toString());
		if (/^\s*$/.test(tor.toString())) {
			res.setHeader('Content-Type', 'text/html');
			res.send('Not found');
		} else {
			console.log('Spawning bittorrent.py');
			var p2 = spawn('python', ["scripts/bittorrent.py", tor, req.body.title, hash]);
			p2.stdout.on('data', function (stat) {
				console.log("[bittorrent.py stdout] " + stat.toString());
			});
			p2.stderr.on('data', function (data) {
				console.log("[bittorrent.py stderr] " + data.toString());
			});
			res.send(hash);
		}
	});
	process.stderr.on('data', function (data) {
		console.log('[KAT.py stderr] ' + data.toString());
	});
});

app.get('/ready', function(req, res) {
	console.log('Ready endpoint');
	var hash = req.query.hash;
	if (!fileExists(path.join("outbox", hash))) {
		res.send("None");
	} else {
		fs.readdir(path.join("outbox", hash), function(err, files) {
			if (err) throw err;
			if (files.length == 0) {
				res.send("Error: Missing audio file");
			}
			else {
				files.forEach(function(file) {
					res.sendFile(path.join(__dirname, "outbox", hash, file));
				});
			}
		});
	}
});
	
function fileExists(filePath) {
	try {
		return fs.statSync(filePath).isDirectory();
	} catch (err) {
		return false;
	}
}

app.listen(port, function() {
	console.log('Express server listening on port ' + port);
});
