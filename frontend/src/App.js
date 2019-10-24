import React from 'react';
import './App.css';
import Calendar from './components/Calendar/Calendar';

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
