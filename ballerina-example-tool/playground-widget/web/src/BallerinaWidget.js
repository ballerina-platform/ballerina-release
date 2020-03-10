import React, { Component } from 'react';
import Container from 'semantic-ui-react/dist/es/elements/Container';
import Segment from 'semantic-ui-react/dist/es/elements/Segment';
import CodeEditor from './components/editor/CodeEditor';
import SamplesList from './components/navigation/SamplesList';
import './BallerinaWidget.scss';
import { fetchSamples, fetchSample } from './samples/provider';
import CURLEditor from './components/curl/CURLEditor';
import Console from './components/console/Console';
import ViewSelectPanel, { VIEWS } from './components/controls/ViewSelectPanel';
import RunButton from './components/controls/RunButton';
import DesignView from './components/design-view/DesignView';
import DownloadsView from './components/downloads-view/DownloadsView';
import { getMonospaceFontFamily } from './client-utils';
import githubIcon from './../images/github-mark.svg';
import './styling/semantic.less';

class BallerinaWidget extends Component {

  constructor(...args) {
    super(...args);
    this.state = {
      samples: [],
      selectedSampleIndex: 0,
      selectedView: VIEWS.SOURCE,
      curlVisible: true,
      isReadyToRun: false
    }
    this.consoleRef = undefined;
    this.onSampleSelect = this.onSampleSelect.bind(this);
    this.onCurrentSampleContentChange = this.onCurrentSampleContentChange.bind(this);
  }

  componentDidMount() {
    fetchSamples()
      .then((samples) => {
        this.setState({ 
          samples
        });
        this.onSampleSelect(0);
      })
  }

  onSampleSelect(selectedSampleIndex) {
    const sample = this.state.samples[selectedSampleIndex];
    const { main } = sample;
    this.setState({
      isReadyToRun: false,
      curlVisible: !main
    });
    if (sample.content) {
      this.setState({
        selectedSampleIndex,
        selectedView: VIEWS.SOURCE,
        isReadyToRun: true
      });
    } else {
      const { file, image } = sample;
      fetchSample(file)
        .then((data) => {
           sample.content = data;
           this.setState({
              selectedSampleIndex,
              selectedView: VIEWS.SOURCE,
              isReadyToRun: true
            });
        })
    }
    this.consoleRef.clear();
  }

  onCurrentSampleContentChange(newContent) {
    const sample = this.state.samples[this.state.selectedSampleIndex];
    sample.content = newContent;
    this.forceUpdate();
  }

  render() {
    const { samples, selectedSampleIndex, selectedView, isReadyToRun } = this.state;
    const sample = samples && (samples.length > 0) 
                        && (selectedSampleIndex >= 0)
                        && (samples.length - 1 >= selectedSampleIndex)
                    ? samples[selectedSampleIndex]
                    : undefined;
    const consoleHeight = this.state.curlVisible ? 140 : 168;
    return (
    <Container className="ballerina-playground">
      {sample &&
      <div className="playground-content">
        <Segment.Group className="header">
          <Segment
            className="sample-title"
            onClick={() => {
              window.open(sample.url,'_blank');
            }}
          >
              <span
                className="sample-file-name" 
                style={{ fontFamily: getMonospaceFontFamily() }}
              >
                Example : &lt;{sample.fileName}&gt;</span>
              <span
                className="sample-btn"
              >
                <img name='github' className="github-icon" src={githubIcon} />
              </span>
              {/* <PopOutButton /> */}
          </Segment>
        </Segment.Group>
        <Segment.Group className="body">
          <Segment className="sample-image">
                <img src={'images/examples/' + sample.image} />
          </Segment>
          <Segment className="code-editor">
            <ViewSelectPanel
                selectedView={selectedView}
                onViewSwitch={
                  (selectedView) => {
                    this.setState({ selectedView });
                  }
                }
            />
            {selectedView === VIEWS.SOURCE &&
              <CodeEditor
                content={sample.content || ''}
                onChange={this.onCurrentSampleContentChange}
                sample={sample}
              />
            }
            {selectedView === VIEWS.COMPOSER &&
              <DesignView
                content={sample.content || ''}
              />
            }
            {selectedView === VIEWS.BINARY &&
              <DownloadsView  />
            }
          </Segment>
          {this.state.curlVisible &&
            <Segment className="curl-editor">
              <CURLEditor
                sample={sample}
              />
            </Segment>
          }
          <Segment className="console" style={{ height: consoleHeight }}>
            <Console
              sample={sample}
              ref={(consoleRef) => {
                this.consoleRef = consoleRef;
              }}
              curlVisible={this.state.curlVisible}
              onTryItClick={() => {
              }}
            />
          </Segment>
        </Segment.Group>
        <Segment.Group className="footer">
          <Segment className="controls">
              <div className="navigator">
                  <SamplesList samples={samples} onSelect={this.onSampleSelect} />
              </div>
              <div className="other">
                    <RunButton
                      sample={sample}
                      consoleRef={this.consoleRef}
                      disabled={!isReadyToRun}
                    />
                    {/* <ShareButton /> */}
              </div>    
          </Segment>
        </Segment.Group>
        </div>
      }
        {!sample &&
          <p>No samples are available to display.</p>
        }
    </Container>
    
    );
  }
}

export default BallerinaWidget;
