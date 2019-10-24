import React, { Component } from 'react';
import './Calendar.css';
import { Inject, ScheduleComponent, Day, Week, WorkWeek, Month, Agenda,
	EventSettingsModel } from '@syncfusion/ej2-react-schedule';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

class Calendar extends Component {
	 localData: EventSettingsModel = {
		dataSource: [{
			StartTime: new Date(2019, 9, 17, 14, 30),
			EndTime: new Date(2019, 9, 17, 16, 30),
			Subject: 'Work on CS 467 project'
		}]
	};

	// allows you to load data from remote repository
	 remoteData = new DataManager({
		url: 'https://js.syncfusion.com/demos/ejservices/api/Schedule/LoadData',    // url of api
		adaptor: new WebApiAdaptor,
		crossDomain: true
	});

	 render() {
		return (
			<ScheduleComponent
				currentView={'Month'}
				eventSettings={this.localData}>
				<Inject services={ [Day, Week, WorkWeek, Month, Agenda] } />
			</ScheduleComponent>
		)
	}
}

export default Calendar;