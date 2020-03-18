Welcome to the Ballerina.io website content repository.

# 1. *build-bbe.sh*

## This script will help to run the Ballerina in local machine.

Steps
1. Clone this repo.
2. execute the build-bbe.sh 


Requirements
1. Go installed in machine

Run the .sh script by considering $2 is for directory name and $1 for version.
```
tools/build-bbe.sh 
```

# 2. *ballerina-dev-website*
Clone the repo.

Install Jekyll and bundler gems
```
gem install jekyll bundler
```

Build the site and make it available on a local server.
```
bundle exec jekyll serve
```
