import React from 'react';
import './App.css';
import {
	Route,
	NavLink,
	BrowserRouter
} from 'react-router-dom';

import Slot from './components/Slot/Slot';
import Home from './components/Home/Home';
import Reservation from './components/Reservation/Reservation';

function App() {
  return (
  	<BrowserRouter>
	    <div>
			<nav className='navbar navbar-expand-lg navbar-light bg-light'>
				<ul className='navbar-nav mr-auto'>
					<li><NavLink to='/' className='nav-link'>Home</NavLink></li>
					<li><NavLink to='/slots' className='nav-link'>Slots</NavLink></li>
					<li><NavLink to='/reservations' className='nav-link'>Reservations</NavLink></li>
				</ul>
			</nav>
		    <div className='content'>
			    <Route exact path='/' component={Home}/>
			    <Route exact path='/slots' component={Slot}/>
			    <Route exact path='/reservations' component={Reservation}/>
		    </div>
	    </div>
    </BrowserRouter>
  );
}

export default App;
