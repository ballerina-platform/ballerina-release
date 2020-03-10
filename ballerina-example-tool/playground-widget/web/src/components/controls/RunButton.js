import React from 'react';
import PropTypes from 'prop-types';
import Button from 'semantic-ui-react/dist/es/elements/Button/Button';
import Console from '../console/Console';
import { fetchLauncherURL } from '../../utils';
import RunSession from '../../run-session';
import './RunButton.scss';

const MSG_CODES = {
    ERROR: "ERROR",
    BUILD_STARTED: "BUILD_STARTED",
    CURL_EXEC_STARTED: "CURL_EXEC_STARTED",
    CURL_EXEC_STOPPED: "CURL_EXEC_STOPPED",
    BUILD_ERROR: "BUILD_ERROR",
    BUILD_STOPPED: "BUILD_STOPPED",
    BUILD_STOPPED_WITH_ERRORS: "BUILD_STOPPED_WITH_ERRORS",
    EXECUTION_STARTED: "EXECUTION_STARTED",
    EXECUTION_STOPPED: "EXECUTION_STOPPED",
    PROGRAM_TERMINATED: "PROGRAM_TERMINATED",
    DEP_SERVICE_EXECUTION_STARTED: "DEP_SERVICE_EXECUTION_STARTED",
    DEP_SERVICE_EXECUTION_ERROR: "DEP_SERVICE_EXECUTION_ERROR",
    DEP_SERVICE_EXECUTION_STOPPED: "DEP_SERVICE_EXECUTION_STOPPED",
    RUN_ABORTED: "RUN_ABORTED",
};

const MSG_TYPES = {
    DATA_MSG: "DATA_MSG"
};
class RunButton extends React.Component {
    constructor(...args) {
        super(...args);
        this.state = {
            runInProgress: false,
            waitingOnRemoteAck: false,
        }
        this.onStop = this.onStop.bind(this);
        this.onRun = this.onRun.bind(this);
        this.runSession = undefined;
    }

    clearConsole() {
        const { consoleRef } = this.props;
        if (consoleRef) {
            consoleRef.clear();
        }
    }

    appendToConsole(messsage, type = 'INFO') {
        if (messsage instanceof Error) {
            messsage = 'Error: ' + messsage.message;
        }
        const { consoleRef } = this.props;
        if (consoleRef) {
            consoleRef.append(messsage);
        }
    }

    setConsoleText(messsage, type = 'INFO') {
        const { consoleRef } = this.props;
        if (consoleRef) {
            consoleRef.clearAndPrint(messsage);
        }
    }

    resetSession(clearConsole = false) {
        if (clearConsole) {
            this.clearConsole();
        }
        this.setState({
            runInProgress: false,
            waitingOnRemoteAck: false
        });
        this.runSession = undefined;
    }

    onRun() {
        this.setState({
            waitingOnRemoteAck: true
        });
        const { sample } = this.props;
        if (sample && sample.content) {
            this.clearConsole();
            this.appendToConsole('waiting on remote server...');
            fetchLauncherURL(sample)
                .then(({ launcherUrl, cacheId }) => {
                    try {
                        this.runSession = new RunSession(launcherUrl);
                        this.runSession.init({ 
                            onMessage: ({ type, message, code }) => {
                                switch (code) {
                                    case MSG_CODES.DEP_SERVICE_EXECUTION_STARTED:
                                    case MSG_CODES.DEP_SERVICE_EXECUTION_ERROR:
                                    case MSG_CODES.DEP_SERVICE_EXECUTION_STOPPED:
                                    case MSG_CODES.EXECUTION_STARTED:
                                            break;
                                    case MSG_CODES.EXECUTION_STOPPED:
                                    case MSG_CODES.PROGRAM_TERMINATED:
                                            const msg = sample && sample.main 
                                                        ? 'you can edit the code and try again'
                                                        : 'you can edit the code or curl and try again';
                                            this.appendToConsole(msg);
                                            this.runSession.close();
                                            this.resetSession();
                                            break;
                                    case MSG_CODES.ERROR:
                                            if (type === MSG_TYPES.DATA_MSG) {
                                                break;
                                            }
                                    case MSG_CODES.BUILD_ERROR:
                                    case MSG_CODES.RUN_ABORTED:
                                            this.appendToConsole(message);
                                            this.runSession.close();
                                            this.resetSession();
                                            break;
                                    case MSG_CODES.BUILD_STARTED:
                                            this.appendToConsole(message)
                                            this.setState({
                                                runInProgress: true,
                                                waitingOnRemoteAck: false
                                            });
                                            break;
                                    default: this.appendToConsole(message);
                                }
                            }, 
                            onOpen: () => {
                                try {
                                    this.runSession.run(sample, cacheId);
                                    this.props.onRun(sample);
                                } catch (err) {
                                    this.appendToConsole(err);
                                    this.runSession.close();
                                    this.resetSession();
                                }
                            },
                            onClose: (evt) => {
                                if (evt.code !== 1000 && evt.code !== 1006) { 
                                    const err = 'remote server connection was closed due to an error: code:' + evt.code;
                                    this.appendToConsole(err);
                                }
                            }, 
                            onError: (err) => {
                                const msg = 'error occurred with remote server connection';
                                this.appendToConsole(msg);
                                this.resetSession();
                            },
                        });
                    } catch (err) {
                        this.appendToConsole(err);
                        this.resetSession();
                    }
                })
                .catch((err) => {
                    this.appendToConsole(err);
                    this.resetSession();
                })
        }
    }

    onStop() {
        this.setState({
            waitingOnRemoteAck: true
        })
        try {
            if (this.runSession) {
                this.runSession.stop();
            }
        } catch (err) {
            this.appendToConsole(err);
        }
        this.props.onStop(this.props.sample);
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.sample !== nextProps.sample
            && this.state.runInProgress) {
            this.onStop();
        }
    }

    render() {
        const { sample, disabled } = this.props;
        const { runInProgress } = this.state;
        return (
            <Button
                className="run-button"
                onClick={runInProgress ? this.onStop : this.onRun}
                fluid
                basic
                disabled={disabled || !(sample && sample.content && sample.content.trim()) || this.state.waitingOnRemoteAck} >
                <span>{ runInProgress ? 'Stop' : 'Run' }</span>
            </Button>
        );
    }
}

RunButton.propTypes = {
    sample: PropTypes.shape({
        name: PropTypes.string.isRequired,
        fileName: PropTypes.string.isRequired
    }),
    consoleRef: PropTypes.instanceOf(Console),
    disabled: PropTypes.bool,
    onStop: PropTypes.func,
    onRun: PropTypes.func,
    onError: PropTypes.func
};

RunButton.defaultProps = {
    sample: undefined,
    consoleRef: undefined,
    disabled: false,
    onStop: () => {},
    onRun: () => {},
    onError: () => {},
};
  
export default RunButton;