function signInCallback(authResult){
	if(authResult['code']){
		// Hide signin button to prevent user from clicking it multiple times
		$('#signInButton').attr('style','display:none');

		//send one time code to server
		$.ajax({
			type: 'POST',
			url: '/gconnect?state={{session_state}}',
			processData: false,
			data: authResult['code'],
			contentType: 'application/octet-stream;charset=utf-8',
			success: function() {
				window.location.href = "/welcome" 
			} 
		});
	
	} else if (authResult['error']) {
		//display error on page
		if($('#messages').length) {
			$('#messages').html("<li class='message'>Google OAuth Error: Received error while logging in with Google. Received authResult['error'].</li>")
		} else {
			$('section.header').append("<ul id='messages'><li class='message'>Google OAuth Error: Received error while logging in with Google. Received authResult['error'].</li></ul>")
		}
		
	} else {
		if($('#messages').length) {
			$('#messages').html("<li class='message'>Google OAuth Error: Failed to establish communication. authResult returned None.</li>")
		} else {
			$('section.header').append("<ul id='messages'><li class='message'>Google OAuth Error: Failed to establish communication. authResult returned None.</li></ul>")
		}

	} 
} 