import { useState, useEffect, useCallback } from 'react';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import Overview from './pages/Overview.jsx';
import AlertsPage from './pages/Alerts.jsx';
import Monitoring from './pages/Monitoring.jsx';
import SystemHealth from './pages/SystemHealth.jsx';
import { fetchAlerts } from './api.js';

function App() {
  const [currentPage, setCurrentPage] = useState('overview');
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(null);
  const [isBackendOnline, setIsBackendOnline] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const data = await fetchAlerts();
      setAlerts(data);
      setLastRefresh(new Date());
      setIsBackendOnline(true);
      setError(null);
    } catch (err) {
      setError(err.message);
      setIsBackendOnline(false);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load and polling
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [loadData]);

  // Handle status update locally to avoid waiting for next poll
  const handleStatusUpdate = (id, newStatus) => {
    setAlerts(prev => prev.map(a => a.id === id ? { ...a, status: newStatus } : a));
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return <Overview alerts={alerts} />;
      case 'alerts':
      case 'investigations':
        return <AlertsPage alerts={alerts} onStatusUpdate={handleStatusUpdate} />;
      case 'monitoring':
        return <Monitoring alerts={alerts} />;
      case 'system_health':
        return <SystemHealth isOnline={isBackendOnline} lastRefresh={lastRefresh} error={error} />;
      default:
        return <Overview alerts={alerts} />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      <div className="main-content">
        <Header lastRefresh={lastRefresh} isOnline={isBackendOnline} />
        {error && (
          <div style={{ padding: '0 24px', marginTop: '16px' }}>
            <div className="error-banner">
              <strong>Backend Unavailable:</strong> {error}
            </div>
          </div>
        )}
        <div className="page-content">
          {loading && alerts.length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>Loading security data...</div>
          ) : (
            renderPage()
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
