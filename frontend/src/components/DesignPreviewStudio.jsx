import React, { useState, useEffect } from 'react';
import { Sparkles, Download, CheckCircle2, ShieldCheck, RefreshCw, Layers, Compass, Image as ImageIcon } from 'lucide-react';
import { api } from '../services/api';

export default function DesignPreviewStudio() {
  const [activeEngine, setActiveEngine] = useState('editorial'); // 'editorial' (Phase 3A) or 'templates' (Phase 2)
  const [compositions, setCompositions] = useState([]);
  const [selectedCompType, setSelectedCompType] = useState('HERO_IMAGE_EDITORIAL');
  const [templates, setTemplates] = useState([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState('01_PROPERTY_PROBLEM');
  
  const [dimension, setDimension] = useState({ width: 1080, height: 1350, label: '1080 x 1350 (Portrait Feed 4:5)' });
  const [ctaStrategy, setCtaStrategy] = useState('CTA_NONE'); // CTA_NONE, CTA_OPTIONAL, CTA_REQUIRED

  // Form Inputs
  const [headline, setHeadline] = useState('KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?');
  const [highlightWords, setHighlightWords] = useState('HARGA RUMAH, NAIK LEBIH CEPAT');
  const [subheadline, setSubheadline] = useState('Lokasi bukan hanya soal jarak. Aksesibilitas dan perkembangan kawasan ikut memengaruhi nilai apresiasi properti.');
  const [badgeText, setBadgeText] = useState('EDUKASI PROPERTI');
  const [bulletPoints, setBulletPoints] = useState('Akses gerbang tol < 5 menit\nPusat bisnis terpadu\nKawasan bebas banjir');
  const [metricValue, setMetricValue] = useState('+300%');
  const [metricLabel, setMetricLabel] = useState('Pertumbuhan Nilai Kawasan');
  const [ctaText, setCtaText] = useState('Pelajari Solusinya →');
  const [authorName, setAuthorName] = useState('Tim Riset NugiProperti');
  const [propertyLocation, setPropertyLocation] = useState('Jatinangor, Sumedang');
  const [propertyPrice, setPropertyPrice] = useState('Mulai Rp 1,85 Miliar');
  const [propertyFeatures, setPropertyFeatures] = useState('16 Kamar Kost, Yield 12%/thn, SHM Siap, Full Furnished');

  const [rendering, setRendering] = useState(false);
  const [renderResult, setRenderResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [compList, tmplList] = await Promise.all([
        api.getEditorialCompositions().catch(() => []),
        api.getTemplates().catch(() => [])
      ]);
      setCompositions(compList);
      setTemplates(tmplList);
    } catch (err) {
      console.error('Failed to load studio data:', err);
    }
  };

  const handleSelectComposition = (cId) => {
    setSelectedCompType(cId);
    if (cId === 'HERO_IMAGE_EDITORIAL') {
      setBadgeText('EDUKASI PROPERTI');
      setHeadline('KENAPA HARGA RUMAH DI DEKAT TOL BISA NAIK LEBIH CEPAT?');
      setHighlightWords('HARGA RUMAH, NAIK LEBIH CEPAT');
      setSubheadline('Lokasi bukan hanya soal jarak. Aksesibilitas dan aktivitas ekonomi mempercepat apresiasi modal properti.');
      setCtaStrategy('CTA_NONE');
    } else if (cId === 'CINEMATIC_OVERLAY') {
      setBadgeText('MARKET INTELLIGENCE');
      setHeadline('BIAYA IKLAN PROPERTI MAHAL BUKAN KARENA ALGORITMA META');
      setHighlightWords('BUKAN KARENA ALGORITMA');
      setSubheadline('Penyebab utama CPA membengkak adalah penawaran unit yang generik dan respons follow-up tim sales yang lambat.');
      setCtaStrategy('CTA_NONE');
    } else if (cId === 'DATA_EDITORIAL') {
      setBadgeText('DATA & STATISTIK');
      setHeadline('HASIL TRANSFORMASI RESPONSE TIME LEADS GREN PROPERTYKOST');
      setHighlightWords('TRANSFORMASI RESPONSE TIME');
      setMetricValue('+300%');
      setMetricLabel('Kecepatan Respon & Janji Survey');
      setSubheadline('Sistem routing pesan instan berhasil meningkatkan konversi janji survey mahasiswa sebesar 300% dalam 60 hari.');
      setCtaStrategy('CTA_NONE');
    } else if (cId === 'LIST_EDITORIAL') {
      setBadgeText('POIN KRUSIAL');
      setHeadline('5 KESALAHAN FATAL FOLLOW-UP LEADS PROPERTI');
      setHighlightWords('KESALAHAN FATAL');
      setBulletPoints('Respon di atas 15 menit menurunkan closing 80%\nTemplate pesan chat kaku tanpa personalisasi\nTidak mengunci janji temu survey lokasi');
      setCtaStrategy('CTA_NONE');
    } else if (cId === 'PROPERTY_SHOWCASE') {
      setBadgeText('PORTFOLIO UNIT');
      setHeadline('RUKOST PREMIUM DEKAT KAMPUS UNPAD JATINANGOR');
      setHighlightWords('RUKOST PREMIUM, UNPAD JATINANGOR');
      setPropertyLocation('Jatinangor, Sumedang');
      setPropertyPrice('Mulai Rp 1,85 Miliar');
      setCtaStrategy('CTA_OPTIONAL');
      setCtaText('Jadwalkan Survey →');
    } else if (cId === 'MINIMAL_EDITORIAL') {
      setBadgeText('PERSPEKTIF');
      setHeadline('DEVELOPER YANG MENOLAK OTOMASI AKAN TERGANTIKAN OLEH YANG MEMANFAATKANNYA');
      setHighlightWords('OTOMASI');
      setSubheadline('Pasar properti generasi baru menuntut respons instan dan pengalaman digital yang transparan.');
      setAuthorName('Tim Riset NugiProperti');
      setCtaStrategy('CTA_NONE');
    }
  };

  const handleRender = async (e) => {
    if (e) e.preventDefault();
    if (!headline.trim()) return;

    setRendering(true);
    setError(null);

    try {
      const parsedHighlights = highlightWords.split(',').map(w => w.trim()).filter(w => w.length > 0);
      const parsedBullets = bulletPoints.split('\n').map(b => b.trim()).filter(b => b.length > 0);
      const parsedFeatures = propertyFeatures.split(',').map(f => f.trim()).filter(f => f.length > 0);

      const payload = {
        composition_type: selectedCompType,
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
        cta_strategy: ctaStrategy,
        cta_text: ctaText,
        author_name: authorName,
        property_location: propertyLocation,
        property_price: propertyPrice,
        property_features: parsedFeatures,
        brand_name: 'NugiProperti',
        show_logo: true
      };

      const result = activeEngine === 'editorial' 
        ? await api.renderEditorial(payload)
        : await api.renderTemplate(payload);

      setRenderResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setRendering(false);
    }
  };

  useEffect(() => {
    handleRender();
  }, [selectedCompType, selectedTemplateId, dimension, activeEngine, ctaStrategy]);

  return (
    <div className="page-body">
      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Compass size={24} color="var(--accent-cyan)" />
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Editorial Visual Composition Engine</h2>
            <span className="badge badge-info" style={{ fontSize: '0.72rem' }}>Phase 3A Active</span>
          </div>

          {/* Engine Mode Toggle */}
          <div style={{ display: 'flex', gap: '6px', background: 'rgba(0,0,0,0.4)', padding: '4px', borderRadius: 'var(--radius-md)' }}>
            <button
              className={`btn btn-sm ${activeEngine === 'editorial' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveEngine('editorial')}
            >
              ✦ Editorial Engine (7 Archetypes)
            </button>
            <button
              className={`btn btn-sm ${activeEngine === 'templates' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveEngine('templates')}
            >
              📄 Templates (Phase 2)
            </button>
          </div>
        </div>
        <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Transformasi konten properti menjadi visual editorial berkelas media profesional (1080x1350 Instagram Portrait).
        </p>
      </div>

      {/* Composition Archetype Cards */}
      {activeEngine === 'editorial' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '10px', marginBottom: '22px' }}>
          {compositions.map(c => {
            const isSelected = selectedCompType === c.id;
            return (
              <div
                key={c.id}
                className="card"
                onClick={() => handleSelectComposition(c.id)}
                style={{
                  cursor: 'pointer',
                  padding: '12px',
                  borderColor: isSelected ? 'var(--accent-cyan)' : 'var(--border-card)',
                  background: isSelected ? 'rgba(56, 189, 248, 0.12)' : 'var(--bg-card)',
                  transition: 'all 0.15s ease'
                }}
              >
                <span style={{ fontSize: '0.64rem', fontWeight: 800, color: isSelected ? 'var(--accent-cyan)' : 'var(--text-dim)' }}>
                  {c.visual_dominance}
                </span>
                <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: '#fff', marginTop: '2px', marginBottom: '2px' }}>{c.name}</h4>
                <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineClamp: 1, display: '-webkit-box', WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                  {c.best_for}
                </p>
              </div>
            );
          })}
        </div>
      )}

      {/* Main Studio Area */}
      <div style={{ display: 'grid', gridTemplateColumns: '460px 1fr', gap: '24px', alignItems: 'start' }}>
        {/* Left Form */}
        <div className="card">
          <form onSubmit={handleRender}>
            {/* Format Selector */}
            <div className="form-group">
              <label className="form-label">Format Canvas Instagram</label>
              <div style={{ display: 'flex', gap: '8px' }}>
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

            {/* CTA Business Rule Selector */}
            <div className="form-group">
              <label className="form-label">CTA Business Rule (Editorial vs Penawaran)</label>
              <div style={{ display: 'flex', gap: '6px' }}>
                <button
                  type="button"
                  className={`btn btn-sm ${ctaStrategy === 'CTA_NONE' ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ flex: 1, fontSize: '0.76rem' }}
                  onClick={() => setCtaStrategy('CTA_NONE')}
                >
                  CTA_NONE (Edukasi/Opini)
                </button>
                <button
                  type="button"
                  className={`btn btn-sm ${ctaStrategy === 'CTA_REQUIRED' ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ flex: 1, fontSize: '0.76rem' }}
                  onClick={() => setCtaStrategy('CTA_REQUIRED')}
                >
                  CTA_REQUIRED (Offer)
                </button>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Category / Eyebrow Badge</label>
              <input type="text" className="form-input" value={badgeText} onChange={(e) => setBadgeText(e.target.value)} />
            </div>

            <div className="form-group">
              <label className="form-label">Headline Editorial Utama *</label>
              <textarea className="form-textarea" rows={3} value={headline} onChange={(e) => setHeadline(e.target.value)} required />
            </div>

            <div className="form-group">
              <label className="form-label">Highlight Words (Kata Sorotan Berwarna)</label>
              <input type="text" className="form-input" value={highlightWords} onChange={(e) => setHighlightWords(e.target.value)} />
            </div>

            <div className="form-group">
              <label className="form-label">Subheadline / Penjelasan Editorial</label>
              <textarea className="form-textarea" rows={2} value={subheadline} onChange={(e) => setSubheadline(e.target.value)} />
            </div>

            {selectedCompType === 'DATA_EDITORIAL' && (
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

            {selectedCompType === 'PROPERTY_SHOWCASE' && (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  <div className="form-group">
                    <label className="form-label">Lokasi Unit</label>
                    <input type="text" className="form-input" value={propertyLocation} onChange={(e) => setPropertyLocation(e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Harga Unit</label>
                    <input type="text" className="form-input" value={propertyPrice} onChange={(e) => setPropertyPrice(e.target.value)} />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Spesifikasi Unit (Pills)</label>
                  <input type="text" className="form-input" value={propertyFeatures} onChange={(e) => setPropertyFeatures(e.target.value)} />
                </div>
              </>
            )}

            {selectedCompType === 'LIST_EDITORIAL' && (
              <div className="form-group">
                <label className="form-label">Poin-Poin Listicle (1 baris = 1 poin)</label>
                <textarea className="form-textarea" rows={3} value={bulletPoints} onChange={(e) => setBulletPoints(e.target.value)} />
              </div>
            )}

            {ctaStrategy === 'CTA_REQUIRED' && (
              <div className="form-group">
                <label className="form-label">CTA Button Text</label>
                <input type="text" className="form-input" value={ctaText} onChange={(e) => setCtaText(e.target.value)} />
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
              <button type="submit" className="btn btn-primary" disabled={rendering} style={{ width: '100%' }}>
                {rendering ? <RefreshCw size={16} className="spin" /> : <Sparkles size={16} />}
                <span>{rendering ? 'Rendering Editorial Visual...' : 'Render Editorial Graphic'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Right Preview */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {error && <div className="card" style={{ borderColor: 'var(--accent-rose)', color: 'var(--accent-rose)' }}>{error}</div>}

          {renderResult && (
            <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
              {/* Graphic Canvas Display */}
              <div style={{ width: '380px', flexShrink: 0, background: '#04070d', borderRadius: 'var(--radius-lg)', padding: '10px', border: '1px solid var(--border-highlight)', boxShadow: 'var(--shadow-lg)' }}>
                <img
                  src={renderResult.asset_url}
                  alt="Rendered Editorial Graphic"
                  style={{ width: '100%', borderRadius: 'var(--radius-md)', display: 'block' }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '10px', padding: '0 4px' }}>
                  <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>
                    {renderResult.render_metadata.width} × {renderResult.render_metadata.height} ({renderResult.render_metadata.aspect_ratio})
                  </span>
                  <a
                    href={renderResult.asset_url}
                    download={`editorial_${selectedCompType.toLowerCase()}_${dimension.height}.png`}
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
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 800 }}>Editorial Visual QA</h3>
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
                    <span style={{ color: 'var(--text-dim)' }}>CTA Strategy: </span>
                    <strong style={{ color: 'var(--accent-emerald)' }}>{renderResult.render_metadata.cta_strategy || 'CTA_NONE'}</strong>
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
                    <span>Komposisi visual editorial memenuhi standar kualitas media profesional!</span>
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
