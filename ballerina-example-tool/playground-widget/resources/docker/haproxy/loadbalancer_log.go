/*
Copyright 2015 The Kubernetes Authors All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/golang/glog"
	"github.com/ziutek/syslog"
	"time"
)

type handler struct {
	*syslog.BaseHandler
}

type syslogServer struct {
	*syslog.Server
}

// newSyslogServer start a syslog server using a unix socket to listen for connections
func newSyslogServer(path string) (*syslogServer, error) {
	glog.Infof("Starting syslog server for haproxy using %v as socket", path)
	// remove the socket file if exists
	os.Remove(path)

	server := &syslogServer{syslog.NewServer()}
	server.AddHandler(newHandler())
	err := server.Listen(path)
	if err != nil {
		return nil, err
	}

	return server, nil
}

func newHandler() *handler {
	h := handler{syslog.NewBaseHandler(1000, nil, false)}
	go h.mainLoop()
	return &h
}

func (h *handler) mainLoop() {
	for {
		message := h.Get()
		if message == nil {
			break
		}

		if !(strings.HasPrefix(message.Tag, "Proxy") && strings.HasSuffix(message.Content, " started.")) &&
			!(strings.HasPrefix(message.Tag, "Stopping") && strings.HasSuffix(message.Content, " in 0 ms.")) &&
			!(strings.HasPrefix(message.Tag, "Server") && strings.HasSuffix(message.Content, "0 remaining in queue.")) &&
			!(strings.HasPrefix(message.Tag, "Proxy") && strings.HasSuffix(message.Content, "(FE: 0 conns, BE: 0 conns).")) &&
			!(strings.HasSuffix(message.Content, "has no server available!")) &&
			!(strings.Contains(message.Content, "from server state file")) {

			t := time.Now()
			fmt.Printf("[%s] [servicelb] [%s] %s%s\n", t.Format(time.RFC3339), strings.ToUpper(message.Severity.String()), message.Tag, message.Content)
		}
	}

	h.End()
}
