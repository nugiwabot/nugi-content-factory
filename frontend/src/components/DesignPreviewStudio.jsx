import React, { useState, useEffect } from 'react';
import { Sparkles, Download, CheckCircle2, AlertTriangle, ShieldCheck, RefreshCw, Layout, Layers } from 'lucide-react';
import { api } from '../services/api';

export default function DesignPreviewStudio() {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState('01_PROPERTY_PROBLEM');
  const [dimension, setDimension] = useState({ width: 1080, height: 1350, label: '1080 x 1350 (Portrait Feed 4:5)' });
  
  // Design Input Form
  const [headline, setHeadline] = useState('LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?');
  const [highlightWords, setHighlightWords] = useState('LAMBAT FOLLOW-UP');
  const [subheadline, setSubheadline] = useState('Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.');
  const [badgeText, setBadgeText] = useState('DILEMA SALES PROPERTI');
  const [bulletPoints, setBulletPoints] = useState('Respon lebih dari 30 menit\nTemplate chat kaku tanpa personalisasi\nTidak follow up kedua kalinya');
  const [metricValue, setMetricValue] = useState('+300% Speed');
  const [metricLabel, setMetricLabel] = useState('Waktu Respon Prospek Iklan');
  const [ctaText, setCtaText] = useState('Pelajari Solusinya →');

  const [rendering, setRendering] = useState(false);
  const [renderResult, setRenderResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const list = await api.getTemplates();
      setTemplates(list);
    } catch (err) {
      console.error('Failed to load templates:', err);
    }
  };

  // Auto update sample presets when template changes
  const handleSelectTemplate = (tmplId) => {
    setSelectedTemplateId(tmplId);
    if (tmplId === '01_PROPERTY_PROBLEM') {
      setBadgeText('DILEMA SALES PROPERTI');
      setHeadline('LEADS IKLAN MASUK, TAPI SALES LAMBAT FOLLOW-UP?');
      setHighlightWords('LAMBAT FOLLOW-UP');
      setSubheadline('Setiap menit keterlambatan bisa membuat prospek berpindah ke kompetitor.');
      setCtaText('Pelajari Solusinya →');
    } else if (tmplId === '02_PROPERTY_INSIGHT') {
      setBadgeText('MARKET INSIGHT');
      setHeadline('KENAPA BIAYA IKLAN PROPERTI MAHAL TAPI CLOSING RENDAH?');
      setHighlightWords('CLOSING RENDAH');
      setSubheadline('Bukan iklannya yang salah, tapi funnel konversi WhatsApp yang bocor.');
      setCtaText('Simpan Postingan Ini ↗');
    } else if (tmplId === '03_NUMBER_LIST') {
      setBadgeText('5 POIN KRUSIAL');
      setHeadline('5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI');
      setHighlightWords('KESALAHAN FATAL');
      setBulletPoints('Respon di atas 15 menit menurunkan closing 80%\nTemplate chat kaku tanpa nama prospek\nTidak membuat janji temu survey yang jelas');
      setCtaText('Baca Selengkapnya di Caption ↓');
    } else if (tmplId === '04_CASE_STUDY') {
      setBadgeText('STUDI KASUS & HASIL');
      setHeadline('TRANSFORMASI RESPONSE TIME LEADS GREN PROPERTYKOST');
      setHighlightWords('TRANSFORMASI RESPONSE TIME');
      setMetricValue('+300% Speed');
      setMetricLabel('Waktu Respon & Janji Survey');
      setCtaText('Konsultasi Strategi →');
    } else if (tmplId === '05_PRODUCT_SOLUTION') {
      setBadgeText('SOLUSI SISTEM');
      setHeadline('OTOMASI DISTRIBUSI LEADS PROPERTI LANGSUNG KE SALES');
      setHighlightWords('OTOMASI DISTRIBUSI LEADS');
      setSubheadline('Sistem routing cerdas mencegah leads terabaikan dan meningkatkan closing.');
      setCtaText('Lihat Demo Sistem →');
    } else if (tmplId === '06_CALL_TO_ACTION') {
      setBadgeText('SLOT TERBATAS');
      setHeadline('KONSULTASI AUDIT SISTEM MARKETING PROPERTI ANDA');
      setHighlightWords('AUDIT SISTEM MARKETING');
      setSubheadline('Dapatkan roadmap perbaikan funnel iklan properti dalam 45 menit.');
      setCtaText('HUBUNGI VIA WHATSAPP ➔');
    }
  };

  const handleRender = async (e) => {
    if (e) e.preventDefault();
    if (!headline.trim()) return;

    setRendering(true);
    setError(null);

    try {
      const parsedHighlights = highlightWords
        .split(',')
        .map(w => w.trim())
        .filter(w => w.length > 0);

      const parsedBullets = bulletPoints
        .split('\n')
        .map(b => b.trim())
        .filter(b => b.length > 0);

      const payload = {
        template_id: selectedTemplateId,
        width: dimension.width,
        height: dimension.height,
        headline,
        highlight_words: parsedHighlights,
        subheadline,
        badge_text: badgeText,
        bullet_points: parsedBullets,
        metric_value: metricValue,
        metric_label: metricLabel,
        cta_text: ctaText,
        brand_name: 'NugiProperti',
        show_logo: true
      };

      const result = await api.renderTemplate(payload);
      setRenderResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setRendering(false);
    }
  };

  // Render initial preview on mount
  useEffect(() => {
    handleRender();
  }, [selectedTemplateId, dimension]);

  return (
    <div className="page-body">
      <div style={{ marginBottom: '22px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={22} color="var(--accent-cyan)" />
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Design Intelligence & Template Studio</h2>
        </div>
        <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
          Studio rendering deterministik berbasis Design DNA NugiProperti (1080x1350 Instagram Portrait & 1080x1080).
        </p>
      </div>

      {/* 1. Template Selector Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '12px', marginBottom: '24px' }}>
        {templates.map(t => {
          const isSelected = selectedTemplateId === t.template_id;
          return (
            <div
              key={t.template_id}
              className="card"
              onClick={() => handleSelectTemplate(t.template_id)}
              style={{
                cursor: 'pointer',
                padding: '14px',
                borderColor: isSelected ? 'var(--accent-cyan)' : 'var(--border-card)',
                background: isSelected ? 'rgba(56, 189, 248, 0.12)' : 'var(--bg-card)',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ fontSize: '0.72rem', fontWeight: 800, color: isSelected ? 'var(--accent-cyan)' : 'var(--text-dim)' }}>
                  {t.template_id.slice(0, 2)}
                </span>
                <span className={`badge ${isSelected ? 'badge-info' : 'badge-secondary'}`} style={{ fontSize: '0.64rem' }}>
                  {t.accent_scheme.toUpperCase()}
                </span>
              </div>
              <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#fff', marginBottom: '4px' }}>{t.name}</h4>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)', lineClamp: 2, display: '-webkit-box', WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {t.purpose}
              </p>
            </div>
          );
        })}
      </div>

      {/* 2. Main Studio Work Area */}
      <div style={{ display: 'grid', gridTemplateColumns: '460px 1fr', gap: '26px', alignItems: 'start' }}>
        {/* Left: Interactive Controlled Form */}
        <div className="card">
          <form onSubmit={handleRender}>
            {/* Format Selector */}
            <div className="form-group">
              <label className="form-label">Format Canvas Instagram</label>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  type="button"
                  className={`btn btn-sm ${dimension.height === 1350 ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ flex: 1 }}
                  onClick={() => setDimension({ width: 1080, height: 1350, label: '1080 x 1350 (Portrait Feed 4:5)' })}
                >
                  📱 1080 x 1350 (4:5 Portrait)
                </button>
                <button
                  type="button"
                  className={`btn btn-sm ${dimension.height === 1080 ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ flex: 1 }}
                  onClick={() => setDimension({ width: 1080, height: 1080, label: '1080 x 1080 (Square 1:1)' })}
                >
                  ⏹️ 1080 x 1080 (1:1 Square)
                </button>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Category Badge Text</label>
              <input
                type="text"
                className="form-input"
                value={badgeText}
                onChange={(e) => setBadgeText(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Headline Visual Utama *</label>
              <textarea
                className="form-textarea"
                rows={3}
                value={headline}
                onChange={(e) => setHeadline(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Highlight Words (Kata Sorotan Berwarna)</label>
              <input
                type="text"
                className="form-input"
                placeholder="Contoh: LAMBAT FOLLOW-UP, CLOSING RENDAH"
                value={highlightWords}
                onChange={(e) => setHighlightWords(e.target.value)}
              />
              <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                Pisahkan dengan koma atau gunakan tanda *bintang* pada teks headline.
              </span>
            </div>

            {selectedTemplateId !== '03_NUMBER_LIST' && selectedTemplateId !== '04_CASE_STUDY' && (
              <div className="form-group">
                <label className="form-label">Subheadline / Supporting Insight</label>
                <textarea
                  className="form-textarea"
                  rows={2}
                  value={subheadline}
                  onChange={(e) => setSubheadline(e.target.value)}
                />
              </div>
            )}

            {selectedTemplateId === '03_NUMBER_LIST' && (
              <div className="form-group">
                <label className="form-label">Daftar Poin Krusial (1 baris = 1 poin)</label>
                <textarea
                  className="form-textarea"
                  rows={3}
                  value={bulletPoints}
                  onChange={(e) => setBulletPoints(e.target.value)}
                />
              </div>
            )}

            {selectedTemplateId === '04_CASE_STUDY' && (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <div className="form-group">
                  <label className="form-label">Metric Value</label>
                  <input type="text" className="form-input" value={metricValue} onChange={(e) => setMetricValue(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Metric Label</label>
                  <input type="text" className="form-input" value={metricLabel} onChange={(e) => setMetricLabel(e.target.value)} />
                </div>
              </div>
            )}

            <div className="form-group">
              <label className="form-label">Call to Action (CTA) Button</label>
              <input
                type="text"
                className="form-input"
                value={ctaText}
                onChange={(e) => setCtaText(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
              <button type="submit" className="btn btn-primary" disabled={rendering} style={{ width: '100%' }}>
                {rendering ? <RefreshCw size={16} className="spin" /> : <Sparkles size={16} />}
                <span>{rendering ? 'Rendering Graphic...' : 'Render Preview Graphic'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Right: Live Graphic Preview & Visual QA Card */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {error && (
            <div className="card" style={{ borderColor: 'var(--accent-rose)', color: 'var(--accent-rose)' }}>
              {error}
            </div>
          )}

          {renderResult && (
            <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
              {/* Graphic Canvas Display */}
              <div style={{ width: '380px', flexShrink: 0, background: '#04070d', borderRadius: 'var(--radius-lg)', padding: '10px', border: '1px solid var(--border-highlight)', boxShadow: 'var(--shadow-lg)' }}>
                <img
                  src={renderResult.asset_url}
                  alt="Rendered Instagram Graphic"
                  style={{ width: '100%', borderRadius: 'var(--radius-md)', display: 'block' }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '10px', padding: '0 4px' }}>
                  <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>
                    {renderResult.render_metadata.width} × {renderResult.render_metadata.height} ({renderResult.render_metadata.aspect_ratio})
                  </span>
                  <a
                    href={renderResult.asset_url}
                    download={`nugiproperti_${selectedTemplateId.toLowerCase()}_${dimension.height}.png`}
                    className="btn btn-secondary btn-sm"
                  >
                    <Download size={14} />
                    <span>Download PNG</span>
                  </a>
                </div>
              </div>

              {/* Visual QA Intelligence Card */}
              <div style={{ flex: 1 }} className="card">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 800 }}>Visual QA Score</h3>
                  <span className={`badge ${renderResult.visual_qa.score >= 85 ? 'badge-success' : 'badge-warning'}`} style={{ fontSize: '0.85rem', padding: '4px 12px' }}>
                    <ShieldCheck size={14} />
                    <span>{renderResult.visual_qa.score} / 100</span>
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '16px' }}>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: 'var(--radius-sm)', fontSize: '0.78rem' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Readability: </span>
                    <strong style={{ color: 'var(--accent-emerald)' }}>{renderResult.visual_qa.readability}</strong>
                  </div>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: 'var(--radius-sm)', fontSize: '0.78rem' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Hierarchy: </span>
                    <strong style={{ color: 'var(--accent-cyan)' }}>{renderResult.visual_qa.hierarchy}</strong>
                  </div>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: 'var(--radius-sm)', fontSize: '0.78rem' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Safe Area: </span>
                    <strong style={{ color: 'var(--accent-emerald)' }}>COMPLIANT</strong>
                  </div>
                  <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: 'var(--radius-sm)', fontSize: '0.78rem' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Latency: </span>
                    <strong style={{ color: '#fff' }}>{renderResult.render_metadata.render_latency_ms} ms</strong>
                  </div>
                </div>

                {renderResult.visual_qa.issues.length > 0 ? (
                  <div style={{ marginBottom: '12px' }}>
                    <p style={{ fontSize: '0.76rem', color: 'var(--accent-amber)', fontWeight: 700, marginBottom: '6px' }}>Catatan Perbaikan:</p>
                    <ul style={{ paddingLeft: '18px', fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                      {renderResult.visual_qa.issues.map((iss, i) => <li key={i}>{iss}</li>)}
                    </ul>
                  </div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-emerald)', fontSize: '0.8rem' }}>
                    <CheckCircle2 size={15} />
                    <span>Seluruh kriteria Design DNA & safe area terpenuhi sempurna!</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
