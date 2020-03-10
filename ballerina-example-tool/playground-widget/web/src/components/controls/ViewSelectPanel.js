import React from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import './ViewSelectPanel.scss';
import viewSourceBtnIcon from './btn-source.svg';
import viewComposerBtnIcon from './btn-composer.svg';
import viewBinaryBtnIcon from './btn-binary.svg';

export const VIEWS = {
    SOURCE: 'SOURCE',
    COMPOSER: 'COMPOSER',
    BINARY: 'BINARY',
};

class ViewSelectPanel extends React.Component {
    render() {
        const { selectedView, onViewSwitch } = this.props;
        return (
            <div
                className="view-select-panel"
            >
                <div 
                    className={cn('btn', 'source-view-btn', { 'active': selectedView === VIEWS.SOURCE })}
                    onClick={() => {
                        if (selectedView !== VIEWS.SOURCE) {
                            onViewSwitch(VIEWS.SOURCE);
                        }
                    }}
                >
                    <img className='source-view-panel' src={viewSourceBtnIcon} />
                </div>
                <div 
                    className={cn('btn', 'composer-view-btn', { 'active': selectedView === VIEWS.COMPOSER })}
                    onClick={() => {
                        if (selectedView !== VIEWS.COMPOSER) {
                            onViewSwitch(VIEWS.COMPOSER);
                        }
                    }}
                >
                    <img className='composer-view-panel' src={viewComposerBtnIcon} />
                </div>
                <div  
                    className={cn('btn', 'binary-view-btn', { 'active': selectedView === VIEWS.BINARY })}
                    onClick={() => {
                        if (selectedView !== VIEWS.BINARY) {
                            onViewSwitch(VIEWS.BINARY);
                        }
                    }}
                >
                    <img className='binary-view-panel' src={viewBinaryBtnIcon} />
                </div>
            </div>
        );
    }
}

ViewSelectPanel.propTypes = {
    selectedView: PropTypes.oneOf([VIEWS.SOURCE, VIEWS.COMPOSER, VIEWS.BINARY]),
    onViewSwitch: PropTypes.func,
};

ViewSelectPanel.defaultProps = {
    selectedView: VIEWS.SOURCE,
    onViewSwitch: () => {
    },
};

export default ViewSelectPanel;