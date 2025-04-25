import React from "react";
import { Link } from "react-router-dom";

export default function TaskTable({ tasks, deleteTask }) {
  return (
    <div className = "mt-6">
      <h2 className = "text-xl font-bold mb-2"> Tasks </h2>
      <ul className = "space-y-4">
        {tasks.map((task) => (
          <li key = {task.id} className = "bg-white p-4 rounded shadow space-y-1">
            <p className = "font-semibold text-blue-600 text-lg">
              {task.taskName}
            </p>

            <p className = "text-sm text-gray-600">
              {task.template} • Estimated Time <strong>{task.adjustedTime?.toFixed(1)} hrs</strong>
            </p>

            <p className="text-sm text-gray-500">
              Assigned to: {Array.isArray(task.userId) ? task.userId.join(", ") : task.userId}
            </p>

            <p className="text-sm text-gray-500">
            Start Date: {new Date(task.startDate).toLocaleString()}
            </p>

            <p className = "text-sm text-gray-800">
              Due by: {new Date(task.endDate).toLocaleString()}
            </p>
       
          <button 
            onClick = {() => deleteTask(task.id)}
            className = "text-sm text-red-500 hover: underline"> Delete 
          </button>


            <div className = "flex gap-2 mt-1 items-center">
              <span
                className = {`text-xs font-semibold px-2 py-1 rounded-full ${
                  task.priority === 'High'
                    ? 'bg-red-200 text-red-800'
                    : task.priority === 'Medium'
                    ? 'bg-yellow-200 text-yellow-800'
                    : 'bg-green-200 text-green-800'
                }`}
              >
                {task.priority}
              </span>
              <span className = "text-xs uppercase bg-gray-100 text-gray-600 px-2 py-1 rounded">
                {task.status}
              </span>
            </div>
            {task.risk?.text && (
              <p className = "text-xs mt-1 text-white px-2 py-1 rounded" style = {{ backgroundColor: task.risk.color }}>
                Risk: {task.risk.text}
              </p>
            )}
            {task.overrun?.text && (
              <p className = "text-xs mt-1 text-white px-2 py-1 rounded" style = {{ backgroundColor: task.overrun.color }}>
                Overrun: {task.overrun.text}
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
