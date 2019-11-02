import React, { Component } from 'react';
import GoogleButton from '../../containers/Auth/Auth';
import divWithClassName from 'react-bootstrap/esm/utils/divWithClassName';

class Home extends Component {

	render () {
		return (
			<div>
				<div>
					<h4>Welcome to Schedule-It.</h4>
					<p>Please login to continue.</p>
				</div>
				<div>
					<GoogleButton />
				</div>
			</div>
		)
	}
}

export default Home;