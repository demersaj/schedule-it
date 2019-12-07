import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Moment from 'react-moment';
import AddToCalendar from 'react-add-to-calendar';

import "react-big-calendar/lib/css/react-big-calendar.css";

const baseURL = 'https://cs467-backend-nc.appspot.com/reservations/';
const deleteURL = 'https://cs467-backend-nc.appspot.com/reservation/';
const localizer = momentLocalizer(moment);
const icon = {'calendar-plus-o' : 'left'};

class Reservation extends Component {
	constructor(props) {
		super(props);

		this.close = this.close.bind(this);

		this.state = {
			events: [],
			event: {
				id: '',
				startTime: '',
				endTime: '',
				title: '',
				location: '',
				num_people: '',
				owner: '',
			},
			isLoading: true
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
		event.startTime = event.start;
		event.endTime = event.end;
		this.setState({
			showSlot: true,
			event: event
		});
	};


	handleDelete = () => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		this.setState({isLoading: true});
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'delete',
			url: deleteURL + this.state.event.id + '/'
		}).then(setTimeout(function(){window.location.reload(true)}, 500));
			this.setState({isLoading: false});
	};


	eventDisplay = ({ event }) => {
		return (
			<span>
				{event.title}<br />
				Location: {event.location}<br />
				Attendees: {event.attendees[0]}
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
		if (!userData) {
			return (<Redirect to={'/'} />)
		} else if (userData.signedIn === false) {
			return (<Redirect to={'/'}/>)
		}
		axios({
			headers: {
				'Content-Type': 'application/json',
				Authorization : 'Bearer ' + userData.token
			},
			method: 'get',
			url: baseURL
		}).then(res => {
			let events = res.data;

			for (let i = 0; i < events.length; i++) {
				let attendees = [];
				events[i].start = moment.utc(events[i].slot.start).toDate();
				events[i].end = moment.utc(events[i].slot.end).toDate();
				events[i].title = events[i].slot.title;
				events[i].location = events[i].slot.location;
				events[i].num_people = events[i].slot.num_people;
				if (events[i].slot.owner) {
					attendees.push(events[i].slot.owner.onid)
				} if (events[i].slot.owner.onid !== events[i].owner.onid) {
					attendees.push(', ');
					attendees.push(events[i].owner.onid)
				}
				events[i].attendees = attendees;
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
				<h3>Select a reservation to view attendees</h3>
				<Modal
					closeOnOuterClick={true}
					show={this.state.showSlot}
					onClose={this.closeSlot.bind(this)}
				>
					<a style={closeStyle} onClick={this.closeSlot.bind(this)}>X</a>
					<span>
								<h4>{this.state.event.title}</h4>
								<p>Start: <Moment
									date={this.state.event.start}
									format='LLL'
								/>
								</p>
								<p>End: <Moment
									date={this.state.event.end}
									format='LLL'
								/>
								</p>
								<p>Location: {this.state.event.location}</p>
								<p>Num people: {this.state.event.num_people}</p>
								<p>Attendees: {this.state.event.attendees} </p>
								<button>
									<AddToCalendar
										event={this.state.event}
										buttonLabel='Add to Calendar'
										buttonTemplate={icon}
									/>
								</button> <br/>
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
					endAccessor = {this.state.events.end}
					startAccessor = {this.state.events.start}
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