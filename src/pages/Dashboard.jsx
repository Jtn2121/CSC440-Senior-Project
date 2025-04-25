import React, { useState } from "react";
import TaskForm from "../components/TaskForm";
import TaskTable from "../components/TaskTable";

export default function Dashboard() {
  const [tasks, setTasks] = useState(() => {
    const stored = localStorage.getItem("tasks");
    return stored ? JSON.parse(stored) : [];
});
  
  const addTask = (task) => {
    const newTask = {...task, id: crypto.randomUUID() };
    const updated = [...tasks, newTask ];
    setTasks(updated);
    localStorage.setItem("tasks", JSON.stringify(updated));
  };

  const deleteTask = (id) => {
    const updated = tasks.filter((t) => t.id !== id);
    setTasks(updated);
    localStorage.setItem("tasks", JSON.stringify(updated));
  };

  return (
    <div className = "flex flex-col px-6"> 
      <h1 className = "text-2xl font-bold mb-4">  </h1> 
      <TaskForm addTask = {addTask} />
      <TaskTable tasks = {tasks} deleteTask = {deleteTask} />
    </div>
  );
}
