import React from "react";

export default function TaskTable({ tasks, deleteTask, assignees }) {
  return (
    <div className = "mt-6">
      <h2 className = "text-xl font-bold mb-2">Tasks</h2>
      <ul className = "space-y-4">
        {tasks.map((task) => (
          <li key = {task.id} className = "bg-white p-4 rounded shadow space-y-1">
            
            {/* Task Name */}
            <p className = "font-semibold text-blue-600 text-lg">
              {task.taskName}
            </p>

            {/* Template and Estimated Time */}
            <p className = "text-sm text-gray-600">
              {task.template} • Estimated Time: <strong>{task.adjustedTime?.toFixed(1)} hrs</strong>
            </p>

            {/* Assigned To (Show Employee Name, not UUID) */}
            <p className="text-sm text-gray-500">
              Assigned to: {assignees.find(a => a.id === task.userId)?.name || task.userId}
            </p>

            {/* Start Date */}
            <p className="text-sm text-gray-500">
              Start Date: {task.startDate ? new Date(task.startDate).toLocaleString() : "N/A"}
            </p>

            {/* Due Date (End Date) */}
            <p className="text-sm text-gray-500">
              Due by: {task.endDate ? new Date(task.endDate).toLocaleString() : "N/A"}
            </p>

            {/* Estimated Completion */}
            <p className="text-sm text-gray-500">
              Estimated Completion: {task.estimatedCompletion ? new Date(task.estimatedCompletion).toLocaleString() : "N/A"}
            </p>

            {/* Risk */}
            <p className = {`text-sm font-semibold ${
              task.risk?.includes("Low") ? "text-green-600" :
              task.risk?.includes("Medium") ? "text-yellow-600" :
              task.risk?.includes("High") ? "text-red-600" :
              "text-gray-600"
            }`}>
              Risk: {task.risk || "N/A"}
            </p>

            {/* Overrun */}
            <p className = "text-sm text-gray-600">
              Overrun: {task.overrun || "N/A"}
            </p>

            {/* Delete Button */}
            <button
              onClick={() => deleteTask(task.id)}
              className = "text-sm text-red-500 hover:underline mt-2"
            >
              Delete
            </button>

          </li>
        ))}
      </ul>
    </div>
  );
}
