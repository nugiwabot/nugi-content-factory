import React from 'react';
import { Clock, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';

export default function JobStatusTracker({ jobs, onRefresh }) {
  return (
    <div className="page-body">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Generation Job Tracker</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Pantau status eksekusi antrean pipeline AI (Reasoning ➔ Image Gen ➔ Deterministic Render ➔ QA).
          </p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={onRefresh}>
          Refresh Queue
        </button>
      </div>

      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.86rem' }}>
          <thead>
            <tr style={{ background: 'rgba(0,0,0,0.4)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-dim)' }}>
              <th style={{ padding: '14px 18px' }}>Job ID</th>
              <th style={{ padding: '14px 18px' }}>Type</th>
              <th style={{ padding: '14px 18px' }}>Status</th>
              <th style={{ padding: '14px 18px' }}>Progress</th>
              <th style={{ padding: '14px 18px' }}>Waktu</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ padding: '30px', textAlign: 'center', color: 'var(--text-dim)' }}>
                  Belum ada job eksekusi tercatat.
                </td>
              </tr>
            ) : (
              jobs.map(j => (
                <tr key={j.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '14px 18px', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--accent-cyan)' }}>
                    {j.id.slice(0, 8)}...
                  </td>
                  <td style={{ padding: '14px 18px' }}>{j.job_type}</td>
                  <td style={{ padding: '14px 18px' }}>
                    {j.status === 'COMPLETED' && <span className="badge badge-success"><CheckCircle2 size={12} /> COMPLETED</span>}
                    {j.status === 'RUNNING' && <span className="badge badge-info"><Loader2 size={12} className="spin" /> RUNNING</span>}
                    {j.status === 'QUEUED' && <span className="badge badge-warning"><Clock size={12} /> QUEUED</span>}
                    {j.status === 'FAILED' && <span className="badge badge-error"><AlertTriangle size={12} /> FAILED</span>}
                  </td>
                  <td style={{ padding: '14px 18px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '80px', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ width: `${j.progress_percentage}%`, height: '100%', background: 'var(--accent-cyan)' }}></div>
                      </div>
                      <span style={{ fontSize: '0.76rem', color: 'var(--text-dim)' }}>{j.progress_percentage}%</span>
                    </div>
                  </td>
                  <td style={{ padding: '14px 18px', color: 'var(--text-dim)', fontSize: '0.8rem' }}>
                    {new Date(j.created_at).toLocaleTimeString('id-ID')}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
