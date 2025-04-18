import React, { useState } from "react";
import Datetime from 'react-datetime';

function App() {
  const [userId, setUserId] = useState("");
  const [taskName, setTaskName] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [manHours, setManHours] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [timeTotal, setTimeTotal] = useState("");

  const categories = [
    "Check Server Logs",
    "System Update",
    "Code Review",
    "User Testing",
    "Debugging",
    "Coding",
    "Software Maintenance"
  ];

  const Assignee = [
    "1",
    "2",
    "3",
    "4",
    "5"
  ];

  const statuses = [
    "New",
    "In Progress",
    "Complete"
  ];

  // shows what user inputs
  const handleSubmit = (e) => {
    e.preventDefault();
alert(`User ID: ${userId}\n Task: ${taskName}\n Category: ${selectedCategory}
\n Estimated Man Hours: ${manHours} \n Variable 2: ${dueDate}\n Time Total in Progress: ${timeTotal}`);


  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Create Task</h1>
      <form onSubmit={handleSubmit} style={{ display: "inline-block", textAlign: "left" }}>

     {/* Assignee Input */}
  <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
  <label style={{ width: "150px", fontWeight: "bold" }}>Assignee:</label>
  <select
    value={userId}
    onChange={(e) => setUserId(e.target.value)}
    style={{ flex: "1", padding: "5px" }}
  >
    <option value="">-- Select Assignee --</option>
    {Assignee.map((id) => (
      <option key={id} value={id}>
        {id}
      </option>
    ))}
  </select>
</div>

      {/* Task Name Input */}
      <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style={{ width: "150px", fontWeight: "bold" }}>Task Name:</label>
          <input
            type="text"
            value={taskName}
            onChange={(e) => setTaskName(e.target.value)}
            style={{ flex: "1", padding: "5px" }}
          />
        </div>

        {/* Task Category Dropdown */}
        <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style={{ width: "150px", fontWeight: "bold" }}>Task Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{ flex: "1", padding: "5px" }}
          >
            <option value="">-- Select a Category --</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
        {/* Not sure if needed since we are inputing this into database. Would be more frontend/not our worry*/}
        {/* Status Dropdown */}
        <div style = {{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style = {{ width: "150px", fontWeight: "bold" }}>Status:</label>
          <select
            value = {selectedStatus}
            onChange = {(e) => setSelectedStatus(e.target.value)}
            style = {{ flex: "1", padding: "5px" }} >
            <option value="">-- Select a Status --</option>
            {statuses.map((Status) => (
              <option key = {Status} value = {Status}>
                {Status} 
              </option>
            ))}
          </select>
        </div>

        {/* Estimated Man Hours Input */}
     <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style={{ width: "150px", fontWeight: "bold" }}>Estimated Man Hours:</label>
          <input
            type = "number"
            value = {manHours}
            onChange={(e) => setManHours(e.target.value)}
            style={{ flex: "1", padding: "5px" }}
          />
        </div>

          {/* Variable 2 Input */}
     <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style={{ width: "150px", fontWeight: "bold" }}>Due Date:</label>
          <input
            type = "Date"
            value = {dueDate}
            onChange = {(e) => setDueDate(e.target.value)}
            style={{ flex: "1", padding: "5px" }}
          />
        </div>

          {/* Total Time In Progress Input */}
     <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
          <label style={{ width: "150px", fontWeight: "bold" }}>Total Time in Progress:</label>
          <input
            type = "number"
            value = {timeTotal}
            onChange={(e) => setTimeTotal(e.target.value)}
            style={{ flex: "1", padding: "5px" }}
          />
        </div>


        {/* Submit Button */}
        <div style={{ textAlign: "right", marginTop: "10px" }}>
          <button type="submit" style={{ padding: "1px 20px", fontSize: "16px" }}>Submit</button>
        </div>
      </form>
    </div>
  );
}

export default App;
