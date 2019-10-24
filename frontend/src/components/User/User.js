import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import axios from 'axios';

class User extends Component {
	constructor(props) {
		super(props);
		this.state = {
			onid: '',
			first_name: '',
			last_name: '',
			phone_number: '',
			creator_privilege: false
		}
	}
	componentDidMount() {
		this.refreshList();
	}

	refreshList = () => {
		axios.get('/api/students/')
			.then(res => this.setState({ studentList: res.data }))
			.catch(err => console.log(err));
	};

	render() {
		return (
		)
	}
}

export default User