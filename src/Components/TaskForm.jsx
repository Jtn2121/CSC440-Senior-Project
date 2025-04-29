import React, { useState, useEffect } from 'react';

function getFormattedDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}


export default function TaskForm({ addTask }) {
  const [form, setForm] = useState({
    taskName: '',
    userId: '',
    startDate: getFormattedDate(),
    endDate: '',
    template: '',
    estimatedTime: '',
  });

  const [templates, setTemplates] = useState([]);
  const [assignees, setAssignees] = useState([]);
  const [adjustedTime, setAdjustedTime] = useState(0);
  const [estimatedCompletion, setEstimatedCompletion] = useState('');
  const [riskInfo, setRiskInfo] = useState('');
  const [overrunInfo, setOverrunInfo] = useState('');

  // Fetch templates
  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const res = await fetch("http://localhost:5000/templates");
        const data = await res.json();
        setTemplates(data);
      } catch (err) {
        console.error("Failed to fetch templates", err);
      }
    };

   //  Fetch assignees
    const fetchAssignees = async () => {
      try {
        const res = await fetch("http://localhost:5000/assignees");
        const data = await res.json();
        setAssignees(data);
      } catch (err) {
        console.error("Failed to fetch assignees", err);
      }
    };

    fetchTemplates();
    fetchAssignees();
  }, []);

  // Fetch predicted time when template/user changes
  useEffect(() => {
    const predict = async () => {
      if (form.template && form.userId) {
        try {
          const res = await fetch("http://localhost:5000/predict-time", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ template: form.template, userId: form.userId })
          });
          const data = await res.json();
          if (data.predictedTime !== undefined) {
            setAdjustedTime(data.predictedTime);
          }
        } catch (err) {
          console.error("Prediction failed:", err);
        }
      }
    };
    predict();
  }, [form.template, form.userId]);

  // Auto-update Start Date every minute
  useEffect(() => {
    const interval = setInterval(() => {
      setForm(prevForm => ({
        ...prevForm,
        startDate: getFormattedDate()
      }));
    }, 60000); 

    return () => clearInterval(interval); // Cleanup interval when component unmounts
  }, []);

  useEffect(() => {
    const fetchRiskAssessment = async () => {
      if (form.startDate && form.endDate && adjustedTime) {
        try {
          const res = await fetch("http://localhost:5000/assess-risk", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              startDate: form.startDate,
              endDate: form.endDate,
              taskHours: adjustedTime,
              calculatedLength: adjustedTime
            })
          });
          const data = await res.json();
          if (data.estimatedCompletion) {
            setEstimatedCompletion(data.estimatedCompletion);
            setRiskInfo(data.risk);
            setOverrunInfo(data.overrun);
          }
        } catch (err) {
          console.error("Risk assessment failed:", err);
        }
      }
    };

    fetchRiskAssessment();
  }, [form.endDate, adjustedTime]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const task = {
      ...form,
      adjustedTime,
      estimatedCompletion,
      risk: riskInfo,
      overrun: overrunInfo,
      status: 'todo',
    };
    addTask(task);

    setForm({
      taskName: '',
      userId: '',
      startDate: getFormattedDate(),
      endDate: '',
      template: '',
      estimatedTime: '',
    });
    setAdjustedTime(0);
    setEstimatedCompletion('');
    setRiskInfo('');
    setOverrunInfo('');
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <div className = "flex flex-col items-center px-4">
      <h1 className = "text-2xl font-bold mb-4"> Task Prediction </h1>

      <form onSubmit = {handleSubmit} className="w-full max-w-md bg-white p-4 rounded shadow mb-6">
        <div className = "grid grid-cols-1 gap-4">

          {/* Task Name */}
          <div className = "flex flex-col">
            <label htmlFor = "taskName" className="text-sm font-semibold mb-1">Task Name</label>
            <input
              name = "taskName"
              id = "taskName"
              type = "text"
              value = {form.taskName}
              onChange = {handleChange}
              className = "p-2 border rounded"
              required
            />
          </div>

          {/* User ID (Gets based off assignee names in database) */}
          <div className = "flex flex-col">
            <label htmlFor = "userId" className="text-sm font-semibold mb-1">Assignee</label>
            <select
              name = "userId"
              id = "userId"
              value = {form.userId}
              onChange = {handleChange}
              className = "p-2 border rounded"
              required
            >
              <option value = ""> Select Assignee </option>
              {assignees.map((assignee) => (
              <option key = {assignee.id} value={assignee.id}>
              {assignee.name}
                </option>
               ))}

            </select>
          </div>

          {/* Template (gets based off template names in database) */}
          <div className = "flex flex-col">
            <label htmlFor = "template" className="text-sm font-semibold mb-1"> Template </label>
            <select
              name = "template"
              id = "template"
              value = {form.template}
              onChange = {handleChange}
              className = "p-2 border rounded"
              required
            >
              <option value = ""> Select Template </option>
              {templates.map((tpl) => (
                <option key = {tpl} value={tpl}>{tpl}</option>
              ))}
            </select>
          </div>

          {/* Start Date (read-only) */}
          <div className = "flex flex-col">
           <label htmlFor = "startDate" className="text-sm font-semibold mb-1"> Start Date </label>
            <input
              name = "startDate"
              id = "startDate"
              type = "datetime-local"
              value = {form.startDate}
              disabled
              className = "p-2 border rounded bg-gray-100 text-gray-600"
            />
          </div>


          {/* End Date */}
          <div className = "flex flex-col">
            <label htmlFor = "endDate" className="text-sm font-semibold mb-1">End Date</label>
            <input
              name = "endDate"
              id = "endDate"
              type = "datetime-local"
              value = {form.endDate}
              onChange = {handleChange}
              className = "p-2 border rounded w-full"
            />
          </div>

          {/* Predicted Time */}
          <div className = "flex flex-col">
            <label htmlFor = "adjustedTime" className="text-sm font-semibold mb-1"> Predicted Estimated Time (hrs) </label>
            <input
              id = "adjustedTime"
              type = "number"
              step = "0.1"
              value = {adjustedTime ? adjustedTime.toFixed(2) : ''}
              onChange={(e) => setAdjustedTime(parseFloat(e.target.value) || 0)}
              className = "p-2 border rounded bg-gray-100 text-gray-600"
            />
          </div>

          
          {/* Estimated Completion */}
          <div className = "flex flex-col">
            <label className = "text-sm font-semibold mb-1"> Estimated Completion </label>
            <input
              type = "datetime-local"
              value = {estimatedCompletion}
              readOnly
              onChange = {() => {}}
              disabled
              className = "p-2 border rounded bg-gray-100 text-gray-600"
            />
          </div>

          {/* Risk Info */}
          <div className = "flex flex-col">
            <label className = "text-sm font-semibold mb-1"> Risk </label>
            <input
              value = {riskInfo}
              readOnly
              onChange = {() => {}}
              disabled
              className = {`p-2 border rounded ${
                riskInfo.includes('Low') ? 'bg-green-100 text-green-700' :
                riskInfo.includes('Medium') ? 'bg-yellow-100 text-yellow-700' :
                riskInfo.includes('High') ? 'bg-red-100 text-red-700' :
                'bg-gray-100 text-gray-600'
              }`}
            />
          </div>

          {/* Overrun Info */}
          <div className = "flex flex-col">
            <label className = "text-sm font-semibold mb-1"> Overrun </label>
            <input
              value={overrunInfo}
              readOnly
              onChange = {() => {}}
              disabled
              className = "p-2 border rounded bg-gray-100 text-gray-600"
            />
          </div>

          <button type = "submit" className = "mt-4 bg-blue-600 text-white px-4 py-2 rounded">
            Create Task
          </button>

        </div>
      </form>
    </div>
  );
}
