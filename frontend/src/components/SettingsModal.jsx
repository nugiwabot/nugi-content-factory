import React, { useState, useEffect } from 'react';
import { 
  X, Server, HardDrive, ShieldAlert, Sparkles, RefreshCw, 
  CheckCircle2, AlertTriangle, MessageSquare, Image as ImageIcon,
  Save, Sliders, Zap
} from 'lucide-react';
import { api } from '../services/api';

export default function SettingsModal({ isOpen, onClose, healthStatus }) {
  const [activeTab, setActiveTab] = useState('llm');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Form states
  const [llmConfig, setLlmConfig] = useState({
    provider: 'openrouter',
    base_url: 'https://openrouter.ai/api/v1',
    api_key: '',
    model: 'google/gemini-2.5-flash-lite'
  });

  const [imageConfig, setImageConfig] = useState({
    provider: 'flux',
    endpoint_url: 'https://api.bfl.ai/v1',
    api_key: '',
    model: 'flux-2-klein-9b'
  });

  // Test states
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  // Knowledge source
  const [knowledgeStatus, setKnowledgeStatus] = useState(null);
  const [knowledgePath, setKnowledgePath] = useState('');
  const [knowledgeMsg, setKnowledgeMsg] = useState(null);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
      loadKnowledgeSource();
      setTestResult(null);
      setSaveSuccess(false);
    }
  }, [isOpen]);

  const loadKnowledgeSource = async () => {
    try {
      const data = await api.getKnowledgeSource();
      setKnowledgeStatus(data);
      setKnowledgePath(data.source_path || '');
    } catch (err) {
      console.error('Failed to load knowledge source:', err);
    }
  };

  const saveKnowledgeSource = async () => {
    try {
      setKnowledgeMsg(null);
      await api.setKnowledgeSource(knowledgePath.trim());
      await loadKnowledgeSource();
      setKnowledgeMsg({ ok: true, text: 'Sumber pengetahuan berhasil disimpan & diindeks ulang.' });
    } catch (err) {
      setKnowledgeMsg({ ok: false, text: err.message || 'Gagal menyimpan sumber pengetahuan.' });
    }
  };

  const loadSettings = async () => {
    try {
      setLoading(true);
      const data = await api.getProviderSettings();
      if (data.llm) {
        setLlmConfig(prev => ({
          ...prev,
          provider: data.llm.provider || 'openrouter',
          base_url: data.llm.base_url || '',
          api_key: data.llm.api_key || '',
          model: data.llm.model || ''
        }));
      }
      if (data.image) {
        setImageConfig(prev => ({
          ...prev,
          provider: data.image.provider || 'flux',
          endpoint_url: data.image.endpoint_url || '',
          api_key: data.image.api_key || '',
          model: data.image.model || ''
        }));
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setSaveSuccess(false);
      await api.updateProviderSettings({
        llm: llmConfig,
        image: imageConfig
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      alert('Gagal menyimpan konfigurasi: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async (category) => {
    setTesting(true);
    setTestResult(null);
    try {
      let payload = { category };
      if (category === 'llm') {
        payload = { ...payload, ...llmConfig };
      } else if (category === 'image') {
        payload = { ...payload, ...imageConfig };
      }

      const res = await api.testProviderConnection(payload);
      setTestResult(res);
    } catch (err) {
      setTestResult({
        status: 'FAILED',
        category,
        provider: 'Unknown',
        message: err.message || 'Gagal menghubungi endpoint provider.'
      });
    } finally {
      setTesting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-card" style={{ maxWidth: '640px', width: '90%' }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={20} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Model Provider Architecture</h3>
          </div>
          <button className="btn btn-secondary btn-icon-only" onClick={onClose}><X size={16} /></button>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '6px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '10px', marginBottom: '16px' }}>
          <button 
            className={`btn btn-sm ${activeTab === 'llm' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => { setActiveTab('llm'); setTestResult(null); }}
          >
            <MessageSquare size={14} />
            <span>LLM Provider</span>
          </button>
          <button 
            className={`btn btn-sm ${activeTab === 'image' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => { setActiveTab('image'); setTestResult(null); }}
          >
            <ImageIcon size={14} />
            <span>Image Provider</span>
          </button>
          <button 
            className={`btn btn-sm ${activeTab === 'system' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => { setActiveTab('system'); setTestResult(null); }}
          >
            <Server size={14} />
            <span>Storage & System</span>
          </button>
        </div>

        {/* Tab 1: LLM Provider */}
        {activeTab === 'llm' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="form-group">
              <label className="form-label">LLM Provider Vendor</label>
              <select 
                className="form-select"
                value={llmConfig.provider}
                onChange={(e) => setLlmConfig({ ...llmConfig, provider: e.target.value })}
              >
                <option value="openrouter">OpenRouter Gateway (Gemini, Claude, DeepSeek)</option>
                <option value="openai">OpenAI / OpenAI-Compatible (vLLM, Ollama, Groq)</option>
                <option value="anthropic">Anthropic Messages API (Claude 3.5)</option>
                <option value="google">Google Gemini Direct API</option>
                <option value="custom">Custom REST Endpoint</option>
                <option value="mock">Mock Offline Provider (Testing)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Base URL / Endpoint</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="https://openrouter.ai/api/v1"
                value={llmConfig.base_url || ''}
                onChange={(e) => setLlmConfig({ ...llmConfig, base_url: e.target.value })}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div className="form-group">
                <label className="form-label">API Key</label>
                <input 
                  type="password" 
                  className="form-input" 
                  placeholder="sk-..."
                  value={llmConfig.api_key || ''}
                  onChange={(e) => setLlmConfig({ ...llmConfig, api_key: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Model Identifier</label>
                <input 
                  type="text" 
                  className="form-input" 
                  placeholder="google/gemini-2.5-flash-lite"
                  value={llmConfig.model || ''}
                  onChange={(e) => setLlmConfig({ ...llmConfig, model: e.target.value })}
                />
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-start', marginTop: '6px' }}>
              <button 
                className="btn btn-secondary btn-sm"
                disabled={testing}
                onClick={() => handleTest('llm')}
              >
                <RefreshCw size={13} className={testing ? 'spin' : ''} />
                <span>{testing ? 'Testing Connection...' : 'Test LLM Connection'}</span>
              </button>
            </div>
          </div>
        )}

        {/* Tab 2: Image Provider */}
        {activeTab === 'image' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="form-group">
              <label className="form-label">Image Provider Engine</label>
              <select 
                className="form-select"
                value={imageConfig.provider}
                onChange={(e) => setImageConfig({ ...imageConfig, provider: e.target.value })}
              >
                <option value="flux">Flux / Black Forest Labs API (Primary)</option>
                <option value="openai">OpenAI DALL-E / OpenRouter Image API</option>
                <option value="custom">Custom WebUI / ComfyUI / SD Endpoint</option>
                <option value="mock">Mock Image Provider (Testing)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">API Endpoint / Base URL</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="https://api.bfl.ai/v1"
                value={imageConfig.endpoint_url || ''}
                onChange={(e) => setImageConfig({ ...imageConfig, endpoint_url: e.target.value })}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div className="form-group">
                <label className="form-label">API Key</label>
                <input 
                  type="password" 
                  className="form-input" 
                  placeholder="bfl_..."
                  value={imageConfig.api_key || ''}
                  onChange={(e) => setImageConfig({ ...imageConfig, api_key: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Model Identifier</label>
                <input 
                  type="text" 
                  className="form-input" 
                  placeholder="flux-2-klein-9b"
                  value={imageConfig.model || ''}
                  onChange={(e) => setImageConfig({ ...imageConfig, model: e.target.value })}
                />
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-start', marginTop: '6px' }}>
              <button 
                className="btn btn-secondary btn-sm"
                disabled={testing}
                onClick={() => handleTest('image')}
              >
                <RefreshCw size={13} className={testing ? 'spin' : ''} />
                <span>{testing ? 'Testing Connection...' : 'Test Image Connection'}</span>
              </button>
            </div>
          </div>
        )}

        {/* Tab 3: System & Storage */}
        {activeTab === 'system' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <Server size={15} color="var(--accent-cyan)" />
                <strong style={{ fontSize: '0.85rem' }}>Backend Server Status</strong>
              </div>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', margin: 0 }}>
                Environment: <span style={{ color: '#fff', fontWeight: 600 }}>{healthStatus?.environment || 'development'}</span> | Status: <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>{healthStatus?.status || 'Online'}</span>
              </p>
            </div>

            <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <HardDrive size={15} color="var(--accent-emerald)" />
                <strong style={{ fontSize: '0.85rem' }}>Local Asset Storage</strong>
              </div>
              <p style={{ fontSize: '0.76rem', color: 'var(--text-dim)', wordBreak: 'break-all', margin: 0 }}>
                Path: {healthStatus?.storage?.path || './storage/assets'}
              </p>
            </div>

            <div className="card" style={{ background: 'rgba(0,0,0,0.3)', padding: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <Zap size={15} color="var(--accent-violet)" />
                <strong style={{ fontSize: '0.85rem' }}>Knowledge Source (freelance-nugi-software-engineer)</strong>
              </div>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)', margin: '4px 0 8px' }}>
                Folder repo bisnis yang dibaca sebagai sumber pengetahuan konten. File privat (data sales, keuangan) otomatis dikecualikan.
              </p>
              <input
                type="text"
                className="form-input"
                placeholder="C:\Users\...\freelance-nugi-software-engineer"
                value={knowledgePath}
                onChange={(e) => setKnowledgePath(e.target.value)}
              />
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginTop: '8px' }}>
                <button className="btn btn-secondary btn-sm" onClick={saveKnowledgeSource} disabled={saving}>
                  Simpan & Indeks
                </button>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={async () => {
                    try {
                      const data = await api.rescanKnowledge();
                      setKnowledgeStatus(data);
                      setKnowledgeMsg({ ok: true, text: 'Sumber pengetahuan diindeks ulang.' });
                    } catch (err) {
                      setKnowledgeMsg({ ok: false, text: err.message });
                    }
                  }}
                >
                  <RefreshCw size={13} /> Rescan
                </button>
                {knowledgeStatus?.active && (
                  <span style={{ fontSize: '0.72rem', color: 'var(--accent-emerald)' }}>
                    ✓ {knowledgeStatus.core_docs} core · {knowledgeStatus.supporting_docs} pendukung
                  </span>
                )}
                {knowledgeStatus && !knowledgeStatus.active && (
                  <span style={{ fontSize: '0.72rem', color: 'var(--accent-rose)' }}>Sumber tidak ditemukan</span>
                )}
              </div>
              {knowledgeMsg && (
                <p style={{ fontSize: '0.74rem', margin: '6px 0 0', color: knowledgeMsg.ok ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                  {knowledgeMsg.text}
                </p>
              )}
            </div>

            <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start', background: 'rgba(56, 189, 248, 0.08)', padding: '10px', borderRadius: 'var(--radius-md)', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
              <ShieldAlert size={15} color="var(--accent-cyan)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.4, margin: 0 }}>
                Kunci API disimpan lokal dalam bentuk teks biasa di folder data aplikasi Anda dan hanya dikirim ke provider yang dituju.
              </p>
            </div>
          </div>
        )}

        {/* Live Test Result Banner */}
        {testResult && (
          <div style={{ 
            marginTop: '12px', 
            padding: '10px 12px', 
            borderRadius: 'var(--radius-sm)', 
            fontSize: '0.76rem', 
            background: testResult.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.12)' : 'rgba(244, 63, 94, 0.12)',
            border: `1px solid ${testResult.status === 'SUCCESS' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`,
            color: testResult.status === 'SUCCESS' ? 'var(--accent-emerald)' : 'var(--accent-rose)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700 }}>
                {testResult.status === 'SUCCESS' ? <CheckCircle2 size={14} /> : <AlertTriangle size={14} />}
                <span>{testResult.provider}: {testResult.status}</span>
              </div>
              {testResult.latency_ms && (
                <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>{testResult.latency_ms} ms</span>
              )}
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.74rem', margin: 0 }}>{testResult.message}</p>
          </div>
        )}

        {/* Footer Actions */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px', paddingTop: '12px', borderTop: '1px solid var(--border-subtle)' }}>
          <div>
            {saveSuccess && (
              <span style={{ color: 'var(--accent-emerald)', fontSize: '0.78rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle2 size={14} /> Konfigurasi berhasil disimpan!
              </span>
            )}
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn btn-secondary" onClick={onClose}>Tutup</button>
            <button 
              className="btn btn-primary" 
              disabled={saving}
              onClick={handleSave}
            >
              <Save size={14} />
              <span>{saving ? 'Menyimpan...' : 'Simpan Pengaturan'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
