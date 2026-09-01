import React, { useState, useEffect, useRef } from 'react';
import { Upload, RefreshCw, Trash2, Database, BookOpen, Target, FileText } from 'lucide-react';
import { api } from '../services/api';

export default function KnowledgeManager() {
  const [skills, setSkills] = useState([]);
  const [pillars, setPillars] = useState([]);
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);
  const fileInputRef = useRef(null);

  const loadAll = async () => {
    try {
      setLoading(true);
      const [skillRes, pillarRes, brandRes] = await Promise.all([
        api.listSkills().catch(() => []),
        api.getPillars().catch(() => []),
        api.getBrandContexts().catch(() => [])
      ]);
      setSkills(skillRes);
      setPillars(pillarRes);
      setBrands(brandRes);
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setMessage(null);
    try {
      const res = await api.uploadKnowledge(file);
      setMessage({ type: 'success', text: `${res.count} skill berhasil ditambahkan.` });
      loadAll();
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteSkill(id);
      loadAll();
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    }
  };

  const handleSeed = async () => {
    setMessage(null);
    try {
      const res = await api.seedKnowledge();
      setMessage({ type: 'success', text: `Seed selesai: ${res.skills} skill, ${res.pillars} pillar, ${res.brand} brand.` });
      loadAll();
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    }
  };

  return (
    <div className="page-body">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Knowledge Base</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Skill & framework yang dipakai AI Agent untuk menulis copy & caption sesuai gaya Nugi.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-secondary btn-sm" onClick={() => fileInputRef.current?.click()} disabled={uploading}>
            {uploading ? <RefreshCw size={14} className="spin" /> : <Upload size={14} />}
            <span>Upload skill (.md / .zip)</span>
          </button>
          <button className="btn btn-secondary btn-sm" onClick={handleSeed}>
            <Database size={14} />
            <span>Re-seed</span>
          </button>
          <input ref={fileInputRef} type="file" accept=".md,.markdown,.zip" style={{ display: 'none' }} onChange={handleUpload} />
        </div>
      </div>

      {message && (
        <div style={{ padding: '10px 14px', borderRadius: 'var(--radius-md)', marginBottom: '16px', background: message.type === 'error' ? 'rgba(244,63,94,0.15)' : 'rgba(16,185,129,0.15)', color: message.type === 'error' ? 'var(--accent-rose)' : 'var(--accent-emerald)', fontSize: '0.85rem', border: `1px solid ${message.type === 'error' ? 'rgba(244,63,94,0.3)' : 'rgba(16,185,129,0.3)'}` }}>
          {message.text}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Memuat knowledge base...</div>
      ) : (
        <>
          <section style={{ marginBottom: '28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Target size={16} color="#c084fc" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Content Pillars</h3>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '14px' }}>
              {pillars.map(p => (
                <div key={p.id} className="card" style={{ padding: '14px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 700, color: '#f8fafc' }}>{p.name}</span>
                    <span className="badge badge-purple">{Math.round(p.ratio * 100)}%</span>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)', marginTop: '2px' }}>Goal: {p.business_goal}</p>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '8px', lineHeight: 1.4 }}>{p.prompt_guidance}</p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '8px' }}>
                    {(p.mapped_content_types || []).slice(0, 4).map(t => (
                      <span key={t} className="badge badge-info" style={{ fontSize: '0.62rem' }}>{t}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section style={{ marginBottom: '28px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <FileText size={16} color="#c084fc" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Brand Context</h3>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '14px' }}>
              {brands.map(b => (
                <div key={b.id} className="card" style={{ padding: '14px' }}>
                  <span style={{ fontWeight: 700, color: '#f8fafc' }}>{b.name}</span>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '8px', maxHeight: '160px', overflowY: 'auto', whiteSpace: 'pre-wrap', lineHeight: 1.45 }}>{b.content}</p>
                </div>
              ))}
            </div>
          </section>

          <section>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <BookOpen size={16} color="#c084fc" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Skills ({skills.length})</h3>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '14px' }}>
              {skills.map(s => (
                <div key={s.id} className="card" style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                      <span style={{ fontWeight: 700, color: '#f8fafc' }}>{s.name}</span>
                      <span className="badge badge-info" style={{ marginLeft: '8px', fontSize: '0.62rem' }}>{s.source}</span>
                    </div>
                    <button className="btn btn-secondary btn-sm" style={{ padding: '4px 8px' }} onClick={() => handleDelete(s.id)} title="Hapus skill">
                      <Trash2 size={13} color="var(--accent-rose)" />
                    </button>
                  </div>
                  <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>{s.description}</p>
                </div>
              ))}
              {skills.length === 0 && <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>Belum ada skill. Klik "Re-seed" atau upload file skill.</p>}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
