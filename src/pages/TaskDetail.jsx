import React from "react";
import { useParams } from "react-router-dom";

export default function TaskDetail() {
  const { id } = useParams();
  const tasks = JSON.parse(localStorage.getItem("tasks") || "[]");
  const task = tasks.find((t) => t.id === id);

  if (!task) return <p>Task not found</p>;

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">{task.taskName}</h2>
      <p className="text-gray-700">Template: {task.template}</p>
      <p className="text-gray-700">Priority: {task.priority}</p>
      <p className="text-gray-700">Estimated Time: {task.adjustedTime} hrs</p>
      <p className="text-gray-700">Due: {new Date(task.endDate).toLocaleString()}</p>
      
    </div>
  );
}
