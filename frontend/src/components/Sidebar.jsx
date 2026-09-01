import React from 'react';
import { LayoutGrid, FileText, Image as ImageIcon, Palette, Clock, Layers, Sparkles, BookOpen } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'ai_studio', label: 'AI Agent Copilot', icon: Sparkles, badge: 'Agent' },
    { id: 'design_studio', label: 'Design Engine (1080x1350)', icon: Layers },
    { id: 'studio', label: 'Content Gallery', icon: ImageIcon },
    { id: 'briefs', label: 'AI Brief Creator', icon: FileText },
    { id: 'knowledge', label: 'Knowledge Base', icon: BookOpen, badge: 'Skill' },
    { id: 'projects', label: 'Project Workspaces', icon: LayoutGrid },
    { id: 'brands', label: 'Brand Profiles', icon: Palette },
    { id: 'jobs', label: 'Job Tracker', icon: Clock },
  ];

  return (
    <aside className="sidebar-container">
      <div style={{ padding: '24px 20px 16px 20px', borderBottom: '1px solid var(--border-subtle)' }}>
        <p style={{ fontSize: '0.74rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: 700 }}>
          Navigasi Utama
        </p>
      </div>

      <nav style={{ padding: '12px 10px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {menuItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                width: '100%',
                padding: '10px 14px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? 'rgba(168, 85, 247, 0.15)' : 'transparent',
                border: isActive ? '1px solid rgba(168, 85, 247, 0.35)' : '1px solid transparent',
                color: isActive ? '#c084fc' : 'var(--text-muted)',
                fontWeight: isActive ? 700 : 500,
                fontSize: '0.88rem',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Icon size={18} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span style={{ fontSize: '0.65rem', background: isActive ? 'rgba(168, 85, 247, 0.25)' : 'rgba(56, 189, 248, 0.2)', color: isActive ? '#e9d5ff' : 'var(--accent-cyan)', padding: '2px 6px', borderRadius: '4px', fontWeight: 700 }}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      <div style={{ marginTop: 'auto', padding: '18px', borderTop: '1px solid var(--border-subtle)' }}>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <p style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>AI Content Agent: Active</p>
          <p style={{ fontSize: '0.68rem', color: 'var(--text-dim)', marginTop: '2px' }}>Content Strategy + Art Direction</p>
        </div>
      </div>
    </aside>
  );
}
