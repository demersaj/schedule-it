import React, { Component } from "react";
import { Calendar, momentLocalizer } from 'react-big-calendar';
import Views from 'react-big-calendar';
import moment from "moment";

import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);
const propTypes = {};

class Scheduler extends Component {
	state = {
		events: [
			{
				start: new Date(),
				end: new Date(moment().add(1, "days")),
				title: "Some title"
			}
		]
	};

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
