//GOOGLE SIGNIN
//The credit for this method goes to 'Google sign-in for server-side apps' guide.
//See https://developers.google.com/identity/sign-in/web/server-side-flow for details.
function start(){
    gapi.load('auth2',function(){
        auth2 = gapi.auth2.init({
            client_id: '204396521992-k942mpj3pchloa0njikr3g3alu9l7n6v.apps.googleusercontent.com',
            scope: 'openid profile email',
        });
    });
}

function gLogin(session_token){
    auth2.grantOfflineAccess().then(function(authResult){
        if(authResult['code']){
            // Hide signin button to prevent user from clicking it multiple times
            $('#signInButton').attr('style','display:none');

            //send one time code to server
            $.ajax({
                type: 'POST',
                url: '/login/gconnect?state='+session_token,
                headers: {
                    'x-Requested-With': 'XMLHttpRequest'
                },
                processData: false,
                data: authResult['code'],
                contentType: 'application/octet-stream;charset=utf-8',
                success: function(result) {
                    if(!result){
                      $('#result').html('Google OAuth Error: Received error while logging in.');
                    }
                    else{
                      window.location.href = '/welcome'
                    }
                }
            });
        } else {
            $('section.header').append('<ul id="messages"><li class="message">Google OAuth Error: Error occured while communicating with Google server.</li></ul>');
        };
    });
}