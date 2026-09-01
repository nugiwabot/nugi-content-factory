import React, { useState } from 'react';
import { Plus, Folder, Calendar } from 'lucide-react';
import { api } from '../services/api';

export default function ProjectView({ projects, onProjectCreated, onSelectProject }) {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const newProj = await api.createProject({ name, description });
      setName('');
      setDescription('');
      setShowModal(false);
      onProjectCreated(newProj);
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
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Project Workspaces</h2>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Kelola workspace pemasaran untuk berbagai proyek properti dan agensi Anda.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} />
          <span>Tambah Project Baru</span>
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '18px' }}>
        {projects.map(proj => (
          <div 
            key={proj.id} 
            className="card" 
            style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '170px' }}
            onClick={() => onSelectProject(proj)}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                <Folder size={20} color="var(--accent-cyan)" />
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>{proj.name}</h3>
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineClamp: 2, display: '-webkit-box', WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {proj.description || 'Tidak ada deskripsi proyek.'}
              </p>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid var(--border-subtle)', paddingTop: '10px' }}>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Calendar size={12} />
                {new Date(proj.created_at).toLocaleDateString('id-ID')}
              </span>
              <span className="badge badge-info">Buka Workspace →</span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '16px' }}>Buat Project Workspace Baru</h3>
            {error && <div style={{ color: 'var(--accent-rose)', fontSize: '0.84rem', marginBottom: '12px' }}>{error}</div>}
            
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Nama Project Properti *</label>
                <input 
                  type="text" 
                  className="form-input" 
                  placeholder="Contoh: GREN Propertykost Jatinangor"
                  value={name} 
                  onChange={(e) => setName(e.target.value)} 
                  required 
                />
              </div>

              <div className="form-group">
                <label className="form-label">Deskripsi / Keterangan</label>
                <textarea 
                  className="form-textarea" 
                  rows={3} 
                  placeholder="Contoh: Kampanye penjualan unit rumah kost mahasiswa 16 kamar dekat UNPAD Jatinangor."
                  value={description} 
                  onChange={(e) => setDescription(e.target.value)} 
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Batal</button>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Menyimpan...' : 'Simpan Project'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
