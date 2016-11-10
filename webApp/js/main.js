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
		
		for(var i = 0; i < data.length; i++)
		{
			var timestamp = data[i].date_time;
			var imageURL = data[i].image;
			
			html += '<div class="imgContainer"><a target="_blank" href="' + imageURL + '"><img src="' + 'images/test1.png' + '" alt="Logo"><div class="after">' + timestamp + '</div></a></div>';
		}
		
		$('#' + htmlId).html(html);
		
	});
}