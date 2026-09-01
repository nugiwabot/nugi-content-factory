import React from 'react';
import { X, Server, HardDrive, Cpu, ShieldAlert } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose, healthStatus }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>System Configuration & Status</h3>
          <button className="btn btn-secondary btn-icon-only" onClick={onClose}><X size={16} /></button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Engine Environment */}
          <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <Server size={16} color="var(--accent-cyan)" />
              <strong style={{ fontSize: '0.88rem' }}>Backend Server Engine</strong>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Environment: <span style={{ color: '#fff', fontWeight: 600 }}>{healthStatus?.environment || 'development'}</span> | Status: <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>{healthStatus?.status || 'Active'}</span>
            </p>
          </div>

          {/* AI Providers */}
          <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <Cpu size={16} color="var(--accent-indigo)" />
              <strong style={{ fontSize: '0.88rem' }}>Active AI Providers (Phase 1)</strong>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              LLM Provider: <span style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>{healthStatus?.providers?.llm || 'MockLLMProvider'}</span>
            </p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Image Generator: <span style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>{healthStatus?.providers?.image || 'MockImageProvider'}</span>
            </p>
          </div>

          {/* Storage Directory */}
          <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <HardDrive size={16} color="var(--accent-emerald)" />
              <strong style={{ fontSize: '0.88rem' }}>Local Asset Storage</strong>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', wordBreak: 'break-all' }}>
              Path: {healthStatus?.storage?.path || './storage/assets'}
            </p>
          </div>

          {/* Security Note */}
          <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start', background: 'rgba(56, 189, 248, 0.08)', padding: '12px', borderRadius: 'var(--radius-md)', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
            <ShieldAlert size={16} color="var(--accent-cyan)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
              API Keys dan rahasia aplikasi dikelola secara aman melalui environment variables / <code style={{ color: '#fff' }}>.env</code> dan tidak pernah diekspos ke client.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '22px' }}>
          <button className="btn btn-secondary" onClick={onClose}>Tutup</button>
        </div>
      </div>
    </div>
  );
}
