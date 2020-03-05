import React from 'react';
import ReactDOM from 'react-dom';
import BallerinaWidget from './BallerinaWidget';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<BallerinaWidget />, div);
  ReactDOM.unmountComponentAtNode(div);
});
