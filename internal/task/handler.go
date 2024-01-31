package task

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
)

func NewHandler(ts TaskStore) func(http.ResponseWriter, *http.Request) {
	h := handler{store: ts}
	return func(w http.ResponseWriter, r *http.Request) {
		h.routeAndHandleRequest(w, r)
	}
}

type handler struct {
	store TaskStore
}

func (h *handler) routeAndHandleRequest(w http.ResponseWriter, r *http.Request) {
	isAllowed := strings.HasPrefix(r.URL.Path, "/task/")
	if !isAllowed {
		sendJSONError(w, fmt.Sprintf("Expects /task/, got %s", r.URL.Path), http.StatusInternalServerError)
		return
	}

	path := strings.Trim(r.URL.Path, "/")
	parts := strings.Split(path, "/")

	if len(parts) == 1 {
		h.routeBasePath(w, r)
	} else if len(parts) == 2 {
		h.routeTaskById(w, r, parts[1])
	} else {
		sendJSONError(w, "Invalid path format", http.StatusBadRequest)
	}
}

func (h *handler) routeBasePath(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		h.getAllTasksHandler(w, r)
	case http.MethodPost:
		h.createTaskHandler(w, r)
	case http.MethodDelete:
		h.deleteAllTasksHandler(w, r)
	default:
		sendJSONError(w, fmt.Sprintf("Expect method GET, DELETE, or POST at /task/, got %v", r.Method), http.StatusMethodNotAllowed)
	}
}

func (h *handler) routeTaskById(w http.ResponseWriter, r *http.Request, idStr string) {
	id, err := strconv.Atoi(idStr)
	if err != nil {
		sendJSONError(w, "Invalid task ID", http.StatusBadRequest)
		return
	}

	switch r.Method {
	case http.MethodGet:
		h.getTaskByIdHandler(w, r, id)
	case http.MethodDelete:
		h.deleteTaskByIdHandler(w, r, id)
	default:
		sendJSONError(w, fmt.Sprintf("Expect method GET or DELETE at /task/<id>, got %v", r.Method), http.StatusMethodNotAllowed)
	}
}

func (h *handler) getTaskByIdHandler(w http.ResponseWriter, r *http.Request, id int) {
	task, err := h.store.GetTaskById(id)
	if err != nil {
		log.Printf("Error getting task by ID: %v", err)
		sendJSONError(w, "Task not found", http.StatusNotFound)
		return
	}

	sendJSONResponse(w, task, http.StatusOK)
}

func (h *handler) getAllTasksHandler(w http.ResponseWriter, r *http.Request) {
	tasks := h.store.GetAllTasks()
	sendJSONResponse(w, tasks, http.StatusOK)
}

func (h *handler) deleteTaskByIdHandler(w http.ResponseWriter, r *http.Request, id int) {
	err := h.store.DeleteTaskById(id)
	if err != nil {
		log.Printf("Error deleting task by ID: %v", err)
		sendJSONError(w, "Task not found", http.StatusNotFound)
		return
	}

	sendJSONResponse(w, map[string]string{"message": "Task successfully deleted"}, http.StatusOK)
}

func (h *handler) deleteAllTasksHandler(w http.ResponseWriter, r *http.Request) {
	h.store.DeleteAllTasks()
	sendJSONResponse(w, map[string]string{"message": "All tasks successfully deleted"}, http.StatusOK)
}

func (h *handler) createTaskHandler(w http.ResponseWriter, r *http.Request) {
	var task Task
	if r.Header.Get("Content-Type") != "application/json" {
		sendJSONError(w, "Content-Type is not application/json", http.StatusUnsupportedMediaType)
		return
	}

	if err := json.NewDecoder(r.Body).Decode(&task); err != nil {
		log.Printf("Error decoding task: %v", err)
		sendJSONError(w, "Failed to decode task", http.StatusBadRequest)
		return
	}

	createdTask := h.store.CreateTask(task.Title)
	sendJSONResponse(w, createdTask, http.StatusCreated)
}

func sendJSONError(w http.ResponseWriter, message string, statusCode int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(map[string]string{"error": message})
}

func sendJSONResponse(w http.ResponseWriter, data interface{}, statusCode int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Printf("Error encoding response: %v", err)
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(map[string]string{"error": "Error encoding response"})
	}
}
