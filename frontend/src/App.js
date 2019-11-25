import React from 'react';
import './App.css';
import {
	Route,
	NavLink,
	BrowserRouter
} from 'react-router-dom';

import Calendar from './components/Calendar/Calendar';
import User from './components/User/User';
import Home from './components/Home/Home';

function App() {
  return (
  	<BrowserRouter>
	    <div>
			<nav className='navbar navbar-expand-lg navbar-light bg-light'>
				<ul className='navbar-nav mr-auto'>
					<li><NavLink to='/' className='nav-link'>Home</NavLink></li>
					<li><NavLink to='/calendar' className='nav-link'>Calendar</NavLink></li>
				</ul>
			</nav>
		    <div className='content'>
			    <Route exact path='/' component={Home}/>
			    <Route exact path='/calendar' component={Calendar}/>
		    </div>
	    </div>
    </BrowserRouter>
  );
}

export default App;
