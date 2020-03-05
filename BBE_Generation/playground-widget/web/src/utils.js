
import axios from 'axios';

const isProduction = process.env.NODE_ENV === 'production';

const HOST =  isProduction 
                    ? BACKEND_HOST
                    : 'localhost:8081';

export const FETCH_LAUNCHER_API = `http${isProduction ? 's' : ''}://${isProduction ? 'controller.' : ''}${HOST}/api/launcher`;
export const PARSER_API_URL = `http${isProduction ? 's' : ''}://${isProduction ? 'parser.' : ''}${HOST}/api/parser`;

function createLauncherURL(launcherHost) {
    return `ws${isProduction ? 's' : ''}://${launcherHost}/api/run`;
}

export function fetchLauncherURL(sample) {
    if (!isProduction) {
        return Promise.resolve({
            launcherUrl: createLauncherURL(HOST),
            cacheId: undefined
        });
    }
    const payload = {
        source: sample.content,
        curl: sample.curl
    };
    return axios.post(FETCH_LAUNCHER_API, payload,
            { 
                headers: {
                    'content-type': 'application/json; charset=utf-8',
                } 
            })
            .then(({ data }) => {
                return {
                    launcherUrl: createLauncherURL(data['launcher-url']),
                    cacheId: data['cache-id']
                };
            });
}