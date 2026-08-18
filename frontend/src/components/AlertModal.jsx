import { useState } from 'react';
import { patchAlertStatus } from '../api.js';

function AlertModal({ alert, onClose, onStatusUpdate }) {
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState(null);

  const handleStatusChange = async (newStatus) => {
    setUpdating(true);
    setError(null);
    try {
      await patchAlertStatus(alert.id, newStatus);
      onStatusUpdate(alert.id, newStatus);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="font-mono font-bold">
            INVESTIGATION: <span className="text-muted">{alert.id}</span>
          </div>
          <button onClick={onClose} className="text-muted" style={{ fontSize: '16px' }}>&times;</button>
        </div>
        
        <div className="modal-body" style={{ flex: 1, overflowY: 'auto' }}>
          {error && (
            <div className="error-banner">{error}</div>
          )}
          
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="card">
              <div className="card-title">Network Flow</div>
              <div className="grid grid-cols-2 gap-2 text-sm font-mono">
                <div className="text-muted">Source IP</div><div>{alert.source_ip}</div>
                <div className="text-muted">Source Port</div><div>{alert.source_port}</div>
                <div className="text-muted">Dest IP</div><div>{alert.destination_ip}</div>
                <div className="text-muted">Dest Port</div><div>{alert.destination_port}</div>
                <div className="text-muted">Protocol</div><div>{alert.protocol}</div>
                <div className="text-muted">Total Bytes</div><div>{alert.total_bytes}</div>
                <div className="text-muted">Packets</div><div>{alert.total_packets}</div>
              </div>
            </div>
            
            <div className="card">
              <div className="card-title">Risk Assessment</div>
              <div className="grid grid-cols-2 gap-2 text-sm font-mono mb-4">
                <div className="text-muted">Severity</div>
                <div><span className={`badge badge-${alert.severity.toLowerCase()}`}>{alert.severity}</span></div>
                <div className="text-muted">Risk Score</div>
                <div style={{ color: alert.risk_score > 75 ? 'var(--color-critical)' : 'inherit' }}>{alert.risk_score.toFixed(2)} / 100</div>
                <div className="text-muted">ML Prediction</div>
                <div>{alert.prediction === 1 ? 'Attack' : 'Normal'}</div>
              </div>
              <div className="card-title" style={{ marginTop: '16px' }}>Reasoning</div>
              <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                {alert.reason || 'Network telemetry indicates anomalous behavior matching known attack signatures or significant deviation from baseline.'}
              </div>
            </div>
          </div>

          <div className="card mb-4" style={{ backgroundColor: 'rgba(239, 68, 68, 0.05)', borderColor: 'rgba(239, 68, 68, 0.2)' }}>
            <div className="card-title text-critical">Recommended Actions</div>
            <ul className="text-sm gap-2 flex" style={{ flexDirection: 'column', color: 'var(--text-primary)' }}>
              <li>1. Isolate endpoint {alert.source_ip} from internal network.</li>
              <li>2. Verify if destination {alert.destination_ip} holds sensitive data.</li>
              <li>3. Check host-based logs (EDR/Sysmon) for anomalous processes.</li>
              <li>4. Mark status below based on investigation outcome.</li>
            </ul>
          </div>
        </div>

        <div className="modal-footer" style={{ justifyContent: 'space-between' }}>
          <div className="text-sm font-mono text-muted flex items-center">
            CURRENT STATUS: <span style={{ color: 'var(--text-primary)', marginLeft: '8px' }}>{alert.status}</span>
          </div>
          <div className="flex gap-2">
            <button className="btn" disabled={updating} onClick={() => handleStatusChange('Investigating')}>
              Investigating
            </button>
            <button className="btn" disabled={updating} onClick={() => handleStatusChange('False Positive')}>
              False Positive
            </button>
            <button className="btn btn-primary" disabled={updating} onClick={() => handleStatusChange('Resolved')}>
              Mark Resolved
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AlertModal;
