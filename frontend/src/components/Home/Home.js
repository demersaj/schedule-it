import React, { Component } from 'react';
import GoogleButton from '../../containers/Auth/Auth';
import Aux from '../../containers/Aux';

class Home extends Component {
	render () {
		return (
			<Aux>
				<div>
					<h4>Welcome to Schedule-It.</h4>
					<p>Please login to continue.</p>
				</div>
				<div>
					<GoogleButton />
				</div>
			</Aux>
		)
	}
}

export default Home;