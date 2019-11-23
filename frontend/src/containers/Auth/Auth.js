import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import GoogleLogin from 'react-google-login';
import axios from 'axios';

const baseURL = 'http://localhost:8000/users/';

class Auth extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loginError: false,
			redirect: false
		};
		this.login = this.login.bind(this);
	}

	signupUser = (user) => {
		axios({
			'headers': {
				'Content-Type': 'application/json'
			},
			method: 'post',
			'url' : baseURL,

			data: {
				onid: user.onid,
				first_name: user.firstName,
				last_name: user.lastName,
				phone_number: '0',
				creator_privilege: true
			}
		})
	};


	login = (res, type) => {
		let user;
		if (type === 'google' && res.w3.U3) {
			user = {
				firstName: res.w3.ofa,
				lastName: res.w3.wea,
				onid: res.w3.U3.slice(0, res.w3.U3.length - 16),
				token: res.Zi.access_token,
				signedIn: true,
				id: null
			};
		}
		axios.get(baseURL + '?onid=' + user.onid)
			.then(res => {
				if (res) {  // user exists
					user.id = res.id;
					sessionStorage.setItem('userData', JSON.stringify(user));
					this.setState({redirect: true});
				} else { // sign up user
					this.signupUser(user);
				}
			})
	};

	render() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		if (this.state.redirect || userData.signedIn === true) {
			return (<Redirect to={'/reservations'}/>)
		}

		const responseGoogle = (res) => {
			this.login(res, 'google');
		};

		return (
			<GoogleLogin
				clientId="97035292419-vtd1vjmj9rbg3s1qlprnjrquecmkn0m8.apps.googleusercontent.com"
				buttonText="Login"
				onSuccess={responseGoogle}
				onFailure={responseGoogle}
				cookiePolicy={'single_host_origin'}
				// redirectUri='http://localhost:3000/reservations'
				// uxMode='script'
				// hostedDomain='https://apis.google.com/js/platform.js'
			/>
		)
	}
}

export default Auth;