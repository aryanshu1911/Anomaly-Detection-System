import { useState } from 'react';
import AlertModal from '../components/AlertModal.jsx';

function AlertsPage({ alerts, onStatusUpdate }) {
  const [filterSeverity, setFilterSeverity] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [searchIP, setSearchIP] = useState('');
  const [selectedAlert, setSelectedAlert] = useState(null);

  // Client-side filtering
  const filteredAlerts = alerts.filter(a => {
    if (filterSeverity && a.severity !== filterSeverity) return false;
    if (filterStatus && a.status !== filterStatus) return false;
    if (searchIP && !a.source_ip.includes(searchIP) && !a.destination_ip.includes(searchIP)) return false;
    return true;
  }).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return (
    <div>
      <h2 className="mb-4 font-mono text-sm" style={{ color: 'var(--text-muted)' }}>// ALERT_MANAGEMENT</h2>
      
      <div className="card mb-4">
        <div className="flex gap-4 items-center">
          <input 
            type="text" 
            placeholder="Search IP..." 
            value={searchIP}
            onChange={(e) => setSearchIP(e.target.value)}
            style={{ flex: 1 }}
          />
          <select value={filterSeverity} onChange={(e) => setFilterSeverity(e.target.value)}>
            <option value="">All Severities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="">All Statuses</option>
            <option value="Open">Open</option>
            <option value="Acknowledged">Acknowledged</option>
            <option value="Investigating">Investigating</option>
            <option value="Resolved">Resolved</option>
            <option value="False Positive">False Positive</option>
          </select>
          <div className="text-muted text-sm font-mono">
            {filteredAlerts.length} RESULT(S)
          </div>
        </div>
      </div>

      <div className="card">
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Alert ID</th>
                <th>Source IP</th>
                <th>Dest IP</th>
                <th>Proto</th>
                <th>Bytes</th>
                <th>Risk Score</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredAlerts.map(a => (
                <tr key={a.id}>
                  <td className="font-mono text-muted">{new Date(a.timestamp).toLocaleString()}</td>
                  <td className="font-mono text-sm">{a.id.substring(0, 8)}</td>
                  <td className="font-mono">{a.source_ip}</td>
                  <td className="font-mono">{a.destination_ip}</td>
                  <td className="font-mono">{a.protocol}</td>
                  <td className="font-mono text-muted">{a.total_bytes}</td>
                  <td className="font-mono">{a.risk_score.toFixed(2)}</td>
                  <td>
                    <span className={`badge badge-${a.severity.toLowerCase()}`}>{a.severity}</span>
                  </td>
                  <td>
                    <span style={{ 
                      color: a.status === 'Open' ? 'var(--color-critical)' : 
                             a.status === 'Investigating' ? 'var(--color-low)' : 'var(--text-muted)'
                    }}>{a.status}</span>
                  </td>
                  <td>
                    <button className="btn" onClick={() => setSelectedAlert(a)}>Investigate</button>
                  </td>
                </tr>
              ))}
              {filteredAlerts.length === 0 && (
                <tr>
                  <td colSpan="10" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
                    No alerts match filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {selectedAlert && (
        <AlertModal 
          alert={selectedAlert} 
          onClose={() => setSelectedAlert(null)} 
          onStatusUpdate={onStatusUpdate}
        />
      )}
    </div>
  );
}

export default AlertsPage;
