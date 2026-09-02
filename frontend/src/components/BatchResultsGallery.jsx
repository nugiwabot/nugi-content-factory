import React, { useState } from 'react';
import { Copy, Check, Download, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function BatchResultsGallery({ batchRun, onRefresh }) {
  const [copiedId, setCopiedId] = useState(null);

  const copyCaption = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const statusLabel = {
    QUEUED: 'Antre',
    RUNNING: 'Berjalan',
    COMPLETED: 'Selesai',
    FAILED: 'Gagal'
  };

  if (!batchRun) return null;

  const items = batchRun.items || [];
  const isRunning = ['QUEUED', 'RUNNING'].includes(batchRun.status);

  return (
    <div className="card" style={{ margin: '16px 0 24px 0', padding: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            {isRunning ? <Loader2 size={18} className="spin" color="#c084fc" /> : <CheckCircle2 size={18} color="var(--accent-emerald)" />}
            <span style={{ fontWeight: 700, color: '#f8fafc' }}>
              Batch {statusLabel[batchRun.status] || batchRun.status}
              <span style={{ color: 'var(--text-dim)', fontWeight: 500 }}>
                {' · '}{batchRun.completed_items}/{batchRun.total_items} konten
              </span>
            </span>
            {!isRunning && batchRun.summary?.estimated_cost_usd != null && batchRun.summary?.estimated_cost_usd > 0 && (
              <span className="badge badge-info">Est. biaya: ${Number(batchRun.summary.estimated_cost_usd).toFixed(4)}</span>
            )}
          </div>
          <button className="btn btn-secondary btn-sm" onClick={onRefresh} disabled={isRunning}>
            {isRunning ? 'Memproses...' : 'Refresh'}
          </button>
        </div>

      {items.length === 0 ? (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Menunggu hasil generasi...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
          {items.map(it => (
            <div key={it.id} style={{ background: 'rgba(7, 11, 20, 0.6)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
              <div style={{ width: '100%', aspectRatio: '1080 / 1350', background: '#040711', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                {it.asset_url ? (
                  <img
                    src={`/api/v1/assets/download?path=${it.asset_path}`}
                    alt={it.headline || it.topic}
                    style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                  />
                ) : it.status === 'FAILED' ? (
                  <AlertCircle size={28} color="var(--accent-rose)" />
                ) : (
                  <Loader2 size={28} className="spin" color="#c084fc" />
                )}
              </div>
              <div style={{ padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {it.content_type && <span className="badge badge-info">{it.content_type}</span>}
                  {it.pillar && <span className="badge badge-purple">{it.pillar}</span>}
                  {it.status === 'FAILED' && <span className="badge badge-error">Gagal</span>}
                </div>
                <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#f8fafc', lineHeight: 1.3 }}>
                  {it.headline || it.topic}
                </h4>
                {it.error && <p style={{ fontSize: '0.75rem', color: 'var(--accent-rose)' }}>{it.error}</p>}
                {it.caption && (
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', maxHeight: '90px', overflowY: 'auto', whiteSpace: 'pre-wrap', lineHeight: 1.45 }}>
                    {it.caption}
                  </p>
                )}
                <div style={{ display: 'flex', gap: '8px', marginTop: 'auto', paddingTop: '8px' }}>
                  {it.caption && (
                    <button className="btn btn-secondary btn-sm" style={{ flex: 1 }} onClick={() => copyCaption(it.caption, it.id)}>
                      {copiedId === it.id ? <Check size={13} color="var(--accent-emerald)" /> : <Copy size={13} />}
                      <span>{copiedId === it.id ? 'Tersalin' : 'Caption'}</span>
                    </button>
                  )}
                  {it.asset_path && (
                    <a href={`/api/v1/assets/download?path=${it.asset_path}`} download target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
                      <Download size={13} />
                      <span>Unduh</span>
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
