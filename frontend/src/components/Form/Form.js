import React, { Component } from 'react';
import Aux from '../../containers/Aux';
import axios from 'axios';

const baseURL = 'https://cs467-backend-nc.appspot.com/slots/';

class FormComponent extends Component {
	constructor( props ) {
		super(props);
		this.state = {
			event: {
				id: '',
				start: '',
				end: '',
				title: '',
				location: '',
				num_people: '',
				owner: ''
			}
		};
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit = async (e) => {
		//e.preventDefault();
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		let id = userData.id;
		axios({
			'headers': {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'post',
			url: baseURL,
			data: {
				title: this.state.title,
				start:this.props.start,
				end: this.props.end,
				location: this.state.location,
				num_people: this.state.num_people,
				owner: id
				}
		}).then(res => this.createReservation(res))
			.then(res => console.log(res))
			.catch(err => {
			console.log(err);
		})
	};

	// creates a reservation using a response from the slot creation
	createReservation = async (res) => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));

		axios({
			"headers": {
				"Content-Type": "application/json"
			},
			method: 'post',
			url: 'https://cs467-backend-nc.appspot.com/scheduleuser/reservations/',

			data: {
				user: userData.id,
				slot: res.data.id
			}
		})
	};



	render() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		let id = userData.id;
		return (
			<Aux>
				<h4>Create New Slot</h4>
				<form>
					<input type='datetime-local'
					       name='start'
					       placeholder={'Start Time'}
					       value={this.state.start}
					       defaultValue={this.props.start.substring(0, 16)}
					       onChange={e => this.setState( {start: e.target.value})}
					/>

					<input type='datetime-local'
					       name='end'
					       placeholder={'End Time'}
					       value={this.state.end}
					       defaultValue={this.props.end.substring(0, 16)}
					       onChange={e => this.setState( {end: e.target.value})}
					/>

					<input type='text'
					       name='title'
					       placeholder={'Title'}
					       value={this.state.title}
					       onChange={e => this.setState( {title: e.target.value})}
					/>

					<input type='text'
					       name='location'
					       placeholder={'Location'}
					       value={this.state.location}
					       onChange={e => this.setState( {location: e.target.value})}
					/>

					<input type='number'
					       name='num_people'
					       placeholder={'Number of people'}
					       value={this.state.num_people}
					       onChange={e => this.setState( {num_people: e.target.value})}
					/>
					< button onClick={this.handleSubmit}>Submit</button>
				</form>
			</Aux>
		)
	}
}

export default FormComponent;