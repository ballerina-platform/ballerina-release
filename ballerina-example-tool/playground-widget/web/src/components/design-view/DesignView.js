import React from 'react';
import PropTypes from 'prop-types';
import Loader from 'semantic-ui-react/dist/es/elements/Loader/Loader';
import Dimmer from 'semantic-ui-react/dist/es/modules/Dimmer/Dimmer';
import { Scrollbars } from 'react-custom-scrollbars';
import './DesignView.scss';

/**
 * DesignView component
 */
class DesignView extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.state = {
          DiagramView: undefined
        }
    }

    componentDidMount() {
        import(/* webpackChunkName: "interaction.diagram" */ './DiagramView').then(diagram => {
            this.setState({ DiagramView: diagram.default });
        });
    }

    /**
     * @inheritDoc
     */
    render() {
        const { DiagramView } = this.state;
        const diagramSize = { width: 476, height: 285 };
        return (
            <div
                className='design-view'
                ref={(ref) => {
                    this.container = ref;
                }}
                style={{ ...this.props.size }}
            >
                {!DiagramView &&
                    <Dimmer active inverted>
                        <Loader inverted />
                    </Dimmer>
                }
                {DiagramView &&
                    <Scrollbars style={{ ...diagramSize }}>
                        <DiagramView content={this.props.content} size={diagramSize} />
                    </Scrollbars>
                }
            </div>
        );
    }
}

DesignView.propTypes = {
    content: PropTypes.string,
};

export default DesignView;
