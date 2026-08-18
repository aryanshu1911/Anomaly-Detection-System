function Sidebar({ currentPage, onNavigate }) {
  const navItems = [
    { id: 'overview', label: 'Overview' },
    { id: 'alerts', label: 'Alerts' },
    { id: 'investigations', label: 'Investigations' },
    { id: 'monitoring', label: 'Monitoring' },
    { id: 'system_health', label: 'System Health' },
  ];

  return (
    <div className="sidebar">
      <div style={{ padding: '24px', borderBottom: '1px solid var(--border-color)', marginBottom: '16px' }}>
        <h1 style={{ fontSize: '18px', fontWeight: '700', letterSpacing: '0.05em', margin: 0 }}>
          SENTINEL<span className="text-low">AI</span>
        </h1>
        <div className="text-muted text-sm mt-4 font-mono">
          SOC CONSOLE v1.0
        </div>
      </div>
      
      <nav style={{ flex: 1 }}>
        <ul style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          {navItems.map(item => (
            <li key={item.id}>
              <button
                className={`nav-item w-full ${currentPage === item.id ? 'active' : ''}`}
                style={{ width: '100%', textAlign: 'left' }}
                onClick={() => onNavigate(item.id)}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      
      <div style={{ padding: '24px', borderTop: '1px solid var(--border-color)', fontSize: '11px' }} className="text-muted font-mono">
        <div>USER: ANALYST-01</div>
        <div>ROLE: TIER 2 SOC</div>
      </div>
    </div>
  );
}

export default Sidebar;
