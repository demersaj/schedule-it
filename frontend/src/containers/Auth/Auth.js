import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';

class GoogleButton extends Component {
	render() {
		return (
			<GoogleLogin
				clientId="97035292419-vtd1vjmj9rbg3s1qlprnjrquecmkn0m8.apps.googleusercontent.com"
				buttonText="Login"
				onSuccess={responseGoogle}
				onFailure={responseGoogle}
				cookiePolicy={'single_host_origin'}
				redirectUri='http://localhost:3000/reservations'
				uxMode='redirect'
				hostedDomain='https://apis.google.com/js/platform.js'
			/>
		)
	}
}
const responseGoogle = (response) => {
	console.log(response);
};
export default GoogleButton;