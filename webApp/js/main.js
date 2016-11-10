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
		phone_number: $("#phoneNum").val(),
		email: $("#email").val(),
		
	},
	function(data, status){
		if(status === 'success')
		{
			$.get("http://icu.services:5000/log/id/5/action/initial activation",
			{},
			function(data, status){		
				if(status === 'success')
				{
					window.location.href = "http://icu.services/Dashboard.html"
				}
			});
		}
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
		$.get("http://icu.services:5000/log/id/5/action/sign in",
			{},
			function(data, status){
				if(status === 'success')
				{
					window.location.href = "http://icu.services/Dashboard.html"
				}
			});
	});
}