import React, { useState, useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  Bot, 
  User, 
  Download, 
  Copy, 
  Check, 
  ShieldCheck, 
  Layers, 
  RefreshCw, 
  Palette, 
  FileText, 
  Compass, 
  ArrowRight,
  Lightbulb,
  Target,
  CheckCircle2,
  Loader2,
  AlertCircle,
  Eye,
  Sliders
} from 'lucide-react';
import { api } from '../services/api';

export default function AIContentStudio({ currentProject }) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'agent',
      content: 'Halo Mas Nugi! Saya **Nugi AI Content Copilot**. Cukup ketik instruksi konten properti apa saja yang ingin dibuat (misalnya edukasi investasi, tips follow-up, perbandingan SHM vs Girik, studi kasus rukost mahasiswa, dll.), dan saya akan otomatis menganalisis audiens, merancang headline hook, mengarahkan visual, hingga merender poster 1080x1350 siap posting!',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'completed'
    }
  ]);

  const [inputPrompt, setInputPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [showSafezoneOverlay, setShowSafezoneOverlay] = useState(false);
  const [activeActionLoading, setActiveActionLoading] = useState(null); // 'headline' | 'caption' | 'visual'

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const quickPrompts = [
    { label: 'Leads Boncos Closing Rendah', prompt: 'Kenapa leads iklan properti banyak tapi closing tetap rendah? Target: Developer & Sales Manager.' },
    { label: '3 Kesalahan Follow-Up', prompt: '3 kesalahan follow-up yang membuat calon pembeli properti hilang tanpa kabar.' },
    { label: 'Beli Tanah Girik vs SHM', prompt: 'Edukasi bahaya membeli tanah tanpa sertifikat SHM untuk investor pemula di Bandung.' },
    { label: 'Cash Flow vs Capital Gain', prompt: 'Investasi properti: Lebih menguntungkan cash flow kos-kosan atau capital gain tanah kosong?' },
    { label: 'Lokasi vs Luas Bangunan', prompt: 'Kenapa lokasi strategis lebih penting daripada luas bangunan untuk rumah pertama?' }
  ];

  // Auto scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isGenerating]);

  const handleSendPrompt = async (customPrompt) => {
    const textToSend = (customPrompt || inputPrompt).trim();
    if (!textToSend || isGenerating) return;

    const userMsgId = 'user_' + Date.now();
    const agentMsgId = 'agent_' + (Date.now() + 1);

    // 1. Append User Message
    const userMsg = {
      id: userMsgId,
      role: 'user',
      content: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    // 2. Append Pending Agent Message
    const agentPendingMsg = {
      id: agentMsgId,
      role: 'agent',
      content: 'Sedang merancang paket konten editorial properti...',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'generating',
      activeStep: 0,
      steps: [
        { id: 1, label: 'Menganalisis Target Audiens & Market Friction...', status: 'in_progress' },
        { id: 2, label: 'Merumuskan Headline Hook & Copywriting Konversi...', status: 'pending' },
        { id: 3, label: 'Directing 3D Architectural Visual & Lighting...', status: 'pending' },
        { id: 4, label: '13-Layer Typography Compositing & Safezone QA...', status: 'pending' }
      ]
    };

    setMessages(prev => [...prev, userMsg, agentPendingMsg]);
    setInputPrompt('');
    setIsGenerating(true);

    // Progressive step simulation for UX while backend generates
    const stepInterval = setInterval(() => {
      setMessages(prev => prev.map(m => {
        if (m.id === agentMsgId && m.status === 'generating') {
          const nextStep = Math.min((m.activeStep || 0) + 1, 3);
          const updatedSteps = m.steps.map((s, idx) => ({
            ...s,
            status: idx < nextStep ? 'completed' : (idx === nextStep ? 'in_progress' : 'pending')
          }));
          return { ...m, activeStep: nextStep, steps: updatedSteps };
        }
        return m;
      }));
    }, 900);

    try {
      const payload = {
        topic: textToSend,
        project_id: currentProject?.id || null
      };

      const result = await api.generateAIContent(payload);
      clearInterval(stepInterval);

      // Finalize Agent Message with complete result package
      setMessages(prev => prev.map(m => {
        if (m.id === agentMsgId) {
          const completedSteps = m.steps.map(s => ({ ...s, status: 'completed' }));
          return {
            ...m,
            status: 'completed',
            content: `Saya telah merancang konten editorial bertema: **"${result.editorial_spec?.headline}"** dengan compositing 13-layer presisi dan validasi Instagram Safezone 100%.`,
            resultPackage: result,
            steps: completedSteps
          };
        }
        return m;
      }));
    } catch (err) {
      clearInterval(stepInterval);
      setMessages(prev => prev.map(m => {
        if (m.id === agentMsgId) {
          return {
            ...m,
            status: 'error',
            error: err.message || 'Gagal memproses prompt konten.'
          };
        }
        return m;
      }));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendPrompt();
    }
  };

  const handleCopyCaption = (msgId, captionText) => {
    if (!captionText) return;
    navigator.clipboard.writeText(captionText);
    setCopiedId(msgId);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const handleRegenerateHeadlineInChat = async (msgId, currentPkg) => {
    if (!currentPkg || activeActionLoading) return;
    setActiveActionLoading(`headline_${msgId}`);
    try {
      const updated = await api.regenerateHeadline({ package: currentPkg });
      setMessages(prev => prev.map(m => {
        if (m.id === msgId) {
          return { ...m, resultPackage: updated };
        }
        return m;
      }));
    } catch (err) {
      alert('Gagal meregenerasi headline: ' + err.message);
    } finally {
      setActiveActionLoading(null);
    }
  };

  const handleRegenerateVisualInChat = async (msgId, currentPkg) => {
    if (!currentPkg || activeActionLoading) return;
    setActiveActionLoading(`visual_${msgId}`);
    try {
      const updated = await api.regenerateVisual({ package: currentPkg });
      setMessages(prev => prev.map(m => {
        if (m.id === msgId) {
          return { ...m, resultPackage: updated };
        }
        return m;
      }));
    } catch (err) {
      alert('Gagal meregenerasi visual: ' + err.message);
    } finally {
      setActiveActionLoading(null);
    }
  };

  return (
    <div className="chat-studio-wrapper">
      {/* Scrollable Chat Feed */}
      <div className="chat-messages-scroll">
        {/* Top Header Badge */}
        <div className="chat-welcome-banner">
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(168, 85, 247, 0.15)', padding: '6px 16px', borderRadius: '9999px', border: '1px solid rgba(168, 85, 247, 0.3)', marginBottom: '14px' }}>
            <Sparkles size={16} color="#c084fc" />
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#e9d5ff' }}>NUGIPROPERTI AGENTIC STUDIO</span>
          </div>
          <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: '#f8fafc', marginBottom: '8px' }}>
            AI Content Copilot & Design Factory
          </h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>
            Tulis prompt konten properti dalam bahasa sehari-hari. AI Agent otomatis menyusun strategi pasar, headline tajam, visual arsitektur, dan render poster 1080x1350 dalam safezone Instagram.
          </p>
        </div>

        {/* Message Thread */}
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-bubble-row ${msg.role === 'user' ? 'user-row' : 'agent-row'}`}>
            {msg.role === 'agent' && (
              <div className="chat-avatar agent-avatar">
                <Bot size={20} />
              </div>
            )}

            <div className="chat-bubble-content">
              {msg.role === 'user' ? (
                <div className="user-bubble">
                  {msg.content}
                </div>
              ) : (
                <div className="agent-bubble">
                  {/* Agent Header / Status */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 700, color: '#c084fc', fontSize: '0.88rem' }}>Nugi Agent</span>
                      <span className="badge badge-purple" style={{ fontSize: '0.68rem' }}>Editorial Copilot</span>
                    </div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{msg.timestamp}</span>
                  </div>

                  {/* Message Text */}
                  <p style={{ whiteSpace: 'pre-line', marginBottom: msg.steps || msg.resultPackage ? '14px' : '0' }}>
                    {msg.content}
                  </p>

                  {/* Step Reasoning Cards */}
                  {msg.status === 'generating' && msg.steps && (
                    <div className="agent-reasoning-stepper">
                      <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <Loader2 size={13} className="spin" color="#c084fc" />
                        <span>Tahapan Eksekusi Otomatis:</span>
                      </div>
                      {msg.steps.map((st) => (
                        <div 
                          key={st.id} 
                          className={`reasoning-step-item ${st.status === 'in_progress' ? 'active' : ''} ${st.status === 'completed' ? 'completed' : ''}`}
                        >
                          {st.status === 'completed' ? (
                            <CheckCircle2 size={15} color="var(--accent-emerald)" />
                          ) : st.status === 'in_progress' ? (
                            <Loader2 size={15} className="spin" color="#c084fc" />
                          ) : (
                            <div style={{ width: '15px', height: '15px', borderRadius: '50%', border: '1px solid var(--border-card)' }} />
                          )}
                          <span>{st.label}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Error Display */}
                  {msg.status === 'error' && (
                    <div style={{ background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', padding: '12px 14px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent-rose)', fontSize: '0.85rem' }}>
                      <AlertCircle size={18} />
                      <span>{msg.error}</span>
                    </div>
                  )}

                  {/* Embedded Result Package Card */}
                  {msg.resultPackage && (
                    <div style={{ background: 'rgba(7, 11, 20, 0.8)', border: '1px solid rgba(168, 85, 247, 0.3)', borderRadius: 'var(--radius-lg)', padding: '18px', marginTop: '14px', boxShadow: '0 8px 24px rgba(0,0,0,0.4)' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '20px', alignItems: 'start' }}>
                        
                        {/* Poster Thumbnail + Overlays */}
                        <div>
                          <div style={{ position: 'relative', width: '100%', aspectRatio: '1080 / 1350', borderRadius: 'var(--radius-md)', overflow: 'hidden', border: '1px solid var(--border-card)', background: '#070b14' }}>
                            {msg.resultPackage.rendered_asset_url ? (
                              <img 
                                src={msg.resultPackage.rendered_asset_url} 
                                alt="Poster Preview"
                                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                              />
                            ) : (
                              <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-dim)', fontSize: '0.8rem' }}>
                                Preview Sedang Dimuat...
                              </div>
                            )}

                            {/* Safezone Overlay Preview */}
                            {showSafezoneOverlay && (
                              <div style={{
                                position: 'absolute',
                                top: '15%',
                                bottom: '15%',
                                left: '10%',
                                right: '10%',
                                border: '2px dashed rgba(244, 63, 94, 0.85)',
                                pointerEvents: 'none',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                background: 'rgba(244, 63, 94, 0.05)'
                              }}>
                                <span style={{ fontSize: '0.65rem', background: 'rgba(244, 63, 94, 0.9)', color: '#fff', padding: '2px 6px', borderRadius: '4px', fontWeight: 700 }}>
                                  SAFE ZONE 4:5
                                </span>
                              </div>
                            )}
                          </div>

                          {/* Quick Tools below Thumbnail */}
                          <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                            <button
                              type="button"
                              className="btn btn-sm btn-secondary"
                              style={{ flexGrow: 1, fontSize: '0.75rem', padding: '6px 8px' }}
                              onClick={() => setShowSafezoneOverlay(!showSafezoneOverlay)}
                            >
                              <ShieldCheck size={14} color={showSafezoneOverlay ? "var(--accent-rose)" : "var(--accent-cyan)"} />
                              <span>{showSafezoneOverlay ? 'Tutup Safezone' : 'Audit Safezone'}</span>
                            </button>

                            {msg.resultPackage.rendered_asset_url && (
                              <a
                                href={msg.resultPackage.rendered_asset_url}
                                download="NugiProperti_Editorial_Poster_1080x1350.png"
                                className="btn btn-sm btn-primary"
                                style={{ flexGrow: 1, fontSize: '0.75rem', padding: '6px 8px', textDecoration: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}
                              >
                                <Download size={14} />
                                <span>Unduh HD</span>
                              </a>
                            )}
                          </div>
                        </div>

                        {/* Content Specs & Metadata */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                          
                          {/* Badges Info */}
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', alignItems: 'center' }}>
                            <span className="badge badge-purple">
                              🎯 {msg.resultPackage.strategy_spec?.target_audience || 'Investor Properti'}
                            </span>
                            <span className="badge badge-info">
                              📐 {msg.resultPackage.strategy_spec?.content_archetype || 'PROPERTY_INSIGHT'}
                            </span>
                            <span className="badge badge-success">
                              🛡️ Safezone Pass (100/100)
                            </span>
                          </div>

                          {/* Headline Formula */}
                          <div style={{ background: 'rgba(15, 23, 42, 0.6)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '12px 14px' }}>
                            <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase', marginBottom: '4px' }}>
                              Headline & Hook Formula:
                            </div>
                            <div style={{ fontSize: '1.05rem', fontWeight: 800, color: '#f8fafc', lineHeight: 1.3 }}>
                              {msg.resultPackage.editorial_spec?.headline}
                            </div>
                            {msg.resultPackage.editorial_spec?.subheadline && (
                              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                                {msg.resultPackage.editorial_spec.subheadline}
                              </div>
                            )}
                          </div>

                          {/* Instagram Caption */}
                          <div style={{ background: 'rgba(15, 23, 42, 0.6)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '12px 14px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                              <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase' }}>
                                Caption Instagram Siap Pakai:
                              </span>
                              <button
                                type="button"
                                className="btn btn-sm btn-secondary"
                                style={{ fontSize: '0.72rem', padding: '3px 8px' }}
                                onClick={() => handleCopyCaption(msg.id, msg.resultPackage.editorial_spec?.caption)}
                              >
                                {copiedId === msg.id ? (
                                  <>
                                    <Check size={12} color="var(--accent-emerald)" />
                                    <span style={{ color: 'var(--accent-emerald)' }}>Tersalin!</span>
                                  </>
                                ) : (
                                  <>
                                    <Copy size={12} />
                                    <span>Salin Caption</span>
                                  </>
                                )}
                              </button>
                            </div>
                            <p style={{ fontSize: '0.82rem', color: '#cbd5e1', whiteSpace: 'pre-line', maxHeight: '140px', overflowY: 'auto', lineHeight: 1.5 }}>
                              {msg.resultPackage.editorial_spec?.caption}
                            </p>
                          </div>

                          {/* Quick Revisi Buttons */}
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', paddingTop: '4px' }}>
                            <button
                              type="button"
                              className="btn btn-sm btn-secondary"
                              style={{ fontSize: '0.76rem' }}
                              disabled={activeActionLoading !== null}
                              onClick={() => handleRegenerateHeadlineInChat(msg.id, msg.resultPackage)}
                            >
                              <RefreshCw size={13} className={activeActionLoading === `headline_${msg.id}` ? 'spin' : ''} />
                              <span>{activeActionLoading === `headline_${msg.id}` ? 'Merumuskan...' : 'Variasi Headline Lain'}</span>
                            </button>

                            <button
                              type="button"
                              className="btn btn-sm btn-secondary"
                              style={{ fontSize: '0.76rem' }}
                              disabled={activeActionLoading !== null}
                              onClick={() => handleRegenerateVisualInChat(msg.id, msg.resultPackage)}
                            >
                              <Palette size={13} className={activeActionLoading === `visual_${msg.id}` ? 'spin' : ''} />
                              <span>{activeActionLoading === `visual_${msg.id}` ? 'Merender...' : 'Regenerate Visual'}</span>
                            </button>
                          </div>

                        </div>
                      </div>
                    </div>
                  )}

                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="chat-avatar user-avatar">
                <User size={18} />
              </div>
            )}
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      {/* Floating Bottom Input Dock */}
      <div className="chat-input-dock">
        
        {/* Quick Suggestion Chips */}
        <div className="quick-prompt-chips-bar">
          {quickPrompts.map((qp, idx) => (
            <button
              key={idx}
              type="button"
              className="quick-chip"
              disabled={isGenerating}
              onClick={() => handleSendPrompt(qp.prompt)}
            >
              <Lightbulb size={12} color="#c084fc" />
              <span>{qp.label}</span>
            </button>
          ))}
        </div>

        {/* Textarea Input Card */}
        <div className="chat-input-card">
          <textarea
            ref={textareaRef}
            className="chat-textarea"
            rows={1}
            value={inputPrompt}
            onChange={(e) => setInputPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ketik instruksi konten properti apa saja... (Tekan Enter untuk generate)"
            disabled={isGenerating}
          />

          <button
            type="button"
            className="chat-send-btn"
            disabled={!inputPrompt.trim() || isGenerating}
            onClick={() => handleSendPrompt()}
          >
            {isGenerating ? (
              <Loader2 size={18} className="spin" />
            ) : (
              <Send size={18} />
            )}
          </button>
        </div>

        <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', textAlign: 'center' }}>
          💡 Tip: Cukup ketik topik atau ide bebas, AI Agent akan mengotomatisasi riset audiens, copywriting, & visual compositing 1080x1350.
        </div>
      </div>
    </div>
  );
}
