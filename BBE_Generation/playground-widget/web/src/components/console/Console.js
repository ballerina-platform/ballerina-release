import React from 'react';
import PropTypes from 'prop-types';
import { Scrollbars } from 'react-custom-scrollbars';
import { getMonospaceFontFamily } from '../../client-utils';
import './Console.css';


/**
 * Console component
 */
class Console extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.state = {
            messages: []
        };
        this.messageCache = [];
        this.appendDebounced = () => {
            this.setState({ messages: this.messageCache }); 
            setTimeout(() => {
                if (this.scrollBar) {
                    this.scrollBar.scrollToBottom();
                }
            }, 200);
        };
        this.onTryItClick = this.onTryItClick.bind(this);
        this.scrollBar = undefined;
    }

    /**
     * set
     */
    clearAndPrint(msg) {
        this.messageCache = [];
        this.messageCache.push(msg)
        this.appendDebounced();
    }

    /**
     * append to console
     */
    append(msg) {
        this.messageCache.push(msg);
        this.appendDebounced();
    }

    /**
     * clear console
     */
    clear() {
        this.messageCache = [];
        this.setState({
            messages: [],
        });
    }

    onTryItClick() {
        this.props.onTryItClick();
    }

    /**
     * @inheritDoc
     */
    render() {
        const { curlVisible, sample: { noOfCurlExecutions = 0, main = false } } = this.props;
        const consoleAreaHeight = curlVisible ? 106 : 132;
        return (
            <div 
                className='console-area'
                style={{
                    fontFamily: getMonospaceFontFamily()
                }}
            >
                <Scrollbars 
                    style={{ width: 460, height: consoleAreaHeight }}
                    ref={(scrollBar) => {
                        this.scrollBar = scrollBar;
                    }}
                >
                    {this.state.messages.map((msg, index, msgs) => {
                        if (!msg || msg.startsWith('BVM-OUTPUT:/ballerina/runtime/bin/ballerina: line ')) {
                            return (<span/>);
                        }
                        if (msg === 'Compiling source' || msg === 'Generating executable') {
                            return (<span/>);
                        }
                        if ((index - 1) >= 0 && (msgs[index - 1] === 'Compiling source' || msgs[index - 1] === 'Generating executable')) {
                            return (<span/>);
                        }
                        if (msg === 'building...' && msgs.length > (index + 5)
                                && msgs[index + 5].startsWith('build completed in')) {
                            return (<span/>);
                        }
                        if (msg === 'building...' && msgs.length > (index + 1)
                                && msgs[index + 1].startsWith('build completed in') && main) {
                            return (<span/>);
                        }
                        if (msg.startsWith('build completed in') && !main) {
                            return (<div className="console-line">{'building...   ' 
                            + msg.replace('build completed in', 'deployed to kubernetes in')}</div>)
                        }
                        if (msg.startsWith('executing curl...') && noOfCurlExecutions > 0) {
                            return (<div className="console-line">{`executing curl ${noOfCurlExecutions} times...`}</div>)
                        }
                        if (msg.startsWith('executing curl completed in')) {
                            return (
                                <div className="console-line">{msg.replace('executing', '')}</div>
                            );
                        }
                        if (msg.includes('CircuitBreaker failure threshold exceeded')) {
                            return (<div className="console-line bvm-output">{'Circuit tripped : CLOSE -> OPEN'}</div>)
                        }
                        if (msg.includes('CircuitBreaker reset timeout reached')) {
                            return (<div className="console-line bvm-output">{'Circuit open timeout reached : OPEN -> HALF-OPEN'}</div>)
                        }
                        if (msg.includes('CircuitBreaker trial run  was successful')) {
                            return (<div className="console-line bvm-output">{'Circuit closed : HALF-OPEN -> CLOSE'}</div>)
                        }
                        if (msg.includes('INFO [ballerina.net.http] - ')) {
                            return (<div className="console-line bvm-output">{msg.split('INFO [ballerina.net.http] -')[1]}</div>)
                        }
                        if (msg.startsWith('CURL-OUTPUT:')) {
                            return (<div className="console-line curl-output">{msg.replace('CURL-OUTPUT:', '')}</div>)
                        }
                        if (msg.startsWith('BVM-OUTPUT:')) {
                            return (<div className="console-line bvm-output">{msg.replace('BVM-OUTPUT:', '')}</div>)
                        }
                        return (<div className="console-line">{msg}</div>)
                    })}
                </Scrollbars>
            </div>
        );
    }
}

Console.propTypes = {
    sample: PropTypes.shape({
        noOfCurlExecutions: PropTypes.number,
        main: PropTypes.bool,
    }).isRequired,
    onTryItClick: PropTypes.func,
    curlVisible: PropTypes.bool,
};
export default Console;
