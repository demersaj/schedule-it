import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Auth from '../../containers/Auth/Auth';
import Aux from '../../containers/Aux';
import GoogleLogin from 'react-google-login';


class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			name: '',
			redirect: false
		};
	}

	componentDidMount() {
		let data = JSON.parse(sessionStorage.getItem('userData'));
		console.log(data);
		this.setState({ name: data.firstName + ' ' + data.lastName })
	}

	render () {
		return (
			<Aux>
				<div>
					<h4>Welcome to Schedule-It, {this.state.name}.</h4>
					<p>Please login to continue.</p>
				</div>
				<div>
					<Auth />
				</div>
			</Aux>
		)
	}
}

export default Home;