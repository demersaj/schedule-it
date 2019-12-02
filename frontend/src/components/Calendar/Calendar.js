import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

import FormComponent from '../Form/Form';
import "react-big-calendar/lib/css/react-big-calendar.css";

const baseURL = 'https://cs467-backend-nc.appspot.com/slots/scheduleuser/';
const localizer = momentLocalizer(moment);

class Scheduler extends Component {
	constructor(props) {
		super(props);

		this.close = this.close.bind(this);

		this.state = {
			events: [],
			event: {
				id: '',
				start: '',
				end: '',
				title: '',
				location: '',
				num_people: '',
				owner: '',
			},
			people: [],
			reservation: '',
		};
	}

	show() {
		this.setState({show: true})
	}

	close() {
		this.setState({show: false})
	}

	showSlot() {
		this.setState({showSlot: true})
	}

	closeSlot() {
		this.setState({showSlot: false})
	}

	handleSelect = ({ start, end }) => {
		this.setState({
			show: true,
			start: start,
			end: end
		})
	};

	handleEventSelect = event => {
		this.setState({
			showSlot: true,
			event: event
		});
	};

	handleDelete = () => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'delete',
			url: baseURL + this.state.reservation
		})
	};

	eventDisplay = ({ event	}) => {
		return (
			<span>
				{event.title}
				<p>Location: {event.location}</p>
				<p>Num People: {event.num_people}</p>
			</span>
		)
	};

	// TODO: finish display
	// get list of users in a reservation
	getReservation = () => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'get',
			url: 'https://cs467-backend-nc.appspot.com/reservations/' + this.state.reservation
		}).then(res => console.log(res))
			.then(res => {
				this.setState({
					reservation: res.data.id
				})
			})
	};


	componentDidMount() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'get',
			url: baseURL
		}).then(res => {
			let appointments = res.data;

			for (let i = 0; i < appointments.length; i++) {
				appointments[i].start = moment.utc(appointments[i].start).toDate();
				appointments[i].end = moment.utc(appointments[i].end).toDate();
			}
			this.setState({
				events: appointments
			})
		}).catch(err => {
			console.log(err);
		})
	}

	render() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		if (!userData) {
			return (<Redirect to={'/'} />)
		} else if (userData.signedIn === false) {
			return (<Redirect to={'/'}/>)
		}


		return (
			<div className="App">
				<h3>Select or create a reservation</h3>
				<Modal
					closeOnOuterClick={true}
					show={this.state.show}
					onClose={this.close.bind(this)}
				>
					<a style={closeStyle} onClick={this.close.bind(this)}>X</a>
					<div>
						<FormComponent
							start={moment(this.state.start).format()}
							end={moment(this.state.end).format()}
							action={this.close}
						/>
					</div>
				</Modal>

				<Modal
					closeOnOuterClick={true}
					show={this.state.showSlot}
					onClose={this.closeSlot.bind(this)}
					>
					<span>
						<h4>{this.state.event.title}</h4>
						<p>Start: {moment(this.state.start).format().substring(0, 16)}</p>
						<p>End: {moment(this.state.end).format().substring(0, 16)}</p>
						<p>Location: {this.state.event.location}</p>
						<p>Num people: {this.state.event.num_people}</p>
						<p>Attendees: {this.getReservation}</p>
						<p>Add attendee:
							<input type='text'
	                            name='attendee'
	                            placeholder={'Attendee\'s ONID'}
	                            value={this.state.location}
	                            onChange={e => this.setState( {location: e.target.value})}
							/>
						</p>
						<button onClick={this.handleSubmit}>Submit</button>
						<button onClick={this.handleDelete}>Delete</button>
					</span>
				</Modal>

				<Calendar
					selectable
					popup
					localizer={localizer}
					defaultDate={new Date()}
					defaultView="month"
					events={this.state.events}
					style={{ height: "100vh" }}
					onSelectEvent={this.handleEventSelect}
					onSelectSlot={this.handleSelect}
					components={{ event: this.eventDisplay }}
				/>
			</div>
		);
	}
}

export default Scheduler;
