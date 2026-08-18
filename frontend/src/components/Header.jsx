function Header({ lastRefresh, isOnline }) {
  const formatTime = (date) => {
    if (!date) return 'Waiting...';
    return date.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <header className="header">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          {isOnline ? <div className="pulse"></div> : <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: 'var(--color-critical)' }}></div>}
          <span className="font-mono text-sm" style={{ color: isOnline ? 'var(--color-normal)' : 'var(--color-critical)' }}>
            {isOnline ? 'SYSTEM ONLINE' : 'SYSTEM OFFLINE'}
          </span>
        </div>
        <div className="text-muted text-sm font-mono" style={{ borderLeft: '1px solid var(--border-color)', paddingLeft: '16px' }}>
          MONITORING ACTIVE
        </div>
      </div>
      
      <div className="flex items-center gap-4 text-sm font-mono text-muted">
        <div>
          LAST REFRESH: {formatTime(lastRefresh)}
        </div>
      </div>
    </header>
  );
}

export default Header;
