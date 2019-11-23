import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

import FormComponent from '../Form/Form';
import "react-big-calendar/lib/css/react-big-calendar.css";

const baseURL = 'http://localhost:8000/slots/';

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

	eventDisplay = ({ event	}) => {
		return (
			<span>
				{event.title}
				<p>Location: {event.location}</p>
				<p>Num People: {event.num_people}</p>
			</span>
		)
	};

	handleEventSelect = event => {
		this.setState({
			showSlot: true,
			event: event
		});
	};


	componentDidMount() {
		let userData = JSON.parse(sessionStorage.getItem('userData'));
		axios.get(baseURL /* + userData.onid */)
			.then(res => {
				let appointments = res.data;

				for (let i = 0; i < appointments.length; i++) {
					appointments[i].start = moment.utc(appointments[i].start).toDate();
					appointments[i].end = moment.utc(appointments[i].end).toDate();
				}
				this.setState({
					events: appointments
				})
			})
			.catch(err => {
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
				<h2>Select or create a slot</h2>
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
							action={this.close }
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
