var http = require('http');
var express = require('express');
var app = express();
var port = process.env.PORT || 8080;
var url = require('url');
var nodemailer = require('nodemailer');
var smtpTransport = require('nodemailer-smtp-transport');

var config = require('./config');
var client = require('twilio')(config.accountSid, config.authToken);

app.get('/sendSMS', function(req, res){
	var numAppend = '+1';
	var formattedNum;
	//User's number
	var toNum = req.query.toNum; // $_GET["toNum"]
	//Twilio number
	var fromNumber = config.sendingNumber;
	//Message text
	var text = req.query.text; // $_GET["text"]
	//Image server URL
	var image = req.query.image;
	
	if(toNum[0] != '+' && toNum[1] != '1'){
		formattedNum = numAppend.concat(toNum)
	}
	else{
		formattedNum = toNum;
	}
		//Create message
		client.sendMessage({
			to: formattedNum,
			from: fromNumber,
			body: text,
			mediaUrl: image,
		}, function(err, data){
			if(err)
				console.log(err);
			console.log(data);
			console.log(req);
		});
		
		res.end('Response Ended');
});

app.get('/emailUser', function(req, res){
	//User's email
	var toEmail = req.query.toEmail; // $_GET["toEmail"]
	//ICU Alerts email
	var fromEmail = config.fromEmail;
	var pass = config.pass;
	
	//Authenticate email credentials
	var transport = nodemailer.createTransport(smtpTransport({
		host: 'smtp.mail.yahoo.com',
		secureConnection: true,
		port: 465,
		auth:{
			user: fromEmail,
			pass: pass
		}
	}));
	
	//Prepare email body
	var imgUrl = "'http://s1.thingpic.com/images/HU/CDZn4zEZTgyRP5eiPQoJeye3.jpeg'";
	var mailOptions = {
		from: 'ICU Alerts <ICUAlerts@yahoo.com>',
		to: toEmail,
		subject: 'Movement Detected',
		text: 'This is an updated test!',
		html: '<p>This is an updated test! <br> <img src=' + imgUrl + '/></p>'
	};
	
	//Send email
	transport.sendMail(mailOptions, function(error, info){
		if(error){
			return console.log(error);
		}
		console.log('Message sent: ' + info.response);
	});
	res.end('Response Ended');
});

app.listen(port);
console.log('Server running on port: ' + port);

// Export Express app
module.exports = app;
