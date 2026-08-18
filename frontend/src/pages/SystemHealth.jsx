function SystemHealth({ isOnline, lastRefresh, error }) {
  return (
    <div>
      <h2 className="mb-4 font-mono text-sm" style={{ color: 'var(--text-muted)' }}>// SYSTEM_HEALTH</h2>
      
      <div className="card mb-4">
        <div className="card-title">Core Services</div>
        <div className="grid grid-cols-2 gap-4 mt-4 font-mono text-sm">
          <div className="flex justify-between items-center p-2" style={{ backgroundColor: 'var(--bg-main)', borderRadius: '4px' }}>
            <span className="text-muted">API Gateway</span>
            <span style={{ color: isOnline ? 'var(--color-normal)' : 'var(--color-critical)' }}>
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
          <div className="flex justify-between items-center p-2" style={{ backgroundColor: 'var(--bg-main)', borderRadius: '4px' }}>
            <span className="text-muted">ML Inference Engine</span>
            <span style={{ color: isOnline ? 'var(--color-normal)' : 'var(--color-critical)' }}>
              {isOnline ? 'ONLINE' : 'UNREACHABLE'}
            </span>
          </div>
          <div className="flex justify-between items-center p-2" style={{ backgroundColor: 'var(--bg-main)', borderRadius: '4px' }}>
            <span className="text-muted">SQLite Storage</span>
            <span style={{ color: isOnline ? 'var(--color-normal)' : 'var(--color-critical)' }}>
              {isOnline ? 'ONLINE' : 'UNREACHABLE'}
            </span>
          </div>
          <div className="flex justify-between items-center p-2" style={{ backgroundColor: 'var(--bg-main)', borderRadius: '4px' }}>
            <span className="text-muted">Polling Agent</span>
            <span className="text-normal">ACTIVE (5s)</span>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Diagnostics</div>
        <div className="font-mono text-sm text-muted">
          <div>&gt; Last successful sync: {lastRefresh ? lastRefresh.toLocaleString() : 'Never'}</div>
          <div>&gt; Backend endpoint: http://127.0.0.1:8000/alerts</div>
          <div>&gt; Proxy status: {isOnline ? 'OK' : 'FAIL'}</div>
          {error && (
            <div className="text-critical mt-2">
              &gt; ERROR: {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SystemHealth;
