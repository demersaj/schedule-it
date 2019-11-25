import React, { Component } from 'react';
import Auth from '../../containers/Auth/Auth';
import Aux from '../../containers/Aux';


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
		if (data && data.signedIn === true) {
			this.setState({ name: ', ' + data.firstName + ' ' + data.lastName})
		}
	}

	render () {
		return (
			<Aux>
				<div>
					<h4>Welcome to Schedule-It{this.state.name}.</h4>
				</div>
				<div>
					<Auth />
				</div>
			</Aux>
		)
	}
}

export default Home;