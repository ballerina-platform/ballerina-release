import React from 'react';
import PropTypes from 'prop-types';
import './CURLEditor.css';
import { getMonospaceFontFamily } from '../../client-utils';

/**
 * CURL editor
 */
class Console extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.state = {
          content: this.props.sample.curl
        }
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            content: nextProps.sample.curl
        });
    }

    /**
     * @inheritDoc
     */
    render() {
        const { sample } = this.props;
        const { content } = this.state;
        return (
            <div className='curl-editor'>
                <div className="curl-string">
                        <input
                            type="text"
                            value={content}
                            onChange={(evt) => {
                                sample.curl = evt.target.value;
                                this.setState({
                                    content: evt.target.value
                                });
                            }}
                            spellcheck="false"
                            style={{ fontFamily: getMonospaceFontFamily() }}
                        />
                </div>
            </div>
        );
    }
}

Console.propTypes = {
    onChange: PropTypes.func,
    sample: PropTypes.shape({
        name: PropTypes.string.isRequired,
        source: PropTypes.string.isRequired,
        curl: PropTypes.string,
    }),
};

Console.defaultProps = {
    onChange: () => {},
    sample: {}
};

export default Console;
