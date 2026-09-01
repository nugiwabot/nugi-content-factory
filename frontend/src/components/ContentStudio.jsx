import React, { useState } from 'react';
import { Copy, Check, Download, ShieldCheck, AlertCircle } from 'lucide-react';

export default function ContentStudio({ contents, onRefresh }) {
  const [copiedId, setCopiedId] = useState(null);

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  return (
    <div className="page-body">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Content Studio & Published Gallery</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Daftar visual marketing dan copy yang telah diproduksi secara deterministic oleh sistem.
          </p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={onRefresh}>
          Refresh Galeri
        </button>
      </div>

      {contents.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <p style={{ color: 'var(--text-muted)', marginBottom: '12px' }}>Belum ada konten yang dibuat untuk project ini.</p>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)' }}>Gunakan menu "Brief Creator" untuk membuat konten pertama Anda.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '22px' }}>
          {contents.map(c => {
            const finalAsset = c.assets?.find(a => a.asset_type === 'rendered_final') || c.assets?.[0];
            const qaResult = c.qa_results?.[0];

            return (
              <div key={c.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {/* Visual Preview */}
                {finalAsset && (
                  <div style={{ width: '100%', height: '280px', borderRadius: 'var(--radius-md)', overflow: 'hidden', background: '#04070d', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <img 
                      src={`/api/v1/assets/download?path=${finalAsset.file_path}`} 
                      alt={c.headline} 
                      style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                    />
                  </div>
                )}

                {/* Header & QA Badge */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span className="badge badge-info">{c.status}</span>
                  {qaResult && (
                    <span className={`badge ${qaResult.status === 'PASSED' ? 'badge-success' : 'badge-warning'}`}>
                      {qaResult.status === 'PASSED' ? <ShieldCheck size={12} /> : <AlertCircle size={12} />}
                      <span>QA: {qaResult.status}</span>
                    </span>
                  )}
                </div>

                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#fff' }}>{c.headline}</h3>

                {/* Caption Snippet */}
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: 'var(--radius-sm)', fontSize: '0.82rem', color: 'var(--text-muted)', maxHeight: '120px', overflowY: 'auto', whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>
                  {c.body_caption}
                </div>

                {/* Action Buttons */}
                <div style={{ display: 'flex', gap: '8px', marginTop: 'auto', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)' }}>
                  <button 
                    className="btn btn-secondary btn-sm" 
                    style={{ flex: 1 }}
                    onClick={() => copyToClipboard(`${c.body_caption}\n\n${c.hashtags || ''}`, c.id)}
                  >
                    {copiedId === c.id ? <Check size={14} color="var(--accent-emerald)" /> : <Copy size={14} />}
                    <span>{copiedId === c.id ? 'Tersalin!' : 'Copy Caption'}</span>
                  </button>

                  {finalAsset && (
                    <a 
                      href={`/api/v1/assets/download?path=${finalAsset.file_path}`} 
                      download 
                      target="_blank"
                      rel="noreferrer"
                      className="btn btn-secondary btn-sm"
                    >
                      <Download size={14} />
                      <span>Download</span>
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
