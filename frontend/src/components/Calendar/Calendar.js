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
			event: {
				id: null,
				start: '',
				end: '',
				title: '',
				location: '',
				num_people: 0
			}
		}
	}

	handleSelect = async ({ start, end }) => {
		let title, location, num_people;
		title = window.prompt('New Event name');
		if (title) location = window.prompt('New Event location');
		if (location) num_people = window.prompt('Number of people meeting.');
		let postPromise;
		if (num_people) {
			try {
				postPromise = await axios.post('http://localhost:8000/slots/',
					{
						title: title,
						start: start,
						end: end,
						location: location,
						owner: "1",
						num_people: num_people
					}).catch(console.log("caught"));

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
			} catch (err) {
				console.log(start);
				console.log(end);
				console.log("Error Caught");
				console.log(err.response.data);
				alert("Event could not be created\nSee log for details.")
			}
		}
	}


	eventDisplay = ({ event	}) => {
		return (
			<span>
				{event.title}
				<p>Location: {event.location}</p>
			</span>
		)
	}

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
				<Calendar
					selectable
					localizer={localizer}
					defaultDate={new Date()}
					defaultView="month"
					events={this.state.events}
					style={{ height: "100vh" }}
					onSelectEvent={event => alert(event.title)}
					onSelectSlot={this.handleSelect}
					components= {{
						event: this.eventDisplay
					}}
				/>
			</div>
		);
	}
}

export default Scheduler;
