import React from 'react';
import ReactDOM from 'react-dom';
import './index.scss';
import BallerinaWidget from './BallerinaWidget';

export function renderOnDiv(divId) {
    ReactDOM.render(<BallerinaWidget />, document.getElementById(divId));
}