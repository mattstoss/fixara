package main

import (
	"errors"
	"fixara/internal/task"
	"flag"
	"log"
	"net/http"
)

type Opts struct {
	Addr     string
	CertFile string
	KeyFile  string
}

func parseOpts() (Opts, error) {
	var opts Opts

	flag.StringVar(&opts.Addr, "addr", "localhost:4000", "HTTPS network address")
	flag.StringVar(&opts.CertFile, "certfile", "cert.pem", "certificate PEM file")
	flag.StringVar(&opts.KeyFile, "keyfile", "key.pem", "key PEM file")

	flag.Parse()

	if opts.Addr == "" {
		return Opts{}, errors.New("must set --addr")
	}
	if opts.CertFile == "" {
		return Opts{}, errors.New("must set --certfile")
	}
	if opts.KeyFile == "" {
		return Opts{}, errors.New("must set --keyfile")
	}

	return opts, nil
}

func runServer() error {
	opts, err := parseOpts()
	if err != nil {
		return err
	}

	taskStore := task.NewStore()
	taskHandler := task.NewHandler(taskStore)

	log.Print("starting server on ", opts.Addr)
	return http.ListenAndServeTLS(
		opts.Addr,
		opts.CertFile,
		opts.KeyFile,
		taskHandler,
	)
}

func main() {
	err := runServer()
	if err != nil {
		log.Fatal("server failed: ", err)
	}
}
