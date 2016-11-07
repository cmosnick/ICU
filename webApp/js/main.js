function signUp()
{
	console.log($("#fname").val());

	//this route will most likely need to change, revisit once the API is up
	$.post("icu.service:5000/user/add/",
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
		alert("Data: " + data + "\nStatus: " + status);
	});
};

function login()
{
	//this route will def need to change, just a placeholder for now
	$.post("icu.service:5000/login/",
	{
		username: $("#username").val(),
		password: $("#password").val(),
		
	},
	function(data, status){
		alert("Data: " + data + "\nStatus: " + status);
	});
}