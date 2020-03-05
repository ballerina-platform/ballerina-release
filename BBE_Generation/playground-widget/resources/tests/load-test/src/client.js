import axios from 'axios';
import WebSocket, { OPEN } from 'ws';
import { resolve } from 'url';
import https from 'https';

export const CONTROLLER_URL = 'https://controller.playground.preprod.ballerina.io/api/launcher';

const COMMON_CONFIG = { 
    headers: {
        'content-type': 'application/json; charset=utf-8',
    },
    httpsAgent: new https.Agent({  
        rejectUnauthorized: false
    })
};

export function fetchLauncherURL(source, curl) {
    const payload = {
        source,
        curl
    };
    return axios.post (
                CONTROLLER_URL,
                payload,
                COMMON_CONFIG
            ).then(({ data }) => {
                return {
                    launcherUrl: `wss://${data['launcher-url']}/api/run`,
                    cacheId: data['cache-id']
                };
            });
}

export function createLauncherConnection(url) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(url, {
            rejectUnauthorized: false
        });
        ws.on('open', () => {
            resolve(ws);
        });
        ws.on('error', (e) => {
            console.log(e);
            reject(new Error('Launcher connection error, ' + e.message, e));
        });
    });
}

export const MSG_CODES = {
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

export function processMsg(testId, msg, onComplete = () => {}, onError = () => {}) {
    const { type, message, code } = JSON.parse(msg);
    if (message.startsWith('build completed in')) {
        console.log('Test ' + testId + ': ' + message);
    }
    switch (code) {
        case MSG_CODES.DEP_SERVICE_EXECUTION_STARTED:
        case MSG_CODES.DEP_SERVICE_EXECUTION_ERROR:
        case MSG_CODES.DEP_SERVICE_EXECUTION_STOPPED:
        case MSG_CODES.EXECUTION_STARTED:
                break;
        case MSG_CODES.EXECUTION_STOPPED:
        case MSG_CODES.PROGRAM_TERMINATED:
                onComplete();
                break;
        case MSG_CODES.ERROR:
        case MSG_CODES.BUILD_ERROR:
        case MSG_CODES.RUN_ABORTED:
                onError(message);
                break;
        case MSG_CODES.BUILD_STARTED:
                break;
        default: ;
    }
}

export function createLaunchCmd(source, curl, cacheId = '') {
    const cmd = {
        command: 'run',
        fileName: 'load-test.bal',
        source,
        curl,
        noOfCurlExecutions: 1,
        dependantService: '',
        resources: [],
        postCurlDelay: 0
    };
    if (cacheId) {
        cmd['cacheId'] = cacheId;
    }
    return cmd;
}


