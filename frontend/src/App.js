import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Calendar from './components/Calendar/Calendar';
//import User from './components/User/User';

function App() {
  return (
    <div className="App">
      <header className="App-header">
	      <h1>Schedule-It</h1>
      </header>
        <p>
         <Calendar/>
        </p>
    </div>
  );
}

export default App;
