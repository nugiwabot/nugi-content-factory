import React, { useState } from 'react';
import { Plus, Palette } from 'lucide-react';
import { api } from '../services/api';

export default function BrandProfileManager({ brands, onBrandCreated }) {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [primaryColor, setPrimaryColor] = useState('#0f172a');
  const [secondaryColor, setSecondaryColor] = useState('#38bdf8');
  const [accentColor, setAccentColor] = useState('#10b981');
  const [fontFamily, setFontFamily] = useState('sans-serif');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const newBrand = await api.createBrandProfile({
        name,
        primary_color: primaryColor,
        secondary_color: secondaryColor,
        accent_color: accentColor,
        font_family: fontFamily
      });
      setShowModal(false);
      setName('');
      onBrandCreated(newBrand);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-body">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Brand Profiles & Identitas Visual</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Atur palet warna, tipografi, dan identitas brand agar setiap visual yang dirender selalu konsisten.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} />
          <span>Tambah Brand Profile</span>
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '18px' }}>
        {brands.map(b => (
          <div key={b.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Palette size={20} color="var(--accent-cyan)" />
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{b.name}</h3>
            </div>

            <div>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginBottom: '8px' }}>Palet Warna Brand:</p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <div style={{ flex: 1, height: '32px', borderRadius: 'var(--radius-sm)', background: b.primary_color, border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', color: '#fff' }}>
                  {b.primary_color}
                </div>
                <div style={{ flex: 1, height: '32px', borderRadius: 'var(--radius-sm)', background: b.secondary_color, border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', color: '#000' }}>
                  {b.secondary_color}
                </div>
                <div style={{ flex: 1, height: '32px', borderRadius: 'var(--radius-sm)', background: b.accent_color, border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', color: '#fff' }}>
                  {b.accent_color}
                </div>
              </div>
            </div>

            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Font Family: <span style={{ color: '#fff', fontWeight: 600 }}>{b.font_family}</span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '16px' }}>Tambah Brand Profile Baru</h3>
            {error && <div style={{ color: 'var(--accent-rose)', fontSize: '0.84rem', marginBottom: '12px' }}>{error}</div>}

            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Nama Brand / Agensi *</label>
                <input 
                  type="text" 
                  className="form-input" 
                  placeholder="Contoh: NugiProperti Studio"
                  value={name} 
                  onChange={(e) => setName(e.target.value)} 
                  required 
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                <div className="form-group">
                  <label className="form-label">Warna Utama</label>
                  <input type="color" className="form-input" style={{ height: '42px', padding: '2px' }} value={primaryColor} onChange={(e) => setPrimaryColor(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Warna Aksen 1</label>
                  <input type="color" className="form-input" style={{ height: '42px', padding: '2px' }} value={secondaryColor} onChange={(e) => setSecondaryColor(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Warna Aksen 2</label>
                  <input type="color" className="form-input" style={{ height: '42px', padding: '2px' }} value={accentColor} onChange={(e) => setAccentColor(e.target.value)} />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Font Family</label>
                <select className="form-select" value={fontFamily} onChange={(e) => setFontFamily(e.target.value)}>
                  <option value="sans-serif">Modern Sans-Serif (Default)</option>
                  <option value="serif">Classic Editorial Serif</option>
                  <option value="monospace">Tech Monospace</option>
                </select>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Batal</button>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Menyimpan...' : 'Simpan Profile'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
