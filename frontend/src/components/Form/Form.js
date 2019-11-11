import React, { Component } from 'react';
import Aux from '../../containers/Aux';
import axios from 'axios';

class FormComponent extends Component {
	constructor( props ) {
		super(props);
		this.state = {
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
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit = async (e) => {
		//e.preventDefault();

		axios({
			"headers": {
				"Content-Type": "application/json"
			},
			method: 'post',
			url: 'http://localhost:8000/api/slots/',

			data: {
				title: this.state.title,
				start: this.state.start === '' ? this.props.start: this.state.start,
				end: this.state.end === '' ? this.props.end: this.state.end,
				location: this.state.location,
				num_people: this.state.num_people,
				owner: this.state.owner
				}
		}).catch(err => {
			console.log(err);
		})

	};

	render() {
		return (
			<Aux>
				<h4>Create New Slot</h4>
				<form>
					<input type='datetime-local'
					       name='start'
					       placeholder={'Start Time'}
					       value={this.state.start}
					       defaultValue={this.props.start.substring(0, 16)}
					       onChange={e => this.setState( {start: e.target.value})}
					/>

					<input type='datetime-local'
					       name='end'
					       placeholder={'End Time'}
					       value={this.state.end}
					       defaultValue={this.props.end.substring(0, 16)}
					       onChange={e => this.setState( {end: e.target.value})}
					/>

					<input type='text'
					       name='title'
					       placeholder={'Title'}
					       value={this.state.title}
					       onChange={e => this.setState( {title: e.target.value})}
					/>

					<input type='text'
					       name='location'
					       placeholder={'Location'}
					       value={this.state.location}
					       onChange={e => this.setState( {location: e.target.value})}
					/>

					<input type='number'
					       name='num_people'
					       placeholder={'Number of people'}
					       value={this.state.num_people}
					       onChange={e => this.setState( {num_people: e.target.value})}
					/>

					<input type='number'
					       name='owner'
					       placeholder={'Owner'}
					       value={this.state.owner}
					       onChange={e => this.setState( {owner: e.target.value})}
					/>
					<button
						onClick={this.handleSubmit}
						//onClick={this.props.action}
					>Submit</button>
				</form>
			</Aux>
		)
	}
}

export default FormComponent;