import React, { Component } from 'react';
import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="App-header">
        <h1 onClick={() => {this.navTo('')}}>UD Titrivia</h1>
        <h2 onClick={() => {this.navTo('')}}>See All Questions</h2>
        <h2 onClick={() => {this.navTo('/add')}}>Add More Questions</h2>
        <h2 onClick={() => {this.navTo('/play')}}>Play</h2>
      </div>
    );
  }
}

export default Header;
