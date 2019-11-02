import React, { Component } from "react";
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from "moment";
import axios from 'axios';

import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);
const propTypes = {};

class Scheduler extends Component {
	constructor(props) {
		super(props);

		this.state = {
			events: [],
		}
	}

	handleSelect = ({ start, end }) => {
		const title = window.prompt('New Event name')
		if (title)
			this.setState({
				events: [
					...this.state.events,
					{
						start,
						end,
						title,
					},
				],
			})
	};

	componentDidMount() {
		axios.get('http://localhost:8000/api/slots/')
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
				<Calendar
					selectable
					localizer={localizer}
					defaultDate={new Date()}
					defaultView="month"
					events={this.state.events}
					style={{ height: "100vh" }}
					onSelectEvent={event => alert(event.title)}
					onSelectSlot={this.handleSelect}
				/>
			</div>
		);
	}
}

export default Scheduler;
