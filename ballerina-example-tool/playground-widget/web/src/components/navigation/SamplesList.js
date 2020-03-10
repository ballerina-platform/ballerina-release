import React from 'react';
import PropTypes from 'prop-types';
import Menu from 'semantic-ui-react/dist/es/collections/Menu/Menu';
import './SamplesList.css';

const LINK_CLS_NAME = 'bpg-sample-link';
class SamplesList extends React.Component {

    constructor(...args) {
        super(...args);
        this.state = {
            selectedIndex: 0
        }
        this.onChange = this.onChange.bind(this);
    }

    onChange(evt, data ) {
        this.setState({
            selectedIndex: data.index
        });
        this.props.onSelect(data.index);
    }

    render() {
        const { samples } = this.props;
        const options = samples.map(({ name }, index) => {
            return {
                text: name,
                key: index,
                value: index
            };
        });
        const middle = (options.length % 2) === 0 ? options.length / 2 : Math.floor(options.length / 2) + 1;
        const leftItems = options.slice(0, middle);
        const rightItems = options.slice(middle);
        
        const activeItem = this.state.selectedIndex;
        return (
        <div className="samples-navigation-list">
            <div style={{ float: "left" }} >
                <Menu text vertical>
                    { leftItems.map(e => {
                        return <Menu.Item 
                            className={LINK_CLS_NAME}
                            name={e.text} 
                            index={e.value}
                            active={activeItem === e.value}
                            onClick={this.onChange}
                        />
                    })}
                </Menu>
            </div>
            <div style={{ float: "left" }} >
                <Menu text vertical>
                    { rightItems.map(e => {
                        return <Menu.Item 
                            className={LINK_CLS_NAME}
                            name={e.text} 
                            index={e.value}
                            active={activeItem === e.value}
                            onClick={this.onChange} 
                        />
                    })}
                </Menu>
            </div>
        </div>
        );
    }
}

SamplesList.propTypes = {
    samples: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        source: PropTypes.string.isRequired
    })),
    onSelect: PropTypes.func,
};

SamplesList.defaultProps = {
    samples: [],
    onSelect: () => {},
};
  
export default SamplesList;