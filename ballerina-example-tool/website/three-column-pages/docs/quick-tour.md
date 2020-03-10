# Quick Tour

Now that you know [a little bit about Ballerina](index.md), let's take it for a spin! 

## Install Ballerina

1. Go to http://www.ballerinalang.org and click **Download**. 
1. Download the Ballerina Tools distribution and unzip it on your computer. Ballerina Tools includes the Ballerina runtime plus the visual editor (Composer) and other tools. 
1. Add the `<ballerina_home>/bin` directory to your $PATH environment variable so that you can run the Ballerina commands from anywhere. 

>NOTE: Throughout this documentation, `<ballerina_home>` refers to the Ballerina directory you just installed. 

## Run HelloWorld

The HelloWorld sample will show you how easy it is to run Ballerina, send it a request, and get a response. 

Let's take a look at what the sample looks like in the Ballerina programming language:

```
import ballerina.lang.system;
function main (string[] args) {
  system:println("Hello, World!");
}
``` 

The HelloWorld sample doesn't take any specific input, so simply running it will cause it to print "Hello, World!" at the command line.

At the command prompt, navigate to the `<ballerina_home>/samples/helloWorld` directory and enter the following line:

```
ballerina run main helloworld.bal
```

You will see the following response:

```
Hello, World!
```

You just started Ballerina, ran the HelloWorld sample, and got a response within seconds. 
