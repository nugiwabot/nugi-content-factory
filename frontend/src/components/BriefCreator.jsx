import React, { useState } from 'react';
import { Sparkles, Send, BookOpen, Target, MessageSquare } from 'lucide-react';
import { api } from '../services/api';

export default function BriefCreator({ currentProject, onContentGenerated }) {
  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('Leader Sales & Marketing Manager Properti');
  const [pillar, setPillar] = useState('educational');
  const [tone, setTone] = useState('professional_authoritative');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const presets = [
    {
      label: '⚡ Leads Iklan Dingin',
      topic: '3 Alasan Kenapa Leads Iklan Properti Sering Dingin dan Cara Mengatasinya',
      audience: 'Developer & Sales Manager Properti',
      pillar: 'educational'
    },
    {
      label: '🏢 Investasi Rukos Mahasiswa',
      topic: 'Strategi Passive Income Stabil dari Rumah Kost Mahasiswa dengan Yield 12%',
      audience: 'Investor Properti & Orang Tua Mahasiswa',
      pillar: 'direct_offer'
    },
    {
      label: '📑 Edukasi Legalitas Tanah',
      topic: 'Daftar Dokumen Legalitas Wajib Dicek Sebelum Membeli Lahan Properti',
      audience: 'Calon Pembeli Rumah Pertama & Praktisi Agen',
      pillar: 'authority'
    }
  ];

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!topic.trim() || !currentProject) return;
    setGenerating(true);
    setError(null);
    setResult(null);

    try {
      const resp = await api.generateContent({
        project_id: currentProject.id,
        topic,
        target_audience: audience,
        content_pillar: pillar,
        tone_of_voice: tone
      });
      setResult(resp);
      onContentGenerated(resp);
    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="page-body">
      <div style={{ maxWidth: '840px', margin: '0 auto' }}>
        <div style={{ marginBottom: '22px' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>AI Property Content Brief & Generation</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Tulis brief pemasaran atau pilih template siap pakai untuk memproduksi konten visual & copy berkonversi tinggi.
          </p>
        </div>

        {/* Quick Presets Strip */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-dim)', alignSelf: 'center', marginRight: '4px' }}>Ide Siap Pakai:</span>
          {presets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => {
                setTopic(p.topic);
                setAudience(p.audience);
                setPillar(p.pillar);
              }}
            >
              {p.label}
            </button>
          ))}
        </div>

        <form onSubmit={handleGenerate} className="card" style={{ marginBottom: '24px' }}>
          <div className="form-group">
            <label className="form-label">Topik atau Ide Pokok Konten *</label>
            <input
              type="text"
              className="form-input"
              placeholder="Contoh: Mengapa respon cepat leads iklan dalam 10 menit pertama menentukan closing properti?"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Target Audience / Persona</label>
              <input
                type="text"
                className="form-input"
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Pillar Strategi Konten</label>
              <select className="form-select" value={pillar} onChange={(e) => setPillar(e.target.value)}>
                <option value="educational">Edukasi & Tips Lapangan</option>
                <option value="authority">Otoritas & Pengalaman Nyata</option>
                <option value="direct_offer">Penawaran Langsung / Unit</option>
                <option value="case_study">Studi Kasus & Pembuktian</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
            <button type="submit" className="btn btn-primary" disabled={generating || !currentProject}>
              <Sparkles size={16} />
              <span>{generating ? 'Memproses Reasoning & Rendering...' : 'Generate Konten Deterministic'}</span>
            </button>
          </div>
        </form>

        {error && (
          <div className="card" style={{ borderColor: 'var(--accent-rose)', color: 'var(--accent-rose)', marginBottom: '20px' }}>
            <p><strong>Error:</strong> {error}</p>
          </div>
        )}

        {/* Live Generation Result Preview */}
        {result && (
          <div className="card" style={{ borderColor: 'var(--accent-cyan)', background: 'rgba(15, 23, 42, 0.9)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
              <span className="badge badge-success">✓ Konten Selesai Dirender</span>
              <span className="badge badge-info">Job ID: {result.job_id.slice(0, 8)}...</span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '22px', alignItems: 'start' }}>
              <div>
                <img 
                  src={`/api/v1/assets/download?path=${result.asset_path}`} 
                  alt="Rendered graphic" 
                  style={{ width: '100%', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-card)', boxShadow: 'var(--shadow-md)' }}
                />
              </div>

              <div>
                <h4 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>{result.headline}</h4>
                <p style={{ fontSize: '0.84rem', color: 'var(--accent-cyan)', fontWeight: 600, marginBottom: '12px' }}>{result.hook_text}</p>
                <div style={{ background: 'rgba(0,0,0,0.4)', padding: '14px', borderRadius: 'var(--radius-md)', fontSize: '0.86rem', color: 'var(--text-muted)', whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                  {result.body_caption}
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '8px' }}>{result.hashtags}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
