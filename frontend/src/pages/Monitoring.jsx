import { PredictionPie } from '../components/Charts.jsx';

function Monitoring({ alerts }) {
  // A simulated live feed of the last 20 network flows
  const recentFlows = [...alerts].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 20);
  
  const bytesInLastHour = alerts.reduce((acc, a) => acc + a.total_bytes, 0);
  const packetsInLastHour = alerts.reduce((acc, a) => acc + a.total_packets, 0);

  return (
    <div>
      <h2 className="mb-4 font-mono text-sm" style={{ color: 'var(--text-muted)' }}>// LIVE_MONITORING</h2>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="card">
          <div className="card-title">Telemetry Volume (Total captured)</div>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div>
              <div className="text-sm text-muted">Total Bytes</div>
              <div className="font-mono text-lg">{bytesInLastHour.toLocaleString()} B</div>
            </div>
            <div>
              <div className="text-sm text-muted">Total Packets</div>
              <div className="font-mono text-lg">{packetsInLastHour.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-sm text-muted">Events Processed</div>
              <div className="font-mono text-lg">{alerts.length}</div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-title">Traffic Classification</div>
          <PredictionPie alerts={alerts} />
        </div>
      </div>

      <div className="card">
        <div className="card-title flex items-center gap-2">
          <div className="pulse"></div> Live Telemetry Stream
        </div>
        <div className="table-container" style={{ maxHeight: '400px' }}>
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Source</th>
                <th>Destination</th>
                <th>Proto</th>
                <th>Bytes</th>
                <th>Classification</th>
              </tr>
            </thead>
            <tbody>
              {recentFlows.map((flow, idx) => (
                <tr key={`${flow.id}-${idx}`} className={idx === 0 ? 'flash' : ''}>
                  <td className="font-mono text-muted">{new Date(flow.timestamp).toISOString()}</td>
                  <td className="font-mono">{flow.source_ip}:{flow.source_port}</td>
                  <td className="font-mono">{flow.destination_ip}:{flow.destination_port}</td>
                  <td>{flow.protocol}</td>
                  <td className="font-mono text-muted">{flow.total_bytes}</td>
                  <td>
                    <span style={{ color: flow.prediction === 1 ? 'var(--color-critical)' : 'var(--color-normal)' }}>
                      {flow.prediction === 1 ? 'ATTACK' : 'NORMAL'}
                    </span>
                  </td>
                </tr>
              ))}
              {recentFlows.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
                    Waiting for telemetry...
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

export default Monitoring;
