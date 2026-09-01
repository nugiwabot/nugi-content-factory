import React, { useState } from 'react';
import { X, Server, HardDrive, Cpu, ShieldAlert, Sparkles, RefreshCw, CheckCircle2, AlertTriangle } from 'lucide-react';
import { api } from '../services/api';

export default function SettingsModal({ isOpen, onClose, healthStatus }) {
  const [testingFlux, setTestingFlux] = useState(false);
  const [fluxResult, setFluxResult] = useState(null);

  if (!isOpen) return null;

  const handleTestFlux = async () => {
    setTestingFlux(true);
    setFluxResult(null);
    try {
      const res = await api.checkFluxStatus();
      setFluxResult(res);
    } catch (err) {
      setFluxResult({
        status: 'FAILED',
        message: err.message || 'Gagal menghubungi server untuk pengetesan Flux.'
      });
    } finally {
      setTestingFlux(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-card" style={{ maxWidth: '520px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>System Configuration & Status</h3>
          <button className="btn btn-secondary btn-icon-only" onClick={onClose}><X size={16} /></button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
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

          {/* AI Providers & Flux Status */}
          <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sparkles size={16} color="var(--accent-gold)" />
                <strong style={{ fontSize: '0.88rem' }}>Flux Image Provider</strong>
              </div>
              <button 
                className="btn btn-secondary btn-sm" 
                style={{ fontSize: '0.72rem', padding: '4px 8px' }}
                disabled={testingFlux}
                onClick={handleTestFlux}
              >
                <RefreshCw size={12} className={testingFlux ? 'spin' : ''} />
                <span>{testingFlux ? 'Testing...' : 'Test Connection'}</span>
              </button>
            </div>
            
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Configured in .env: <span style={{ color: healthStatus?.providers?.flux_configured ? 'var(--accent-emerald)' : 'var(--text-dim)', fontWeight: 700 }}>
                {healthStatus?.providers?.flux_configured ? 'Yes (Key Set)' : 'No (Using Mock Fallback)'}
              </span>
            </p>

            {/* Test Result Message */}
            {fluxResult && (
              <div style={{ 
                marginTop: '10px', 
                padding: '8px 10px', 
                borderRadius: 'var(--radius-sm)', 
                fontSize: '0.74rem', 
                background: fluxResult.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.12)' : fluxResult.status === 'NOT_CONFIGURED' ? 'rgba(56, 189, 248, 0.1)' : 'rgba(244, 63, 94, 0.12)',
                border: `1px solid ${fluxResult.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.3)' : fluxResult.status === 'NOT_CONFIGURED' ? 'rgba(56, 189, 248, 0.25)' : 'rgba(244, 63, 94, 0.3)'}`,
                color: fluxResult.status === 'SUCCESS' ? 'var(--accent-emerald)' : fluxResult.status === 'NOT_CONFIGURED' ? 'var(--accent-cyan)' : 'var(--accent-rose)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700, marginBottom: '2px' }}>
                  {fluxResult.status === 'SUCCESS' ? <CheckCircle2 size={13} /> : <AlertTriangle size={13} />}
                  <span>Status: {fluxResult.status}</span>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.72rem' }}>{fluxResult.message}</p>
              </div>
            )}
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
            <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
              API Keys dan rahasia aplikasi dikelola secara aman melalui environment variables / <code style={{ color: '#fff' }}>.env</code> dan tidak pernah diekspos ke client.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '18px' }}>
          <button className="btn btn-secondary" onClick={onClose}>Tutup</button>
        </div>
      </div>
    </div>
  );
}
