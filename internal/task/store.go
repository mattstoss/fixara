package task

import (
	"fmt"
	"sort"
)

type TaskStore interface {
	CreateTask(title string) Task
	GetTaskById(id int) (Task, error)
	GetAllTasks() []Task
	DeleteTaskById(id int) error
	DeleteAllTasks()
}

func NewStore() TaskStore {
	return &store{
		tasks:  make(map[int]Task),
		nextId: 0,
	}
}

type store struct {
	tasks  map[int]Task
	nextId int
}

func (s *store) CreateTask(title string) Task {
	task := Task{s.nextId, title}
	s.nextId = s.nextId + 1
	s.tasks[task.Id] = task
	return task
}

func (s *store) GetAllTasks() []Task {
	tasks := make([]Task, 0)
	for _, t := range s.tasks {
		tasks = append(tasks, t)
	}
	sort.Slice(tasks, func(i, j int) bool {
		return tasks[i].Id < tasks[j].Id
	})
	return tasks
}

func (s *store) GetTaskById(id int) (Task, error) {
	task, exists := s.tasks[id]
	if !exists {
		return Task{}, fmt.Errorf("GetTask(id=%d) failed: not found", id)
	}
	return task, nil
}

func (s *store) DeleteTaskById(id int) error {
	_, exists := s.tasks[id]
	if !exists {
		return fmt.Errorf("DeleteTask(id=%d) failed: not found", id)
	}
	delete(s.tasks, id)
	return nil
}

func (s *store) DeleteAllTasks() {
	s.tasks = make(map[int]Task)
}
