package main

import (
	"fixara/internal/task"
	"log"
	"net/http"
)

func runServer() error {
	taskStore := task.NewStore()
	taskHandler := task.NewHandler(taskStore)

	log.Print("starting server...")
	return http.ListenAndServe("localhost:5050", taskHandler)
}

func main() {
	err := runServer()
	if err != nil {
		log.Fatal("server failed: ", err)
	}
}
