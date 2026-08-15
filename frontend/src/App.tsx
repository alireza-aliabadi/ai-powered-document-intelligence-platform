import "./App.css";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true" />
          <div className="brand-copy">
            <p className="brand-name">DocuMind</p>
            <p className="brand-tag">Document Intelligence Platform</p>
          </div>
        </div>
        <p className="header-status">
          <span className="status-dot" aria-hidden="true" />
          Workspace ready
        </p>
      </header>
      <Dashboard />
    </div>
  );
}
