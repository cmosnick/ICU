function signUp()
{
	console.log($("#fname").val());

	//this route will most likely need to change, revisit once the API is up
	$.post("http://icu.services:5000/user/add/",
	{
		first_name: $("#fname").val(),
		last_name: $("#lname").val(),
		device_id: "1234",
		username: $("#username").val(),
		password: $("#password").val(),
		phone_number: "555-5555",
		email: $("#email").val(),
		
	},
	function(data, status){
		console.log("User add: " );
		console.log(data);
		console.log(status);
	});
	
	
	$.get("http://icu.services:5000/log/id/5/action/initial activation",
	{
		user_id: 7,
		action: 'initial activation',
		
	},
	function(data, status){
		console.log("Log: " );
		console.log(data);
		console.log(status);
	});
	
};

function login()
{
	//this route will def need to change, just a placeholder for now
	$.post("http://icu.services:5000/login/",
	{
		username: $("#username").val(),
		password: $("#password").val(),
		
	},
	function(data, status){
		alert("Data: " + data + "\nStatus: " + status);
	});
}