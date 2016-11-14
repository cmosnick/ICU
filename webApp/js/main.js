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

function populateSettings(data, status)
{
	for(var i = 0; i < data.length; i++)
	{
		var startTime = data[i].start_time.substring(0, data[i].start_time.length - 3);
		var endTime = data[i].end_time.substring(0, data[i].end_time.length - 3);
		var notifyBy = data[i].notification_option_id;
		var startAMorPM = 0, endAMorPM = 0;
		
		if(parseInt(startTime.substring(0,2), 10) > 12)
		{
			startAMorPM = 1;
			var time24 = parseInt(startTime.substring(0,2), 10);
			time24 = time24 - 12;
			startTime = time24.toString() + startTime.substring(2,startTime.length);
		}
		
		if(parseInt(endTime.substring(0,2), 10) > 12)
		{
			endAMorPM = 1;
			var time24 = parseInt(endTime.substring(0,2), 10);
			time24 = time24 - 12;
			endTime = time24.toString() + endTime.substring(2,endTime.length);
		}
		
		if(startTime.charAt(0) == 0){
			startTime = startTime.substring(1, startTime.length);
		}
		if(endTime.charAt(0) == 0){
			endTime = endTime.substring(1, endTime.length);
		}
		
		writeTime(startTime, startAMorPM, endTime, endAMorPM, notifyBy);
	}
	
	function writeTime(startTime, startAMorPM, endTime, endAMorPM, notifyBy)
	{	
		console.log("S: " + startTime + " " + startAMorPM);
		console.log("E: " + endTime + " " + endAMorPM);
		console.log("N: " + notifyBy + "\n");
		$("#notificationContainer").css("visibility", "visible");
		$("#notificationContainer").append('<div class="loadHtml margin30"></div>');
		$(".loadHtml:last").load("notification.html", function(){
			$(this).children('#startTime').val(startTime);
			$(this).children('#startTimeAMPM').prop('selectedIndex', startAMorPM);
			$(this).children('#endTime').val(endTime);
			$(this).children('#endTimeAMPM').prop('selectedIndex', endAMorPM);
			$(this).children('#notify').prop('selectedIndex', notifyBy - 1);
		});			
	}
};

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