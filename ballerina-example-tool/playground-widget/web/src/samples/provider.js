import { samples } from './data.json';
import axios from 'axios';

const SAMPLE_FOLDER = 'resources/guides';

export function fetchSamples() {
    return new Promise((resolve, reject) => {
        if (samples && samples.length > 0) {
            resolve(samples);
        } else {
            reject('Samples are not found');
        }
    });
}

export function fetchSample(fileName) {
    return axios(SAMPLE_FOLDER + '/' + fileName)
               .then((response) => {
                    return response.data;
               });
}
