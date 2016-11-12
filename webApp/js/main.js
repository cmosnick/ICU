//When accessing the login and signup pages, 
// if a current session already exists for the username, redirect to the dashboard
// TODO: FIX THIS SO IT DOESN'T ACT DUMB
function hasSession(){
	
	$.get("http://icu.services:5000/session/",
	{},
	function(data, status){		
		if(status === 'success')
		{
			window.location.href = "http://icu.services/Dashboard.html"
		}
	});
}

//When accessing the MyImages, Register, and Settings pages
// if no session exists for the username, redirect to index
// TODO: FIX THIS SO IT DOESN'T ACT DUMB
function hasNoSession(){
	
	$.get("http://icu.services:5000/session/",
	{},
	function(data, status){		
		if(status === 'error')
		{
			window.location.href = "http://icu.services/index.html"
		}
	}).fail(
	function(data, status){		
		if(status === 'error')
		{
			window.location.href = "http://icu.services/index.html"
		}
	});
}

/* TODO: add log functionality, call the api logout function */
function logout(){
	/*$.get("http://icu.services:5000/user/logout/",
	{},
	function(data, status){		
		if(status === 'success')
		{
			window.location.href = "http://icu.services/index.html";
		}
	});*/

	window.location.href = "http://icu.services/index.html";

}

function signUp()
{
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
	$.post("http://icu.services:5000/user/login/",
	{
		username: $("#username").val(),
		password: $("#password").val(),
		
	},
	function(data, status){
		if(status === 'success'){
			$.get("http://icu.services:5000/log/id/5/action/sign in",
			{},
			function(data, status){
				if(status === 'success')
				{
					window.location.href = "http://icu.services/Dashboard.html"
				}
			});
		}
		
	});
}

function getImages(userId, htmlId)
{
	$.get("http://icu.services:5000/image/info/user/id/" + userId,
	{	
	},
	function(data, status){		
		var html = "";
		var baseImageUrl = "http://icu.services:5000/image/id/";
		for(var i = 0; i < data.length; i++)
		{
			var timestamp = data[i].date_time;
			var image_id = data[i].image_id;
			var imageURL = baseImageUrl + image_id;
			
			// TODO: convert timestamp into nice format, insert src url
			html += '<div class="imgContainer"><a target="_blank" href="' + imageURL + '"><img src="' + imageURL + '" alt="Logo"><div class="after">' + timestamp + '</div></a></div>';
		}
		
		$('#' + htmlId).html(html);
		
	});
}