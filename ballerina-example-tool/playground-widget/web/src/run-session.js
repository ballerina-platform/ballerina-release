// See http://tools.ietf.org/html/rfc6455#section-7.4.1
const WS_NORMAL_CODE = 1000;
const WS_SSL_CODE = 1015;

/**
 * RunSession
 *
 * @class RunSession
 */
class RunSession {

    /**
     * Creates an instance of RunSession.
     * @param {Object} args - connection configurations
     *
     * @memberof RunSession
     */
    constructor(endpoint) {
        if (!endpoint) {
            throw new Error('Invalid Endpoint');
        }
        this.endpoint = endpoint;
    }

    /**
     * init to run api and register callbacks
     *
     * @memberof RunSession
     */
    init({ 
            onMessage = () => {}, 
            onOpen = () => {},
            onClose = () => {}, 
            onError = () => {},
        }) {
        const websocket = new WebSocket(this.endpoint);
        // bind functions
        websocket.onmessage = (strMessage) => { onMessage(JSON.parse(strMessage.data)); };
        websocket.onopen = onOpen;
        websocket.onclose = onClose;
        websocket.onerror = onError;
        this.websocket = websocket;
    }

     /**
     * Send message to run given sample and execute curl after
     * 
     * @param {Object} sample - sample
     * @param {String} cacheId - cacheID
     *
     * @memberof LaunchManager
     */
    run(sample, cacheId = undefined) {
        const { 
            fileName,
            content,
            curl,
            noOfCurlExecutions = 1,
            dependantService = '',
            resources = [],
            postCurlDelay = 0,
        } = sample;
        const cmd = {
            command: 'run',
            fileName,
            source: content,
            curl,
            noOfCurlExecutions,
            dependantService,
            resources,
            postCurlDelay
        };
        if (cacheId) {
            cmd['cacheId'] = cacheId;
        }
        this.sendMessage(cmd);
    }

    /**
     * send stop command.
     *
     * @memberof RunSession
     */
    stop() {
        this.sendMessage({
            command: 'stop',
        });
    }

    /**
     * Sends message to backend
     * 
     * @param {Object} message - object to send
     *
     * @memberof RunSession
     */
    sendMessage(message) {
        if (this.websocket.CONNECTING) {
            this.websocket.onopen = () => {
                this.websocket.send(JSON.stringify(message));
            }
        } else if (this.websocket.OPEN) {
            this.websocket.send(JSON.stringify(message));
        } else {
            throw new Error('Unable to send message: ' + JSON.stringify(message))
        }
        
    }

    /**
     * Close websocket channel.
     *
     * @memberof RunSession
     */
    close() {
        if (this.websocket.CONNECTING || this.websocket.OPEN) {
            this.websocket.close();
        }
    }
}

export default RunSession;