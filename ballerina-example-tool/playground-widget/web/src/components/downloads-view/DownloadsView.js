import React from 'react';
import './DownloadsView.css';

/**
 * DownloadsView component
 */
class DownloadsView extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.scrollBar = undefined;
    }

    /**
     * @inheritDoc
     */
    render() {
        return (
            <div className='downloads-area'>
                <img src="images/deployment.svg" />
            </div>
        );
    }
}
export default DownloadsView;
