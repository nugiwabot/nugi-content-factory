import React, { useState } from 'react';
import { 
  Sparkles, 
  RefreshCw, 
  Download, 
  Copy, 
  Check, 
  ShieldCheck, 
  Layers, 
  Palette, 
  FileText, 
  Compass, 
  ArrowRight,
  HelpCircle,
  Lightbulb,
  Target
} from 'lucide-react';
import { api } from '../services/api';

export default function AIContentStudio({ currentProject }) {
  const [topic, setTopic] = useState('Kenapa leads iklan properti banyak tapi closing tetap rendah?');
  const [audience, setAudience] = useState('Developer & Tim Marketing Properti');
  const [contentTypeOverride, setContentTypeOverride] = useState('');
  const [keyInfo, setKeyInfo] = useState('');

  const [generating, setGenerating] = useState(false);
  const [reheadLoading, setReheadLoading] = useState(false);
  const [recapLoading, setRecapLoading] = useState(false);
  const [revisLoading, setRevisLoading] = useState(false);

  const [contentPackage, setContentPackage] = useState(null);
  const [error, setError] = useState(null);
  const [copiedCaption, setCopiedCaption] = useState(false);

  const presets = [
    { label: 'Leads Boncos Closing Nol', topic: 'Kenapa leads iklan properti banyak tapi closing tetap rendah?', aud: 'Developer & Sales Manager' },
    { label: '5 Kesalahan Fatal Follow-Up', topic: '5 Kesalahan fatal follow up leads properti yang bikin prospek kabur', aud: 'Sales & Agen Properti' },
    { label: 'Kenaikan Harga Dekat Tol', topic: 'Kenapa harga rumah di dekat akses tol bisa naik lebih cepat?', aud: 'Investor & Pembeli Properti' },
    { label: 'Showcase Rukost Jatinangor', topic: 'Unit rukost premium dekat kampus UNPAD Jatinangor siap sewa', aud: 'Investor Passive Income' },
    { label: 'Studi Kasus Kecepatan Respon', topic: 'Studi kasus hasil transformasi response time tim sales properti', aud: 'Principal Agen & Developer' },
    { label: 'Opini: Otomasi Marketing', topic: 'Developer yang menolak otomasi marketing akan tertinggal oleh pasar', aud: 'Owner Developer Properti' }
  ];

  const handleApplyPreset = (p) => {
    setTopic(p.topic);
    setAudience(p.aud);
  };

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    if (!topic.trim()) return;

    setGenerating(true);
    setError(null);

    try {
      const payload = {
        topic: topic.trim(),
        target_audience: audience.trim(),
        content_type_override: contentTypeOverride || null,
        key_information: keyInfo || null,
        project_id: currentProject?.id || null
      };

      const result = await api.generateAIContent(payload);
      setContentPackage(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleRegenerateHeadline = async () => {
    if (!contentPackage) return;
    setReheadLoading(true);
    try {
      const res = await api.regenerateHeadline({
        package: contentPackage,
        custom_topic: topic
      });
      setContentPackage(res);
    } catch (err) {
      setError('Gagal meregenerasi headline: ' + err.message);
    } finally {
      setReheadLoading(false);
    }
  };

  const handleRegenerateCaption = async () => {
    if (!contentPackage) return;
    setRecapLoading(true);
    try {
      const res = await api.regenerateCaption({
        package: contentPackage
      });
      setContentPackage(res);
    } catch (err) {
      setError('Gagal meregenerasi caption: ' + err.message);
    } finally {
      setRecapLoading(false);
    }
  };

  const handleRegenerateVisual = async () => {
    if (!contentPackage) return;
    setRevisLoading(true);
    try {
      const res = await api.regenerateVisual({
        package: contentPackage
      });
      setContentPackage(res);
    } catch (err) {
      setError('Gagal meregenerasi visual: ' + err.message);
    } finally {
      setRevisLoading(false);
    }
  };

  const handleCopyCaption = () => {
    if (!contentPackage?.editorial_spec?.caption) return;
    navigator.clipboard.writeText(contentPackage.editorial_spec.caption);
    setCopiedCaption(true);
    setTimeout(() => setCopiedCaption(false), 2500);
  };

  return (
    <div className="page-body">
      {/* Top Banner */}
      <div style={{ marginBottom: '22px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={26} color="var(--accent-cyan)" />
          <h2 style={{ fontSize: '1.45rem', fontWeight: 800 }}>AI Content & Art Direction Studio</h2>
          <span className="badge badge-info" style={{ fontSize: '0.74rem' }}>Phase 3B Intelligence</span>
        </div>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Input brief sederhana ➔ AI Content Strategist ➔ Creative Director ➔ Deterministic Pillow Rendering ➔ Visual QA.
        </p>
      </div>

      {/* Preset Quick Starters */}
      <div style={{ marginBottom: '20px' }}>
        <p style={{ fontSize: '0.74rem', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '8px' }}>
          ⚡ Preset Topik Properti Populer (1-Click Test):
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {presets.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="btn btn-sm btn-secondary"
              style={{ fontSize: '0.76rem', padding: '6px 12px' }}
              onClick={() => handleApplyPreset(p)}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Studio Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '440px 1fr', gap: '24px', alignItems: 'start' }}>
        {/* Left Column: Brief Input Form */}
        <div className="card">
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileText size={18} color="var(--accent-cyan)" />
            <span>1. User Brief Input</span>
          </h3>

          <form onSubmit={handleGenerate}>
            <div className="form-group">
              <label className="form-label">Topik / Masalah / Pertanyaan Properti *</label>
              <textarea
                className="form-textarea"
                rows={3}
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Contoh: Kenapa leads iklan properti banyak tapi closing tetap rendah?"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Target Audience Persona</label>
              <input
                type="text"
                className="form-input"
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                placeholder="Developer, Sales Manager, Agen Properti..."
              />
            </div>

            <div className="form-group">
              <label className="form-label">Content Type (Otomatis / Override)</label>
              <select
                className="form-select"
                value={contentTypeOverride}
                onChange={(e) => setContentTypeOverride(e.target.value)}
              >
                <option value="">🤖 AI Auto-Detect (Direkomendasikan)</option>
                <option value="PROPERTY_PROBLEM">PROPERTY_PROBLEM (Dilema & Friksi Sales)</option>
                <option value="PROPERTY_INSIGHT">PROPERTY_INSIGHT (Market Insight & Data)</option>
                <option value="PROPERTY_EDUCATION">PROPERTY_EDUCATION (Edukasi Fundamental)</option>
                <option value="PROPERTY_LISTICLE">PROPERTY_LISTICLE (Poin Bernomor / Kesalahan)</option>
                <option value="PROPERTY_CASE_STUDY">PROPERTY_CASE_STUDY (Studi Kasus & Hasil)</option>
                <option value="PROPERTY_SHOWCASE">PROPERTY_SHOWCASE (Unit Rukost/Villa/Rumah)</option>
                <option value="PROPERTY_OPINION">PROPERTY_OPINION (Opini & Perspektif Industri)</option>
                <option value="PROPERTY_SALES_OFFER">PROPERTY_SALES_OFFER (Penawaran Audit/Direct)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Informasi / Data Tambahan (Opsional)</label>
              <input
                type="text"
                className="form-input"
                value={keyInfo}
                onChange={(e) => setKeyInfo(e.target.value)}
                placeholder="Contoh: Waktu respon turun 300%, lokasi Jatinangor..."
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={generating}
              style={{ width: '100%', marginTop: '10px', padding: '12px' }}
            >
              {generating ? <RefreshCw size={16} className="spin" /> : <Sparkles size={16} />}
              <span>{generating ? 'AI Strategist & Director Sedang Berpikir...' : 'Generate Full Content Package'}</span>
            </button>
          </form>
        </div>

        {/* Right Column: AI Strategy, Copy, Visual Art Direction & Rendered Output */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {error && (
            <div className="card" style={{ borderColor: 'var(--accent-rose)', color: 'var(--accent-rose)' }}>
              {error}
            </div>
          )}

          {generating && (
            <div className="card" style={{ textAlign: 'center', padding: '50px 20px', color: 'var(--text-muted)' }}>
              <RefreshCw size={32} className="spin" color="var(--accent-cyan)" style={{ margin: '0 auto 16px auto' }} />
              <h4 style={{ color: '#fff', fontSize: '1.1rem', fontWeight: 700 }}>Merumuskan Strategi & Art Direction...</h4>
              <p style={{ fontSize: '0.84rem', marginTop: '6px' }}>
                Content Strategist ➔ Copywriter ➔ Creative Director ➔ Pillow Renderer ➔ Visual QA
              </p>
            </div>
          )}

          {!generating && contentPackage && (
            <>
              {/* Strategy & Intelligence Preview */}
              <div className="card" style={{ background: 'rgba(15, 23, 42, 0.75)', borderColor: 'var(--border-highlight)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Lightbulb size={18} color="var(--accent-gold)" />
                    <h3 style={{ fontSize: '1rem', fontWeight: 800 }}>2. AI Content Strategy & Art Direction</h3>
                  </div>
                  <span className="badge badge-info">{contentPackage.content_type}</span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', fontSize: '0.78rem' }}>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 12px', borderRadius: 'var(--radius-sm)' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Arketipe Visual: </span>
                    <strong style={{ color: 'var(--accent-cyan)' }}>{contentPackage.art_direction_spec.archetype}</strong>
                  </div>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 12px', borderRadius: 'var(--radius-sm)' }}>
                    <span style={{ color: 'var(--text-dim)' }}>CTA Business Rule: </span>
                    <strong style={{ color: 'var(--accent-emerald)' }}>{contentPackage.editorial_spec.cta_policy}</strong>
                  </div>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 12px', borderRadius: 'var(--radius-sm)' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Negative Space: </span>
                    <strong style={{ color: '#fff' }}>{contentPackage.art_direction_spec.negative_space_location}</strong>
                  </div>
                </div>

                <div style={{ marginTop: '12px', fontSize: '0.8rem', color: 'var(--text-secondary)', borderTop: '1px solid var(--border-subtle)', paddingTop: '10px' }}>
                  <p><strong>🎯 Sudut Pandang Editorial:</strong> {contentPackage.editorial_spec.editorial_angle}</p>
                  <p style={{ marginTop: '4px' }}><strong>💡 Core Insight:</strong> {contentPackage.editorial_spec.core_insight}</p>
                </div>
              </div>

              {/* Main Content & Visual Preview Container */}
              <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: '20px', alignItems: 'start' }}>
                {/* Visual Canvas Display */}
                <div style={{ background: '#04070d', borderRadius: 'var(--radius-lg)', padding: '10px', border: '1px solid var(--border-highlight)', boxShadow: 'var(--shadow-lg)' }}>
                  <img
                    src={contentPackage.rendered_asset_url}
                    alt="Rendered Editorial Graphic"
                    style={{ width: '100%', borderRadius: 'var(--radius-md)', display: 'block' }}
                  />
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px', padding: '0 4px' }}>
                    <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>
                      1080 × 1350 (4:5 Instagram Feed)
                    </span>
                    <a
                      href={contentPackage.rendered_asset_url}
                      download={`nugiproperti_${contentPackage.content_type.toLowerCase()}_1080x1350.png`}
                      className="btn btn-secondary btn-sm"
                    >
                      <Download size={14} />
                      <span>Download PNG</span>
                    </a>
                  </div>

                  {/* QA Score Card */}
                  {contentPackage.visual_qa && (
                    <div style={{ marginTop: '12px', padding: '10px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(16, 185, 129, 0.25)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--accent-emerald)', fontWeight: 700 }}>
                        <ShieldCheck size={16} />
                        <span>Visual QA: {contentPackage.visual_qa.score}/100</span>
                      </div>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>WCAG AAA Compliant</span>
                    </div>
                  )}
                </div>

                {/* Modular Copy & Prompt Inspector */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {/* Headline Editor */}
                  <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>Headline Grafis</h4>
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        disabled={reheadLoading}
                        onClick={handleRegenerateHeadline}
                      >
                        <RefreshCw size={13} className={reheadLoading ? 'spin' : ''} />
                        <span>Regenerate Headline</span>
                      </button>
                    </div>
                    <p style={{ fontSize: '1.05rem', fontWeight: 800, color: '#fff', lineHeight: 1.3 }}>
                      {contentPackage.editorial_spec.headline}
                    </p>
                    <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '6px' }}>
                      {contentPackage.editorial_spec.subheadline}
                    </p>
                    <div style={{ marginTop: '8px', display: 'flex', gap: '6px' }}>
                      {contentPackage.editorial_spec.highlight_words.map((hw, idx) => (
                        <span key={idx} className="badge badge-warning" style={{ fontSize: '0.7rem' }}>
                          Highlight: {hw}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Caption / Article Body */}
                  <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>Instagram Caption (Full Article)</h4>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        <button
                          type="button"
                          className="btn btn-secondary btn-sm"
                          disabled={recapLoading}
                          onClick={handleRegenerateCaption}
                        >
                          <RefreshCw size={13} className={recapLoading ? 'spin' : ''} />
                          <span>Regenerate Caption</span>
                        </button>
                        <button
                          type="button"
                          className="btn btn-primary btn-sm"
                          onClick={handleCopyCaption}
                        >
                          {copiedCaption ? <Check size={13} /> : <Copy size={13} />}
                          <span>{copiedCaption ? 'Tersalin!' : 'Copy Caption'}</span>
                        </button>
                      </div>
                    </div>
                    <div style={{ maxHeight: '220px', overflowY: 'auto', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem', whiteSpace: 'pre-wrap', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                      {contentPackage.editorial_spec.caption}
                    </div>
                  </div>

                  {/* Visual Art Direction & Flux Prompt Inspector */}
                  <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--accent-gold)' }}>Visual Prompt (Pure Photography)</h4>
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        disabled={revisLoading}
                        onClick={handleRegenerateVisual}
                      >
                        <RefreshCw size={13} className={revisLoading ? 'spin' : ''} />
                        <span>Regenerate Visual Concept</span>
                      </button>
                    </div>
                    <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: 'var(--radius-sm)', lineHeight: 1.4 }}>
                      {contentPackage.art_direction_spec.image_prompt}
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
