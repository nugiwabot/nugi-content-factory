import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import AIContentStudio from './components/AIContentStudio';
import DesignPreviewStudio from './components/DesignPreviewStudio';
import ProjectView from './components/ProjectView';
import BriefCreator from './components/BriefCreator';
import ContentStudio from './components/ContentStudio';
import BrandProfileManager from './components/BrandProfileManager';
import JobStatusTracker from './components/JobStatusTracker';
import KnowledgeManager from './components/KnowledgeManager';
import SettingsModal from './components/SettingsModal';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('ai_studio');
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [brands, setBrands] = useState([]);
  const [contents, setContents] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [healthStatus, setHealthStatus] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [loading, setLoading] = useState(true);

  // Initial Data Bootstrap
  useEffect(() => {
    bootstrap();
  }, []);

  // Fetch project-specific content when currentProject changes
  useEffect(() => {
    if (currentProject) {
      loadProjectData(currentProject.id);
    }
  }, [currentProject]);

  const bootstrap = async () => {
    try {
      setLoading(true);
      const [healthRes, projList, brandList] = await Promise.all([
        api.getHealth().catch(() => null),
        api.getProjects().catch(() => []),
        api.getBrandProfiles().catch(() => [])
      ]);

      setHealthStatus(healthRes);
      setBrands(brandList);

      // Auto-create default project if none exists
      if (projList.length === 0) {
        const defaultProj = await api.createProject({
          name: 'NugiProperti Marketing Studio',
          description: 'Workspace utama produksi konten edukasi dan penawaran properti.'
        });
        setProjects([defaultProj]);
        setCurrentProject(defaultProj);
      } else {
        setProjects(projList);
        setCurrentProject(projList[0]);
      }
    } catch (err) {
      console.error('Bootstrap error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadProjectData = async (projectId) => {
    try {
      const [contentList, jobList] = await Promise.all([
        api.getContentList(projectId).catch(() => []),
        api.getJobs(projectId).catch(() => [])
      ]);
      setContents(contentList);
      setJobs(jobList);
    } catch (err) {
      console.error('Error loading project data:', err);
    }
  };

  const handleContentGenerated = (newContent) => {
    if (currentProject) {
      loadProjectData(currentProject.id);
      setActiveTab('studio');
    }
  };

  const handleProjectCreated = (newProj) => {
    setProjects(prev => [newProj, ...prev]);
    setCurrentProject(newProj);
    setActiveTab('studio');
  };

  const handleBrandCreated = (newBrand) => {
    setBrands(prev => [newBrand, ...prev]);
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="main-content">
        <Header 
          projects={projects}
          currentProject={currentProject}
          setCurrentProject={setCurrentProject}
          onOpenSettings={() => setShowSettings(true)}
          onQuickGenerate={() => setActiveTab('ai_studio')}
          healthStatus={healthStatus}
        />

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Memuat Sistem Nugi Content Factory...
          </div>
        ) : (
          <>
            {activeTab === 'ai_studio' && (
              <AIContentStudio currentProject={currentProject} />
            )}

            {activeTab === 'design_studio' && (
              <DesignPreviewStudio />
            )}

            {activeTab === 'studio' && (
              <ContentStudio 
                contents={contents} 
                onRefresh={() => currentProject && loadProjectData(currentProject.id)} 
              />
            )}

            {activeTab === 'briefs' && (
              <BriefCreator 
                currentProject={currentProject} 
                onContentGenerated={handleContentGenerated} 
              />
            )}

            {activeTab === 'projects' && (
              <ProjectView 
                projects={projects} 
                onProjectCreated={handleProjectCreated}
                onSelectProject={(p) => {
                  setCurrentProject(p);
                  setActiveTab('studio');
                }}
              />
            )}

            {activeTab === 'knowledge' && (
              <KnowledgeManager />
            )}

            {activeTab === 'brands' && (
              <BrandProfileManager 
                brands={brands} 
                onBrandCreated={handleBrandCreated} 
              />
            )}

            {activeTab === 'jobs' && (
              <JobStatusTracker 
                jobs={jobs} 
                onRefresh={() => currentProject && loadProjectData(currentProject.id)} 
              />
            )}
          </>
        )}
      </main>

      {/* Settings Modal */}
      <SettingsModal 
        isOpen={showSettings} 
        onClose={() => setShowSettings(false)} 
        healthStatus={healthStatus} 
      />
    </div>
  );
}
