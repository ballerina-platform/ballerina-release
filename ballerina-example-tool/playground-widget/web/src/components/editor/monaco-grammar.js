/*
 *  Copyright (c) 2018, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 *  WSO2 Inc. licenses this file to you under the Apache License,
 *  Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing,
 *  software distributed under the License is distributed on an
 *  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *  KIND, either express or implied.  See the License for the
 *  specific language governing permissions and limitations
 *  under the License.
 */
const letter = '[a-zA-Z_]';
const letterOrDigit = '[a-zA-Z0-9_]';
const identifierLiteralChar = '[^|"\\\f\n\r\t]|\\\\[btnfr]|\\[|"\\/]';
const identifier = `${letter}${letterOrDigit}*)|(\^"${identifierLiteralChar}+")`;
const tokenizer = require('./monarch-tokenizer.json')


export default {
    defaultToken: 'identifier',
    controlKeywords: [
        'if', 'else', 'iterator', 'try', 'catch', 'finally', 'fork', 'join', 'all', 'some',
        'while', 'throw', 'return', 'returns', 'break', 'timeout', 'transaction', 'aborted',
        'abort', 'committed', 'failed', 'retries', 'continue', 'bind', 'with', 'lengthof', 'typeof',
        'foreach', 'in', 'match', 'but', 'check', 'retry'
    ],

    otherKeywords: [
        'import', 'version', 'public', 'attach', 'as', 'native',
        'annotation', 'package', 'connector', 'function', 'resource', 'service', 'action',
        'worker', 'struct', 'transformer', 'endpoint', 'record',
        'const', 'true', 'false', 'reply', 'create', 'parameter', 'new', 'async', 'untaint', 'done', 'start',
        'onretry', 'oncommit', 'onabort', 'sealed', 'primarykey', 'scope', 'compensate', 'compensation'
    ],

    typeKeywords: [
        'boolean', 'int', 'float', 'string', 'var', 'any', 'datatable', 'table', 'byte',
        'map', 'exception', 'json', 'xml', 'xmlns', 'error', 'type', 'future'
    ],

    operators: [
        '!', '%', '+', '-', '~=', '==', '===', '=', '!=', '<', '>', '&&', '\\', '?:',
    ],

    brackets: [
        ['{', '}', 'delimiter.curly'],
        ['[', ']', 'delimiter.square'],
        ['(', ')', 'delimiter.parenthesis'],
        ['<', '>', 'delimiter.angle'],
    ],

    // we include these common regular expressions
    symbols: /[=><!~?:&|+\-*\/\^%]+/,

    // C# style strings
    escapes: /\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,

    tokenizer,

};