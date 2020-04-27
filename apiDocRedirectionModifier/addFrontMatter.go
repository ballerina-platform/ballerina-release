package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"text/template"
)

var apiDocsDir = os.Args[1]
var redirectVersion = os.Args[2]
var permalinkPreFix = os.Args[3]
var outputLocation = os.Args[4]

var fileExtension = ".html"
var templateDir = "templates/"

type APIDoc struct {
	FileName         string
	PermalinkPostFix string
	RedirectVersion  string
	Content          string
}

func main() {
	var files []string
	createDir(outputLocation)
	err := filepath.Walk(apiDocsDir, func(path string, info os.FileInfo, err error) error {
		files = append(files, path)
		split := strings.Split(path, permalinkPreFix)
		fileRelativeURL := split[len(split)-1]
		fileName := info.Name()
		dirForFile := strings.Split(fileRelativeURL, fileName)[0]
		fullPathToOutput := filepath.Join(outputLocation, dirForFile)
		createDir(fullPathToOutput)

		if filepath.Ext(path) == fileExtension {
			fileContent := mustReadFile(path)

			docTmpl, tmplError := template.New("api-doc").Parse(mustReadFile(filepath.Join(templateDir, "api-doc.tmpl")))
			check(tmplError)
			fileNameSplits := strings.Split(fileName, fileExtension)
			onlyFileName := fileNameSplits[0]
			apidoc := APIDoc{
				RedirectVersion:  redirectVersion,
				Content:          fileContent,
				PermalinkPostFix: filepath.Join(permalinkPreFix, dirForFile, onlyFileName),
			}

			apiDocsFile, errorCreatingAPIDoc := os.Create(filepath.Join(fullPathToOutput, fileName))
			check(errorCreatingAPIDoc)
			docTmpl.Execute(apiDocsFile, apidoc)
		} else if !info.IsDir() {
			from, err := os.Open(path)
			if err != nil {
				log.Fatal(err)
			}
			defer from.Close()

			to, err := os.OpenFile(filepath.Join(fullPathToOutput, fileName), os.O_RDWR|os.O_CREATE, 0666)
			if err != nil {
				log.Fatal(err)
			}
			defer to.Close()

			_, err = io.Copy(to, from)
			if err != nil {
				log.Fatal(err)
			}
		}
		return nil
	})
	if err != nil {
		panic(err)
	}
	for _, file := range files {
		fmt.Println(file)
	}
}

func createDir(dir string) {
	_, err := os.Stat(dir)

	if os.IsNotExist(err) {
		errDir := os.MkdirAll(dir, 0755)
		if errDir != nil {
			log.Fatal(err)
		}
	}
}

func mustReadFile(path string) string {
	bytes, err := ioutil.ReadFile(path)
	check(err)
	return string(bytes)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
