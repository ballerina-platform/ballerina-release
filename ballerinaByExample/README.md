Welcome to the Ballerina.io website content repository.

# 1. How to build BBE

This will guide you through the process of using the `build-bbe.sh` tool to generate BBEs as html.


### How to run

##### Requirements
1. Go installed in machine

>**Tip:** The below are a few troubleshooting tips you may require when installing Go.

- If you get the `no required module provides package github.com/russross/blackfriday: go.mod file not found in current directory or any parent directory; see 'go help modules'` error message, execute the `go mod init c/projects/go-projects/go-server` command.
- If you get the `no required module provides package github.com/russross/blackfriday; to add it:
	go get github.com/russross/blackfriday` error message, execute the `go get github.com/russross/blackfriday` command.

##### Steps
1. Clone this repo.
2. execute the build-bbe.sh 

```bash
sudo ./ballerinaByExample/build-bbe.sh <site_version> <output_dir> <ballerina_repo_tag> <generateWithJekyll> <isLatestVersion>
```

**site_version**

This is the version of the site that the tool should generate the BBEs for.
Ex: 1.2 or 1.1

**output_dir**

This is the output directory where the tool will save the generated BBEs html files.

**ballerina_repo_tag**

This is the Ballerina tag that the examples should be extracted from and then use to generate
the BBEs.

Ex: v1.2.0 or v1.1.0.

**generateWithJekyll**

This is the flag to indicate the tool to generate BBEs with or without jekyll front matter.

If pass in `true` it will generate BBEs with jekyll front matter.
If pass in `false` it will generate BBEs without jekyll front matter but as a normal html file.

**isLatestVersion**

This is the flag to indicate the tool to generate BBE for the latest version of Ballerina.

If pass in `true` it will generate BBE with permalink set to `/learn/<etc>`
If pass in `false` it will generate BBE with permalink set to `/<version>/learn/<etc>`

##### Example Usage

* When building examples for website.

```bash
sudo ./ballerinaByExample/build-bbe.sh 1.2 bbes v1.2.0 true false
```

This will generate BBE with jekyll front matter.

* When building examples for normal use.

```bash
sudo ./ballerinaByExample/build-bbe.sh 1.2 bbes v1.2.0 false false
```

This will generate BBE without jekyll front matter but as plain html.

* When building examples for latest ballerina version for the site.

```bash
sudo ./tools/build-bbe.sh 1.2 bbes v1.2.0 true true
```

# 2. Executing BBE gen-tool in github workflows

In addition to above, the tool can be executed by pointing to metadata.json
file which is generated for each release along with the new installers.
This mode is quite useful when used for automation. Instead of taking the 
BBEs from the code, this tool takes the BBEs from ballerina-<version>.zip.

```
./ballerinaByExample/build-bbe-wf.sh _data/metadata.json
```

This will generate BBE with jekyll permalink set to `/learn` as root.

# 3. *ballerina-dev-website*
Clone the repo.

Install Jekyll and bundler gems
```
gem install jekyll bundler
```

Build the site and make it available on a local server.
```
bundle exec jekyll serve
```
