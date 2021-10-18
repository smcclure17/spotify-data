import React from 'react';
import logo from './logo.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          This is the default TS app
        </p>
        <a
          className="google"
          href="https://google.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          google
        </a>
      </header>
    </div>
  );
}

export default App;
