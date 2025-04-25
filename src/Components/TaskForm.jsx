import React, { useState, useEffect } from 'react';

export default function TaskForm({ addTask }) {
  const [form, setForm] = useState({
    taskName: '',
    userId: [],
    startDate: new Date().toISOString(),
    endDate: '',
    template: '',
    estimatedTime: '',
    priority: 'Medium',
  });

  const [adjustedTime, setAdjustedTime] = useState(0);
  const [riskInfo, setRiskInfo] = useState(null);
  const [overrunInfo, setOverrunInfo] = useState(null);
  const [estimatedCompletion, setEstimatedCompletion] = useState(null);

  

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const task = {
      ...form,
      adjustedTime,
      estimatedCompletion: estimatedCompletion?.toISOString(),
      status: 'todo',
      risk: riskInfo,
      overrun: overrunInfo,
    };
    addTask(task);

    setForm({
      taskName: '',
      userId: [],
      startDate: new Date().toISOString(),
      endDate: '',
      template: '',
      estimatedTime: '',
      priority: 'Medium',
    });
    setRiskInfo(null);
    setOverrunInfo(null);
    setEstimatedCompletion(null);
  };

  return (
    <div className="flex flex-col items-center px-4">

      <h1 className="text-2xl font-bold mb-4 text-center w-full max-w-md">Task Prediction</h1>

      <form onSubmit = {handleSubmit} className = "w-full max-w-md bg-white p-4 rounded shadow mb-6">
        <div className = "grid grid-cols-1 gap-4">

          {/* Task Name */}
          <div className="flex flex-col w-full max-w-sm">
            <label htmlFor = "taskName" className = "text-sm font-semibold mb-1"> Task Name </label>
            <input
              name = "taskName"
              id = "taskName"
              type = "text"
              value = {form.taskName}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
              required
            />
          </div>

           {/* User ID */}
           <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "userId" className = "text-sm font-semibold mb-1"> User ID </label>
            <select
              name = "userId"
              id = "userId"
              value = {form.userId}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
              required
            >
              <option value = "">Select User ID</option>
              <option value = "01">01</option>
              <option value = "02">02</option>
              <option value = "03">03</option>
              <option value = "04">04</option>
              <option value = "05">05</option>
            </select>
          </div>

          {/* Template */}
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "template" className="text-sm font-semibold mb-1">Template</label>
            <select
              name = "template"
              id = "template"
              value = {form.template}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
              required
            >
              <option value = ""> Select Template </option>
              <option value = "Check Server Logs"> Check Server Logs </option>
              <option value = "System Update"> System Update </option>
              <option value = "Code Review"> Code Review </option>
              <option value = "User Testing"> User Testing</option>
              <option value = "Debugging"> Debugging </option>
              <option value = "Coding"> Coding </option>
              <option value = "Software maintenance"> Software maintenance </option>
              <option value = "Data Scrubbing"> Data Scrubbing </option>
              <option value = "Analytics Monitoring"> Analytics Monitoring </option>
              <option value = "Meeting Planning"> Meeting Planning </option>
              <option value = "Documentation"> Documentation </option>
              <option value = "Database Management"> Database Management </option>
              <option value = "Database Auditing"> Database Auditing </option>
              <option value = "Aircraft Induction"> Aircraft Induction </option>
              <option value = "Deployment"> Deployment </option>
            </select>
          </div>

         {/*
          // Start Date (autopopulated when task is created)
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "startDate" className="text-sm font-semibold mb-1">Start Date</label>
            <input
              name = "startDate"
              id = "startDate"
              type="datetime-local"
              value = {form.startDate}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
              required
            />
          </div>
          */}

          {/* End Date (includes time)*/}
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "endDate" className="text-sm font-semibold mb-1">End Date</label>
            <input
              name = "endDate"
              id = "endDate"
              type="datetime-local"
              value = {form.endDate}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
            />
          </div>

          {/* Estimated Time */}
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "estimatedTime" className="text-sm font-semibold mb-1"> Estimated Time (hrs) </label>
            <input
              name = "estimatedTime"
              id = "estimatedTime"
              type = "number"
              step = "0.1"
              value = {form.estimatedTime}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
              required
            />
          </div>

          {/* Priority */}
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "priority" className="text-sm font-semibold mb-1"> Priority </label>
            <select
              name = "priority"
              id = "priority"
              value = {form.priority}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
            >
              <option> High </option>
              <option> Medium </option>
              <option> Low </option>
            </select>
          </div>

          {/* Adjusted Time */}
          <div className = "flex flex-col w-full max-w-sm">
            <label htmlFor = "adjustedTime" className="text-sm font-semibold mb-1"> Generated Estimated Time (hrs) </label>
            <input
              id = "adjustedTime"
              disabled
              value = {adjustedTime.toFixed(1)}
              className = "p-2 border rounded bg-gray-100 text-gray-600 w-full"
            />
          </div>
        </div>

        {/* Risk/Overrun Output */}
        <div className = "mt-4 space-y-2">
          {estimatedCompletion && (
            <div className = "text-sm text-gray-700">
              Estimated Completion: <strong>{new Date(estimatedCompletion).toLocaleString()}</strong>
            </div>
          )}
          {riskInfo && (
            <div className = "text-sm font-bold text-white p-2 rounded" style = {{ backgroundColor: riskInfo.color }}>
              Risk: {riskInfo.text}
            </div>
          )}
          {overrunInfo && (
            <div className = "text-sm font-bold text-white p-2 rounded" style = {{ backgroundColor: overrunInfo.color }}>
              Overrun: {overrunInfo.text}
            </div>
          )}
        </div>

        <button type = "submit" className = "mt-4 bg-blue-600 text-white px-4 py-2 rounded">
          Create Task
        </button>
      </form>
    </div>
  );
}