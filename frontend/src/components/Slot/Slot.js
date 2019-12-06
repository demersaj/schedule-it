import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import Moment from 'react-moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

import FormComponent from '../Form/Form';
import Aux from '../../containers/Aux';
import "react-big-calendar/lib/css/react-big-calendar.css";

const baseURL = 'https://cs467-backend-nc.appspot.com/slots/';
const deleteURL = 'https://cs467-backend-nc.appspot.com/slot/';
const userURL = 'https://cs467-backend-nc.appspot.com/scheduleuser/';
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
			people: '',
			reservation: '',
			onid: ''
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
			url: deleteURL + this.state.event.id + '/'
		}).then(this.closeSlot.bind(this))
			// let DELETE request send, then reload page
			.then(setTimeout(function(){window.location.reload(true)}, 500));
	};

	handleAddAttendee = () => {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios({
			"headers": {
				"Content-Type": "application/json",
				Authorization : 'Bearer ' + userData.token
			},
			method: 'get',
			url: userURL + userData.onid + '/',

		}).then(res => {
			axios({
				"headers": {
					"Content-Type": "application/json",
					Authorization : 'Bearer ' + userData.token
				},
				method: 'post',
				url: 'https://cs467-backend-nc.appspot.com/reservations/',
				data: {
					slot: this.state.event.id
				}
			})
		}).then(setTimeout(function(){window.location.reload(true)}, 750))
	};

	eventDisplay = ({ event	}) => {
		return (
			<span>
				{event.title}<br />
				Location: {event.location}<br />
				Num People: {event.num_people}<br />
			</span>
		)
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
		const userData = JSON.parse(sessionStorage.getItem('userData'));
		if (!userData) {
			return (<Redirect to={'/'} />)
		} else if (userData.signedIn === false) {
			return (<Redirect to={'/'}/>)
		}


		return (
			<div className='App'>
				<h3>Select or create a slot</h3>
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
					<a style={closeStyle} onClick={this.closeSlot.bind(this)}>X</a>
					<div>
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
						<p>Owner: {this.state.event.owner.onid}</p>

						{userData.onid === this.state.event.owner.onid ? (
							''
						) : (
							<Aux><button onClick={this.handleAddAttendee}>Join Reservation</button> <br/></Aux>
						)}
						<button onClick={this.handleDelete}>Delete</button>
					</div>
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
