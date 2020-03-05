import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import Loader from 'semantic-ui-react/dist/es/elements/Loader/Loader';
import Dimmer from 'semantic-ui-react/dist/es/modules/Dimmer/Dimmer';
import { PARSER_API_URL } from '../../utils';
import { Diagram, DiagramMode } from '@ballerina/diagram'

import '@ballerina/font/build/font/font-ballerina.css';

/**
 * Invoke parser service for the given content
 * and returns a promise with parsed json
 * @param {string} content
 */
function parseContent(content) {
    const payload = {
        content,
    };
    return axios.post(PARSER_API_URL, payload,
            { 
                headers: {
                    'content-type': 'application/json; charset=utf-8',
                } 
            })
            .then((response) => {
                return response.data;
            });
}


/**
 * DiagramView component
 */
class DiagramView extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.state = {
          model: undefined,
        }
        this.container = undefined;
    }

    /**
     * @override
     * @memberof Diagram
     */
    getChildContext() {
        return {
            getDiagramContainer: () => {
                return this.container;
            },
            getOverlayContainer: () => {
                return this.container;
            }
        };
    }

    componentDidMount() {
        parseContent(this.props.content)
            .then(({ model }) => {
                this.setState({ model });
            })
    }

    /**
     * @inheritDoc
     */
    render() {
        const { model } = this.state;
        const { width, height } = this.props.size;
        return (
        <div className="interaction-diagram ballerina-editor" style={{ ...this.props.size }} >
            {!model &&
                    <Dimmer active inverted>
                        <Loader inverted />
                    </Dimmer>
                }
            {model &&
                <Diagram mode='action'
                    ast={model} 
                    width={width}
                    height={height}
                    zoom={1}
                    mode={DiagramMode.ACTION}
                />
            }
        </div>
        );
    }
}

DiagramView.propTypes = {
    content: PropTypes.string,
    size: PropTypes.shape({
        width: PropTypes.number.isRequired,
        height: PropTypes.number.isRequired
    }).isRequired
};


DiagramView.childContextTypes = {
    getDiagramContainer: PropTypes.func.isRequired,
    getOverlayContainer: PropTypes.func.isRequired
};

export default DiagramView;
