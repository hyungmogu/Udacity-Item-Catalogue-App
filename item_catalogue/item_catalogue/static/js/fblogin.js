// FB SIGNIN
//The credit for this approach goes to 'Facebook Login for the Web with Javascript SDK' guide.
//See https://developers.facebook.com/docs/facebook-login/web for details.
function fbLogin(session_token){
    FB.login(function(response){
        sendTokenToServer(response,session_token);
    },{'scope': 'public_profile,email'});
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '1754114728182463',
        cookie     : true,  // enable cookies to allow the server to access 
                            // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.8' // use graph api version 2.8
    });
};

// Load the SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function sendTokenToServer(response, session_token){
    var access_token = response.authResponse.accessToken;
    $.ajax({
        type: 'POST',
        url: '/login/fbconnect?state='+session_token,
        processData: false,
        data: access_token,
        contentType: 'application/octet-stream; charset=utf-8',
        success: function(result){
            if(!result){
                $('#result').html('Facebook OAuth Error: Received error while logging in.');
            } else{
                window.location.href = '/welcome';
            }
        }
    });
}