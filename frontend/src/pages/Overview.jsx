import { SeverityBar, PredictionPie } from '../components/Charts.jsx';

function Overview({ alerts }) {
  const total = alerts.length;
  const critical = alerts.filter(a => a.severity === 'Critical').length;
  const high = alerts.filter(a => a.severity === 'High').length;
  const open = alerts.filter(a => a.status === 'Open').length;
  const investigating = alerts.filter(a => a.status === 'Investigating').length;

  // Recent alerts table
  const recentAlerts = [...alerts].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);

  return (
    <div>
      <h2 className="mb-4 font-mono text-sm" style={{ color: 'var(--text-muted)' }}>// DASHBOARD_OVERVIEW</h2>
      
      <div className="metric-grid">
        <div className="card">
          <div className="card-title">Total Alerts</div>
          <div className="metric-value">{total}</div>
        </div>
        <div className="card">
          <div className="card-title text-critical">Critical</div>
          <div className="metric-value text-critical">{critical}</div>
        </div>
        <div className="card">
          <div className="card-title text-high">High</div>
          <div className="metric-value text-high">{high}</div>
        </div>
        <div className="card">
          <div className="card-title">Open</div>
          <div className="metric-value">{open}</div>
        </div>
        <div className="card">
          <div className="card-title text-low">Investigating</div>
          <div className="metric-value text-low">{investigating}</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="card">
          <div className="card-title">Alert Severity Distribution</div>
          <SeverityBar alerts={alerts} />
        </div>
        <div className="card">
          <div className="card-title">Traffic Classification (Normal vs Attack)</div>
          <PredictionPie alerts={alerts} />
        </div>
      </div>

      <div className="card">
        <div className="card-title">Recent Alerts</div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Alert ID</th>
                <th>Source IP</th>
                <th>Dest IP</th>
                <th>Proto</th>
                <th>Severity</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentAlerts.map(a => (
                <tr key={a.id}>
                  <td className="font-mono text-muted">{new Date(a.timestamp).toLocaleTimeString()}</td>
                  <td className="font-mono">{a.id.substring(0, 8)}...</td>
                  <td className="font-mono">{a.source_ip}</td>
                  <td className="font-mono">{a.destination_ip}</td>
                  <td>{a.protocol}</td>
                  <td>
                    <span className={`badge badge-${a.severity.toLowerCase()}`}>{a.severity}</span>
                  </td>
                  <td>
                    <span style={{ 
                      color: a.status === 'Open' ? 'var(--color-critical)' : 
                             a.status === 'Investigating' ? 'var(--color-low)' : 'var(--text-muted)'
                    }}>{a.status}</span>
                  </td>
                </tr>
              ))}
              {recentAlerts.length === 0 && (
                <tr>
                  <td colSpan="7" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
                    No alerts found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Overview;
