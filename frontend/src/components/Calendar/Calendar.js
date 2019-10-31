import React, { Component } from 'react';
import './Calendar.css';
import { Inject, ScheduleComponent, Day, Week, WorkWeek, Month } from '@syncfusion/ej2-react-schedule';
import { DataManager, JsonAdaptor } from '@syncfusion/ej2-data';

class Calendar extends Component {
	constructor(props) {
		super(...arguments);

		this.state = {
			events: [],
			event: {
				subject: '',
				date: '',
				'Start Time': '',
				'End Time': '',
				location: '',
				'Max number of people': ''
			},
			isLoading: true
		};
		this.dataManager = new DataManager({
			url: 'http://localhost:8000/api/slots/',    // url of api
			adaptor: new JsonAdaptor(),
			crossDomain: true
		});
	}


	render() {
		return (
			<ScheduleComponent
				currentView={'Month'}
				eventSettings={this.dataManager}
				allowResizing={true}
			>
				<Inject services={ [Day, Week, WorkWeek, Month] } />
			</ScheduleComponent>
		)
	}
}

export default Calendar;