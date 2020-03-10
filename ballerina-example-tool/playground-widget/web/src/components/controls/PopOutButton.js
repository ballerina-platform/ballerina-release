import React from 'react';
import './PopOutButton.scss';
import btnPopOut from './btn-popout.svg';

class PopOutButton extends React.Component {

    render() {
        return (
            <div
                className="btn-popout"
            >
                <img src={btnPopOut} />
                <span>pop-out</span>
            </div>
        );
    }
}

export default PopOutButton;