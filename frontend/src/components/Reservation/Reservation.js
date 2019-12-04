import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Aux from '../../containers/Aux';

import FormComponent from '../Form/Form';
import "react-big-calendar/lib/css/react-big-calendar.css";

const baseURL = 'https://cs467-backend-nc.appspot.com/reservations/slots/scheduleuser/';
const deleteURL = 'https://cs467-backend-nc.appspot.com/reservations/';
const localizer = momentLocalizer(moment);

class Reservation extends Component {
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
			attendee: '',
			attendees: []
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

	// TODO: Fix delete function
	handleDelete = () => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'delete',
			url: deleteURL + this.state.event.id + '/'
		}).then(this.closeSlot.bind(this));
	};

	eventDisplay = ({ event }) => {
		return (
			<span>
				{event.title}<br />
				Location: {event.location}<br />
				Attendees: {this.state.attendees}
			</span>
		)
	};

	eventStyleGetter = (event, start, end, isSelected) => {
		let backgroundColor = '#00e673';
		let style = {
			backgroundColor: backgroundColor,
			opacity: 0.8,
			color: 'black',
			border: '0px',
			display: 'block'
		};
		if (isSelected) {
			style = {
				backgroundColor: '#4dffa6',
				opacity: 0.8,
				color: 'black',
				borderWidth: '1',
				borderColor: '#' + event.hexColor,
				display: 'block'
			}
		}
		return {
			style: style
		};
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
			let events = res.data;
			console.log(res.data);

			for (let i = 0; i < events.length; i++) {
				events[i].start = moment.utc(events[i].start).toDate();
				events[i].end = moment.utc(events[i].end).toDate();
			}
			this.setState({
				events: events
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
			<div className='App'>
				<h3>Select a reservation to add attendees</h3>
				<Modal
					closeOnOuterClick={true}
					show={this.state.showSlot}
					onClose={this.closeSlot.bind(this)}
				>
					<a style={closeStyle} onClick={this.closeSlot.bind(this)}>X</a>
						<span>
							<h4>{this.state.event.title}</h4>
							<p>Start: {moment(this.state.start).format().substring(0, 16)}</p>
							<p>End: {moment(this.state.end).format().substring(0, 16)}</p>
							<p>Location: {this.state.event.location}</p>
							<p>Num people: {this.state.event.num_people}</p>
							<p>Attendees: </p>
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
					eventPropGetter = {this.eventStyleGetter}
				/>
			</div>
		)
	}
}

export default Reservation;