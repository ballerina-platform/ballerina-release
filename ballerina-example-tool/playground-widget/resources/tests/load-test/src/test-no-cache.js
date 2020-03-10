import { readFileSync, openSync as openFileSync } from 'fs';
import { join as joinPath } from 'path';
import { fetchLauncherURL, createLauncherConnection, createLaunchCmd, processMsg } from './client';

const curl = "curl -s -X POST -d 'Ballerina' http://playground.localhost/greeting";
const sampleSource = readFileSync(openFileSync(joinPath(__dirname, 'sample.bal'), 'r'), { encoding: 'utf8' });

let count = 0;

const NO_OF_CONCURRENT_REQUESTS = 20;

function runSample(testId, source, curl, launcherURL, cacheId) {
    createLauncherConnection(launcherURL)
        .then((launcherConnection) => {
            launcherConnection.on('message', (msg) => {
                processMsg(testId, msg, 
                    () => {
                        launcherConnection.close();
                        console.log('Test '+ testId + ': Running sample completed successfully.');
                    },
                    (err) => {
                        console.log('Test '+ testId + ': Error while running sample. Err: ' + err);
                    }
                );
            })
            launcherConnection.send(JSON.stringify(createLaunchCmd(source, curl, cacheId)));
        })
        .catch((e) => {
            console.log('Test '+ testId + ': Error while running sample. Err: ' + e.message);
        });
}

function fetchLauncherURLs() {
    while (count < NO_OF_CONCURRENT_REQUESTS) {
        const testId = count;
        const source = sampleSource.replace('CACHE_CONTROL_PLACEHOLDER', Date.now() + testId);
        fetchLauncherURL(source, curl)
            .then((data) => {
                console.log('Test '+ testId + ': Received launcher for execution at ' + data.launcherUrl);
                runSample(testId, source, curl, data.launcherUrl, data.cacheId);
            })
            .catch((err) => {
                console.log('Test '+ testId + ': Error while fetching launcher url. Error Code: ' + err);
            });
        count++; 
    }
}



fetchLauncherURLs();

