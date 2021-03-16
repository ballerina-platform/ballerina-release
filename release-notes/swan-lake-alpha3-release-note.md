---
layout: ballerina-blank-page
title: Release Note
---
### Overview of Ballerina Swan Lake Alpha3

This Alpha3 release includes the language features planned for the Ballerina Swan Lake release. Moreover, this release includes improvements and bug fixes to the compiler, runtime, standard library, and developer tooling. This release note lists only the features and updates added after the Alpha2 release of Ballerina Swan Lake.

- [Updating Ballerina](#updating-ballerina)
    - [For Existing Users](#for-existing-users)
    - [For New Users](#for-new-users)
- [Highlights](#highlights)
- [What is new in Ballerina Swan Lake Alpha3](#what-is-new-in-ballerina-swan-lake-alpha3)
    - [Language](#language)
    - [Runtime](#runtime)
    - [Standard Library](#standard-library)
    - [Code to Cloud](#code-to-cloud)
    - [Developer Tools](#developer-tools)
    - [Breaking Changes](#breaking-changes)

### Updating Ballerina

You can use the [Update Tool](/learn/tooling-guide/cli-tools/update-tool/) to update to Ballerina Swan Lake Alpha3 as follows.

#### For Existing Users

If you are already using Ballerina, you can directly update your distribution to the Swan Lake channel using the [Ballerina Update Tool](/learn/tooling-guide/cli-tools/update-tool/). To do this, first, execute the command below to get the update tool updated to its latest version. 

> `bal update`

If you are using an **Update Tool version below 0.8.14**, execute the `ballerina update` command to update it. Next, execute the command below to update to Swan Lake Alpha3.

> `bal dist pull slalpha3`

#### For New Users

If you have not installed Ballerina, then download the [installers](/downloads/#swanlake) to install.

### Highlights

### What is new in Ballerina Swan Lake Alpha3

#### Language

##### Support for Module-level Variables with List, Mapping, and Error Binding Patterns

Variable declarations with list, mapping, and error binding patterns are now allowed at module level. Unlike simple variables, these variables must be initialized in the declaration.

Also, these variable declarations cannot contain an `isolated` or `configurable` qualifier.

```ballerina
type Person record {|
    string name;
    boolean married;
|};

function getList() returns [int, float] => [1, 2.5];

function getPerson() returns Person => {name: "John", married: true};

function getError() returns error => error("error message", code = 1001, fatal = true);

// Module-level variable declaration with a list binding pattern. 
[int, float] [a, b] = getList();

// Module-level variable declaration with a mapping binding pattern.
Person {name: firstName, married: isMarried} = getPerson();

// Module-level variable declaration with an error binding pattern.
error error(message, code = errCode) = getError();
```

##### Support for Module-level Public Variables

Module-level variables can now be declared as public using the `public` qualifier. Such variables will be visible outside the modules in which they are declared.

Isolated variables and variables declared with `var` cannot be declared as public variables.

```ballerina
public string name = "Ballerina";

public [int, float] [a, b] = [1, 2.5];
```

##### Improvement to Annotation Attachment with Empty Mapping Constructor Expression

If the type of the annotation is a mapping type for which an empty mapping constructor is valid, the mapping constructor expression is no longer mandatory in the annotation attachment.

The absence of the mapping constructor expression in such an annotation attachment is equivalent to specifying a mapping constructor expression with no fields.
```ballerina
type Annot record {|
    int[] i = [];
|};

public annotation Annot v1 on function;

@v1 // Same as `@v1 {}`
public function main() {
}
```

##### Introduction of the `function` Function Type Descriptor to Represent Any Function

A new `function` type descriptor has been introduced to represent all function values.

```ballerina
import ballerina/io;

function add(int v1, int v2) returns int => v1 + v2;

function compare(int v1, int v2) returns boolean => v1 < v2;

public function main() {
    // A variable of type `function` can hold any function value.
    function f = add;
    io:println("Process (add, 1, 2): ", process(f, 1, 2)); // Prints `Process (add, 1, 2): 3`
    io:println("Process (compare, 1, 2): ", process(compare, 1, 2)); // Prints `Process (compare, 1, 2): 0`
}

function process(function func, int v1, int v2) returns int {
    // A function of type `function` cannot be called directly.
    // A function value assigned to a `function` typed variable 
    // can only be called after the type is narrowed to the relevant type.
    if (func is function (int, int) returns int) {
        return func(v1, v2);
    }
    return 0;
}
```

##### Improved lang library functions

###### New `xml:text()` function

This function can be used to select all the items in a sequence that are of type `xml:Text`.

```ballerina
xml name = xml `<name>Dan<middleName>Gerhard</middleName><!-- This is a comment -->Brown</name>`;
xml:Text nameText = (name/*).text();
io:println(nameText); // "DanBrown"
```

#### Runtime

#### Standard Library

##### HTTP Package Updates

Changed the return types of the client methods to depend on the `targetType` argument. The default `targetType` is `http:Response`.
```ballerina 
http:Client myClient = check new ("http://localhost:9090”);
http:Response response = check myClient->post("/backend/getResponse", "want response");
json jsonPayload = check myClient->post("/backend/getJson", "want json", targetType = json);
xml xmlPayload = check myClient->post("/backend/getXml", "want xml", targetType = xml);
```

Introduced a header map as an optional argument for non-entity-body client remote methods (GET, HEAD, OPTIONS). 
```ballerina
http:Client myClient = check new ("http://localhost:9090”);
map<string|string[]> accHeaders = { "Accept" : "application/json" };
var response = myclient->get("/some/endpoint", accHeaders);
```

Introduced header map and media type as optional arguments for entity body client remote methods (POST, PUT, PATCH, DELETE, EXECUTE).
```ballerina
http:Client myClient = check new ("http://localhost:9090”);
json payload = {}; 
map<string|string[]> accHeaders = { "Accept" : "application/json" };
var response = myclient->post("/some/endpoint", payload, headers = accHeaders);
```

Improved the data types of outbound request/response payloads which can be set directly.  
```ballerina
type RequestMessage Request|string|xml|json[]|byte[]|int|float|decimal|boolean|map<json>|table<map<json>>|
                      table<map<json>>[]|mime:Entity[]|stream<byte[], io:Error>|();

type ResponseMessage Response|string|xml|json|byte[]|int|float|decimal|boolean|map<json>|table<map<json>>|
                      (map<json>|table<map<json>>)[]|mime:Entity[]|stream<byte[], io:Error>|();
```

Marked HTTP client remote methods as isolated.

Introduced module error inheritance and remove error union types.

##### WebSocket Package Updates

Introduced auth support for the websocket client.
Bearer token, Basic auth, JWT, and OAuth2 support has been introduced with the WebSocket client declarative authentication.

Introduced HTTP cookie support for the WebSocket client.
```ballerina
http:Cookie cookie = new ("username", "name");
http:Cookie[] httpCookies = [cookie];

websocket:ClientConfiguration clientConf = {
  cookies: httpCookies
};

websocket:Client wsClient = check new ("ws://localhost:21316/ws", config = clientConf);
```

Made the `websocket:Caller` optional in WebSocket service remote functions.

Introduced support to send text, binary, and pong messages by returning them from the remote methods. 
Users can send text/binary data to the peer by returning a `string` or a `byte[]` value from the `onTextMessage` and `onBinaryMessage` remote methods. And users can send a pong frame to the peer by returning a `byte[]` value from the `onPing` remote method.
```ballerina
remote function onTextMessage(string text) returns string {
    return "Hello World!";
}
```
```ballerina
remote function onPing(byte[] pingData) returns byte[] {
    return pingData;
}
```

Removed the support for `websocket:AsyncClient`.

##### GraphQL Package Updates

Added the support for hierarchical resource paths.
The Ballerina GraphQL resources now can have hierarchical resource paths. Each intermediate resource path then maps to a new type in the generated schema.
```ballerina
import ballerina/graphql;

service /graphql on new Listener(9104) {
   isolated resource function get profile/name/first() returns string {
       return "Sherlock";
   }

   isolated resource function get profile/name/last() returns string {
       return "Holmes";
   }

   isolated resource function get profile/age() returns int {
       return 40;
   }
}
```

Supported resource functions to return optional types. 

The Ballerina GraphQL resources now can return optional types. 
```ballerina
resource function get profile/name/first(int id) returns string? {
    if id == 0 {
        return "sherlock";
    }
}
```

##### Email Package Updates

Enabled read/listen for multiple emails in a single TCP connection.
Each POP3 or IMAP client/listener creation initiates the connection.
Then email sending, receiving or listening operation can be performed many times.
Finally the client/listener has to be closed.

POP3 Client example
```ballerina
email:PopClient popClient = check new ("pop.email.com", "reader@email.com","pass456");
email:Message? emailResponse = check popClient->receiveMessage();
check popClient->close();
```

In IMAP Client a similar format is used.

POP3 Service example
```ballerina
service object {} emailObserver = service object {
   remote function onMessage(Message emailMessage) {

   }

   remote function onError(Error emailError) {

   }

   remote function onClose(Error? closeError) {

   }

};
```

Note how the `close()` method calls the `onClose` method in the service.

Made email body a mandatory field in `sendEmail` method API.

Renamed email sending method names removing `Email` in each of them 
Renamed `sendEmail` as `send`, `sendEmailMessage` as `sendMessage`, `receiveEmailMessage` as `receiveMessage` and `onEmailMessage` as `onMessage`.

Set default `from` address of `email:Message` record from the `SmtpClient` authentication field, `username`.
Earlier the username for authentication was decoupled from message data. Now the field `from` is made optional and default value will be set from the username.

Made POP3 and IMAP clients as blocking clients by providing an optional `timeout` argument
Time unit is seconds and the data type is `decimal`. Default value is 0 where the inbuilt polling interval is 100 milliseconds.
A sample client code is as follows.
```ballerina
email:Message|email:Error? email = popClient->receiveMessage(timeout = 2);
```
In `PopListener` and `ImapListener` configuration polling interval is not set with `decimal` type in seconds to the field, `pollingInterval`, which was earlier named as `pollingIntervalInMillis`.

Renamed `email:SmtpConfig`, `email:PopConfig`, `email:ImapConfig`, `email:PopListenerConfig` and `email:ImapListenerConfiguration` as `email:SmtpConfiguration`, `email:PopConfiguration`, `email:ImapConfiguration`, `email:PopListenerConfiguration` and `email:ImapListenerConfiguration` respectively.

Removed the field, `cronExpression` from `email:ImapListenerConfig` and `email:PopListenerConfig`.

Made the `body` field of `send` method mandatory in `email:SmtpClient`. 

##### WebSub Package Updates

Introduced websub-listener-configuration for websub-listener
```ballerina
import ballerina/websub;

websub:ListenerConfiguration configs = {
    		secureSocket: {
        		key: {
            		certFile: "../resource/path/to/public.crt", 
                    keyFile: "../resource/path/to/private.key"
        		}
    		}    
    // any additional configurations related to http-listener 
};

service /subscriber on new websub:Listener(9090, configs) {
   // resources
}
```

##### WebSubHub Package Updates

Included HTTP Headers parameter into WebSub Hub API
```ballerina
import ballerina/websubhub;
import ballerina/http;

listener websubhub:Listener hubListener = new(9095);

service /websubhub on new websubhub:Listener(9090) {
    remote function onRegisterTopic(TopicRegistration message, http:Headers requestHeaders)
                                returns TopicRegistrationSuccess|TopicRegistrationError {
		return {};
    }
    // http:Headers parameter will be an optional parameter for all the API endpoints
}
```

Introduced pre-initialized constant responses to be used in `websubhub:Service` implementation
```ballerina
import ballerina/websubhub;

service /websubhub on new websubhub:Listener(9090) {

    remote function onRegisterTopic(websubhub:TopicRegistration message)
                                returns websubhub:TopicRegistrationSuccess {
        log:print("Received topic-registration request ", message = message);
        return websubhub:TOPIC_REGISTRATION_SUCCESS;
    }

    // implement other service methods
}
```

Initializing `websubhub:HubClient` with client configurations
```ballerina
import ballerina/websubhub;

websubhub:ClientConfiguration config = {
    retryConfig: {
        interval: 3,
            count: 3,
            backOffFactor: 2.0,
            maxWaitInterval: 20,
            statusCodes: [500]
        },
        timeout: 2
    };

HubClient hubClientEP = check new(subscriptionMsg, config);

websubhub:ContentDistributionMessage msg = {content: "This is sample content delivery"};

var publishResponse = hubClientEP->notifyContentDistribution(msg);
```

Introduced websubhub listener configuration to configure websubhub listener. 
```ballerina
import ballerina/websubhub;

websubhub:ListenerConfiguration configs = {
    		secureSocket: {
        			key: {
            			certFile: "../resource/path/to/public.crt", 
keyFile: "../resource/path/to/private.key"
        			}
    		}
    
    	// any additional configurations related to http-listener 
};

service /hub on new websubhub:Listener(9090, configs) {
    		// resources
}
```

##### Security Updates

Renamed the `ballerina/encoding` module as `ballerina/url` and updated the APIs.
```ballerina
import ballerina/url;

string|url:Error encoded = url:encode("http://localhost:9090", "UTF-8");
string|url:Error decoded = url:decode("http%3A%2F%2Flocalhost%3A9090", "UTF-8");
```

The Ballerina HTTP listener can be configured to authenticate and authorize the inbound requests with Basic Auth file user store.

Improved client and listener `SecureSocket` APIs of HTTP, GRPC, WebSocket, GraphQL, WebSub, WebSubHub, TCP, Email, NATS, STAN and RabbitMQ modules.
```ballerina
public type ListenerSecureSocket record {|
   crypto:KeyStore|CertKey key;
   record {|
       VerifyClient verifyClient = REQUIRE;
       crypto:TrustStore|string cert;
   |} mutualSsl?;
   record {|
       Protocol name;
       string[] versions = [];
   |} protocol?;
   record {|
       CertValidationType type = OCSP_STAPLING;
       int cacheSize;
       decimal cacheValidityPeriod;
   |} certValidation?;
   string[] ciphers = [];
   boolean shareSession = true;
   decimal handshakeTimeout?;
   decimal sessionTimeout?;
|};

public type ClientSecureSocket record {|
   boolean enable = true;
   crypto:TrustStore|string cert?;
   crypto:KeyStore|CertKey key?;
   record {|
       Protocol name;
       string[] versions = [];
   |} protocol?;
   record {|
       CertValidationType type = OCSP_STAPLING;
       int cacheSize;
       decimal cacheValidityPeriod;
   |} certValidation?;
   string[] ciphers?;
   boolean verifyHostName = true;
   boolean shareSession = true;
   decimal handshakeTimeout?;
   decimal sessionTimeout?;
|};

public type CertKey record {|
   string certFile;
   string keyFile;
   string keyPassword?;
|};
 
public enum VerifyClient {
   REQUIRE,
   OPTIONAL
}
 
public enum Protocol {
   SSL,
   TLS,
   DTLS
}
 
public enum CertValidationType {
   OCSP_CRL,
   OCSP_STAPLING
}
```

Improved `SecureSocket` configuration of JDK11 client of JWT and OAuth2 modules.

Added support for OAuth2 client authentication of JDK11 client, which is used to call authorization endpoint.

##### TCP Package Updates

Introduced SSL/TLS support for both the client and listener.
```ballerina
import ballerina/tcp;

configurable string certPath = ?;

public function main() returns error? {
    tcp:Client socketClient = check new ("localhost", 9002, secureSocket = {
        cert: certPath,
        protocol: {
            name: tcp:TLS,
            versions: ["TLSv1.2", "TLSv1.1"]
        },
        ciphers: ["TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"]
    });

    string msg = "Hello Ballerina Echo from secure client";
    byte[] msgByteArray = msg.toBytes();
    check socketClient->writeBytes(msgByteArray);

    readonly & byte[] receivedData = check socketClient->readBytes();

    check socketClient->close();
}
```

```ballerina
configurable string keyPath = ?;
configurable string certPath = ?;

service on new tcp:Listener(9002, secureSocket = {
       key: {
        certFile: certPath,
        keyFile: keyPath
    },
    protocol: {
        name: tpc:TLS,
        versions: ["TLSv1.2", "TLSv1.1"]
    },
    ciphers: ["TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"]
}) {

    isolated remote function onConnect(tcp:Caller caller) returns tcp:ConnectionService {
        io:println("Client connected to secureEchoServer: ", caller.remotePort);
        return new EchoService(caller);
    }
}

service class EchoService {
  
    remote function onBytes(readonly & byte[] data) returns (readonly & byte[])|tcp:Error? {
        io:println("Echo: ", 'string:fromBytes(data));
        return data;
    }
}
```

Included tcp:Caller as an optional parameter in onBytes() method.
```
service class EchoService {
  
    remote function onBytes(tcp:Caller caller, readonly & byte[] data) returns (readonly & byte[])|tcp:Error? {
        io:println("Echo: ", 'string:fromBytes(data));
        check caller->writeBytes(data);
    }
}
```

##### Kafka Package Updates

Renamed `sendProducerRecord` function in the client object `Producer` to `send`.

Renamed `flushRecords` function in the client object `Producer` to `’flush`.

Replaced `kafka:ConsumerError` and `kafka:ProducerError` with `kafka:Error`.

##### NATS Package Updates

Renamed `ConnectionConfig` record to `ConnectionConfiguration`. 

Included `url` as a field in `ConnectionConfiguration` record. 

Changed `ConnectionConfiguration` in client and listener init functions to an included record parameter. This allows the users to pass the record field values as named parameters. 

##### STAN Package Updates

Renamed `StreamingConfig` record to `StreamingConfiguration`. 

Included `url` as a field in `StreamingConfiguration` record. 

Changed `StreamingConfiguration` in client and listener init functions to an included record parameter. This allows the users to pass the record field values as named parameters. 

##### RabbitMQ Package Updates

Renamed `ConnectionConfig` record to `ConnectionConfiguration`. 

###### Common Standard Library Updates

All the timeout configurations are converted to accept decimal values and the time unit is in seconds.

#### Code to Cloud

#### Developer Tools

##### Language Server

##### Ballerina Shell

- The Ballerina Shell now supports redefining module-level definitions and variable declarations. 

```ballerina
=$ int i = 3;
=$ string j = "Hi";
=$ string i = "Hello";  // Same variable can be redefined
```

- A new `/remove` command has been introduced to be used from within the Ballerina Shell to remove one or more declarations from the snippet memory.

```ballerina
=$ int i = 3;
=$ string j = "Hi";
=$ /remove i j
=$ i
| error: undefined symbol 'i'
|       i
|       ^
| Compilation aborted due to errors.
```

- Ballerina Shell can now load definitions and declarations from a file. The file to load from can be specified using the `-f` or `--file` command-line options when launching the Ballerina Shell. Alternatively, the `/file` command can also be used for this purpose from within the Shell. 

```bash
$ bal shell -f my_file.bal
```

The `--force-dumb` command-line option will now have only a long option and the short option `-f` is now used to load from a file.

- The Ballerina Shell now supports cyclic type definitions and list binding patterns.

- The Ballerina Shell now preserves qualifiers such as the `final` qualifier of a variable declaration.

##### Debugger

Now, the debugger supports conditional breakpoints. Conditional expressions can be configured for Ballerina breakpoints in the VSCode debug view.

#### Breaking Changes
1. `==` and `!=` equality expressions can no longer be used with variables of type `readonly`.
