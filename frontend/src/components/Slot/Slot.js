import React, { Component } from 'react';
import Aux from '../../containers/Aux';
import classes from './Slot.css';
import Modal from '../Modal/Modal';
import FormComponent from '../Form/Form';

class Slot extends Component {
	constructor () {
		super();
		this.state = {
			slots: [],
			slot: {
				start: '',
				end: '',
				location: '',
				title: '',
				num_people: '',
				owner: ''
			}
	}
	};

	modalProps = {
		triggerText: 'New Slot'
	};

	modalContent =  (
		<FormComponent />
	);


	render () {
		return (
			<Aux>
				<div>
					<Modal />
				</div>
			</Aux>
		)
	}
}

export default Slot;