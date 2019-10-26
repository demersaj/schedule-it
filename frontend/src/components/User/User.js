import React, { Component } from 'react';
import axios from 'axios';
import './User.css';

const instance = axios.create({ baseURL: 'http://localhost:8000' });
const API = 'http://localhost:8000/api/users/';

class User extends Component {
	constructor(props) {
		super(props);

		this.state = {
			users: [],
			user: {
				onid: '',
				'First Name': '',
				'Last Name': '',
				'Phone': '',
				creator_privilege: false
			},
			isLoading: true,
			error: null
		};
	}

	componentDidMount() {
		this.getUsers();
	}

	getUsers = _ => {
		axios.get(API)
			.then(res => this.setState({
				users: res.data,
				isLoading: false
			}))
			.catch(error => this.setState({
				error,
				isLoading: false
			}));
	};

	renderTableHeader() {
		let header = Object.keys(this.state.user).slice(0, 4);
		return header.map(( key, index ) => {
			return <th key={index}>{key}</th>
		})
	}

	renderTableData() {
		return this.state.users.map((user, index) => {
			const { onid, first_name, last_name, phone_number } = user;	// destructure
			return (
				<tr key={onid}>
					<td>{onid}</td>
					<td>{first_name}</td>
					<td>{last_name}</td>
					<td>{phone_number}</td>
				</tr>
			)
		})
	}

	render() {
		return (
			<div>
				<h1 id='title'>Users</h1>
				<table id='users'>
					<tbody>
						<tr>{this.renderTableHeader()}</tr>
						{this.renderTableData()}
					</tbody>
				</table>
			</div>
		)
	}
}

export default User;