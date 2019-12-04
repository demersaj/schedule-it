import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import axios from 'axios';
import Aux from '../Aux';

const baseURL = 'https://cs467-backend-nc.appspot.com/scheduleusers/';

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
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + user.token
			},
			method: 'post',
			url : baseURL,

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
		console.log(res);
		if (type === 'google' && res.w3.U3) {
			user = {
				firstName: res.w3.ofa,
				lastName: res.w3.wea,
				onid: res.w3.U3.slice(0, res.w3.U3.length - 16),
				token: res.Zi.id_token,
				signedIn: true,
				id: ''
			};
		}

		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + user.token
			},
			method: 'get',
			url: baseURL
		}).then(res => {
			if (res) {  // user exists
				console.log(res);
				user.id = res.data[0].id;
				sessionStorage.setItem('userData', JSON.stringify(user));
				this.setState({redirect: true});
			} else { // sign up user
				//this.signupUser(user);
			}
		})

	};

	render() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		if (this.state.redirect && userData) {
			if (userData.signedIn === true) {
				return (<Redirect to={'/slots'} />)
			}
		}

		const responseGoogle = (res) => {
			this.login(res, 'google');
		};

		const logoutGoogle = () => {
			console.log('user logged out');
			sessionStorage.clear();
			(window.location.reload(true));
		};

		if (!userData || userData.signedIn === false) {
		return (
			<Aux>
				<p>Please login to continue.</p>
				<GoogleLogin
					clientId='636078506451-63230cnsvcb94hphlfnisme1onj2bbba.apps.googleusercontent.com'
					buttonText='Login'
					onSuccess={responseGoogle}
					onFailure={responseGoogle}
					cookiePolicy='single_host_origin'
					// redirectUri='http://localhost:3000/reservations'
					// uxMode='script'
					// hostedDomain='https://apis.google.com/js/platform.js'
				/>
			</Aux>
		)}
		else if (userData.signedIn === true) {
			return (
				<GoogleLogout
					clientId='636078506451-63230cnsvcb94hphlfnisme1onj2bbba.apps.googleusercontent.com'
					onLogoutSuccess={logoutGoogle}
					onFailure={error => console.log(error)}
					buttonText='Logout'
				/>
			)
		}

	}
}

export default Auth;