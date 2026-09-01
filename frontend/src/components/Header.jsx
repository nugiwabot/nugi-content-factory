import React from 'react';
import { Sparkles, Settings as SettingsIcon, Activity } from 'lucide-react';

export default function Header({ projects, currentProject, setCurrentProject, onOpenSettings, onQuickGenerate, healthStatus }) {
  return (
    <header className="top-navbar">
      <div className="brand-title-box">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <img 
            src="/nugi_properti_logo.png" 
            alt="NUGIPROPERTI Logo" 
            style={{ height: '28px', width: 'auto', objectFit: 'contain' }} 
          />
          <span style={{ color: 'var(--text-dim)', fontSize: '0.85rem', fontWeight: 600 }}>| Content Factory</span>
        </div>
        <span className="brand-badge">Property Edition v0.1</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {/* Active Project Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Project:</span>
          <select 
            className="form-select" 
            style={{ width: '220px', padding: '6px 10px', fontSize: '0.84rem' }}
            value={currentProject?.id || ''}
            onChange={(e) => {
              const selected = projects.find(p => p.id === e.target.value);
              setCurrentProject(selected || null);
            }}
          >
            {projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>

        {/* Quick Generate Action */}
        <button className="btn btn-primary btn-sm" onClick={onQuickGenerate}>
          <Sparkles size={15} />
          <span>Buat Konten Baru</span>
        </button>

        {/* System Health Indicator */}
        <div className="badge badge-success" title="System Engine Online">
          <Activity size={12} />
          <span>{healthStatus?.status === 'online' ? 'Engine Ready' : 'Connecting...'}</span>
        </div>

        {/* Settings Modal Trigger */}
        <button className="btn btn-secondary btn-icon-only" onClick={onOpenSettings} title="Pengaturan Provider & Storage">
          <SettingsIcon size={17} />
        </button>
      </div>
    </header>
  );
}
