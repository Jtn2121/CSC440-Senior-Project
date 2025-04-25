import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 p-4 text-white mb-4">
      <Link to="/" className="mr-4">Dashboard</Link>
      <Link to="/new-task">New Task</Link>
    </nav>
  );
}
