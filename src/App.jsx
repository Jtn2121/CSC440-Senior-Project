import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import TaskDetail from "./pages/TaskDetail";
import TaskForm from "./components/TaskForm";
// import Navbar from "./components/Navbar"; // Uncomment if you have a Navbar

export default function App() {
  return (
    
    <Router>
      {/* <Navbar /> */}
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/task/:id" element={<TaskDetail />} />
          <Route path="/new-task" element={<TaskForm />} />
        </Routes>
      </main>
    </Router>
  );

  
}
