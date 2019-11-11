import React, { Component } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Modal, { closeStyle } from 'simple-react-modal'
import moment from 'moment';
import axios from 'axios';

import FormComponent from '../Form/Form';
import "react-big-calendar/lib/css/react-big-calendar.css";

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
				owner: ''
			}
		};
	}



	show() {
		this.setState({show: true})
	}

	close() {
		this.setState({show: false})
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


	componentDidMount() {
		axios.get('http://localhost:8000/slots/')
			.then(res => {
				console.log(res.data);
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
		return (
			<div className="App">
				<Modal
					containerClassName="test"
					closeOnOuterClick={true}
					show={this.state.show}
					onClose={this.close.bind(this)}>

					<a style={closeStyle} onClick={this.close.bind(this)}>X</a>
					<div>
						<FormComponent
							start={moment(this.state.start).format()}
							end={moment(this.state.end).format()}
							action={this.close }
						/>
					</div>
				</Modal>

				<Calendar
					selectable
					localizer={localizer}
					defaultDate={new Date()}
					defaultView="month"
					events={this.state.events}
					style={{ height: "100vh" }}
					onSelectEvent={event => alert(event.title)}
					onSelectSlot={this.handleSelect}
					components={{ event: this.eventDisplay }}
				/>
			</div>
		);
	}
}

export default Scheduler;
