import React, { useState, useEffect } from "react";
import TaskForm from "../components/TaskForm";
import TaskTable from "../components/TaskTable";

export default function Dashboard() {
  const [tasks, setTasks] = useState(() => {
    const stored = localStorage.getItem("tasks");
    return stored ? JSON.parse(stored) : [];
  });

  const [assignees, setAssignees] = useState([]);
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    const fetchAssignees = async () => {
      try {
        const res = await fetch("http://localhost:5000/assignees");
        const data = await res.json();
        setAssignees(data);
      } catch (err) {
        console.error("Failed to fetch assignees", err);
      }
    };

    const fetchTemplates = async () => {
      try {
        const res = await fetch("http://localhost:5000/templates");
        const data = await res.json();
        setTemplates(data);
      } catch (err) {
        console.error("Failed to fetch templates", err);
      }
    };

    fetchAssignees();
    fetchTemplates();
  }, []);

  const addTask = (task) => {
    const newTask = { ...task, id: crypto.randomUUID() };
    const updated = [...tasks, newTask];
    setTasks(updated);
    localStorage.setItem("tasks", JSON.stringify(updated));
  };

  const deleteTask = (id) => {
    const updated = tasks.filter((t) => t.id !== id);
    setTasks(updated);
    localStorage.setItem("tasks", JSON.stringify(updated));
  };

  return (
    <div className="flex flex-col px-6">
      <h1 className="text-2xl font-bold mb-4"> </h1>
      <TaskForm addTask={addTask} assignees={assignees} templates={templates} />
      <TaskTable tasks={tasks} deleteTask={deleteTask} assignees={assignees} />
    </div>
  );
}
