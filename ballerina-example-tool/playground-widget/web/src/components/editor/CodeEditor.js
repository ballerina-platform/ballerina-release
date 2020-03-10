import React from 'react';
import PropTypes from 'prop-types';
import MonacoEditor from 'react-monaco-editor';
import Theme from './theme';
import './CodeEditor.css';
import Grammar from './monaco-grammar';
import BAL_LANG_CONFIG from './monaco-config';
import Loader from 'semantic-ui-react/dist/es/elements/Loader/Loader';
import Dimmer from 'semantic-ui-react/dist/es/modules/Dimmer/Dimmer';
import { getMonospaceFontFamily } from '../../client-utils';

const BAL_LANGUAGE = 'ballerina-lang';
const BAL_WIDGET_MONACO_THEME = 'bal-widget-monaco-theme';

const MONACO_OPTIONS = {
    autoIndent: true,
    fontFamily: getMonospaceFontFamily(),
    fontSize: 11,
    contextmenu: false,
    renderIndentGuides: false,
    autoClosingBrackets: true,
    matchBrackets: true,
    automaticLayout: true,
    lineNumbersMinChars: 3,
    scrollBeyondLastLine: false,
    minimap: {
        enabled: false,
    },
    renderLineHighlight: 'none',
    scrollbar: {
        useShadows: true,
    },
    hideCursorInOverviewRuler: true,
    lineHeight: 14,
    overviewRulerLanes: 0,
}

/**
 * Source editor component which wraps monaco editor
 */
class CodeEditor extends React.Component {

    /**
     * @inheritDoc
     */
    constructor(props) {
        super(props);
        this.state = {
            editorMounted: false
        };
        this.monaco = undefined;
        this.editorInstance = undefined;
        this.editorDidMount = this.editorDidMount.bind(this);
        this.editorWillMount = this.editorWillMount.bind(this);
    }

    /**
     * Life-cycle hook for editor will mount
     * 
     * @param {Object} monaco Monaco API
     */
    editorWillMount(monaco) {
        this.monaco = monaco;
        monaco.languages.register({ id: BAL_LANGUAGE });
        monaco.editor.defineTheme(BAL_WIDGET_MONACO_THEME, Theme);
        monaco.languages.setMonarchTokensProvider(BAL_LANGUAGE, Grammar);
        monaco.languages.setLanguageConfiguration(BAL_LANGUAGE, BAL_LANG_CONFIG);
    }

    /**
     * Life-cycle hook for editor did mount
     *
     * @param {IEditor} editorInstance Current editor instance
     * @param {Object} monaco Monaco API
     */
    editorDidMount(editorInstance, monaco) {
        this.editorInstance = editorInstance;
        this.setState({
            editorMounted: true
        });
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.sample.fileName !== nextProps.sample.fileName
            && this.editorInstance) {
            this.editorInstance.setScrollPosition({ scrollTop: 0, scrollLeft: 0 });
        }
    }
    

    /**
     * @inheritDoc
     */
    render() {
        return (
            <div className='monaco-editor'>
                {!this.state.editorMounted &&
                    <Dimmer active inverted>
                        <Loader inverted />
                    </Dimmer>
                }
                <MonacoEditor
                    language={BAL_LANGUAGE}
                    value={this.props.content}
                    editorWillMount={this.editorWillMount}
                    editorDidMount={this.editorDidMount}
                    onChange={(newValue) => {
                        this.props.onChange(newValue);
                    }}
                    options={MONACO_OPTIONS}
                    theme={BAL_WIDGET_MONACO_THEME}
                />
            </div>
        );
    }
}

CodeEditor.propTypes = {
    content: PropTypes.string,
    onChange: PropTypes.func,
    sample: PropTypes.shape({
        name: PropTypes.string.isRequired,
        fileName: PropTypes.string.isRequired
    }),
};

CodeEditor.defaultProps = {
    content: '',
    onChange: () => {},
};

export default CodeEditor;
