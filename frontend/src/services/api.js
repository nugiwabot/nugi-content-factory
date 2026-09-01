import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000
});

// Response interceptor for consistent error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const errorMsg = error.response?.data?.error?.message || error.message || 'Network error';
    return Promise.reject(new Error(errorMsg));
  }
);

export const api = {
  // System Health & Providers
  getHealth: () => apiClient.get('/health'),
  checkFluxStatus: () => apiClient.get('/health/flux'),
  getProviderSettings: () => apiClient.get('/settings/providers'),
  updateProviderSettings: (data) => apiClient.post('/settings/providers', data),
  testProviderConnection: (data) => apiClient.post('/settings/providers/test', data),

  // Brand DNA
  getBrandDna: () => apiClient.get('/brand/nugi-properti'),

  // Phase 3B AI Content & Art Direction Studio
  chatWithAgent: (data) => apiClient.post('/ai-studio/chat', data),
  generateAIContent: (data) => apiClient.post('/ai-studio/generate', data),
  regenerateHeadline: (data) => apiClient.post('/ai-studio/regenerate/headline', data),
  regenerateCaption: (data) => apiClient.post('/ai-studio/regenerate/caption', data),
  regenerateVisual: (data) => apiClient.post('/ai-studio/regenerate/visual', data),
  renderCustomSpec: (data) => apiClient.post('/ai-studio/render', data),

  // Batch generation (agentic plan + bulk)
  planBatch: (data) => apiClient.post('/batch/plan', data),
  runBatch: (data) => apiClient.post('/batch/run', data),
  getBatchRun: (id) => apiClient.get(`/batch/runs/${id}`),
  getBatchRuns: (projectId) => apiClient.get('/batch/runs', { params: { project_id: projectId } }),

  // Knowledge base (skills, pillars, brand context)
  listSkills: () => apiClient.get('/knowledge/skills'),
  uploadKnowledge: (file) => {
    const fd = new FormData();
    fd.append('file', file);
    return apiClient.post('/knowledge/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
  },
  deleteSkill: (id) => apiClient.delete(`/knowledge/skills/${id}`),
  getPillars: () => apiClient.get('/knowledge/pillars'),
  updatePillar: (id, data) => apiClient.put(`/knowledge/pillars/${id}`, data),
  getBrandContexts: () => apiClient.get('/knowledge/brand'),
  seedKnowledge: () => apiClient.post('/knowledge/seed'),

  // Phase 3A Editorial Visual Engine
  getEditorialCompositions: () => apiClient.get('/editorial/compositions'),
  renderEditorial: (data) => apiClient.post('/editorial/render', data),

  // Phase 2 Templates & Design Brain
  getTemplates: () => apiClient.get('/templates'),
  getTemplate: (id) => apiClient.get(`/templates/${id}`),
  renderTemplate: (data) => apiClient.post('/templates/render', data),

  // Projects
  getProjects: () => apiClient.get('/projects'),
  createProject: (data) => apiClient.post('/projects', data),
  getProject: (id) => apiClient.get(`/projects/${id}`),

  // Brand Profiles
  getBrandProfiles: () => apiClient.get('/brand-profiles'),
  createBrandProfile: (data) => apiClient.post('/brand-profiles', data),
  getBrandProfile: (id) => apiClient.get(`/brand-profiles/${id}`),

  // Briefs
  getBriefs: (projectId) => apiClient.get('/briefs', { params: { project_id: projectId } }),
  createBrief: (data) => apiClient.post('/briefs', data),
  getBrief: (id) => apiClient.get(`/briefs/${id}`),

  // Content & Generation
  getContentList: (projectId) => apiClient.get('/content', { params: { project_id: projectId } }),
  getContentDetail: (id) => apiClient.get(`/content/${id}`),
  generateContent: (data) => apiClient.post('/content/generate', data),

  // Jobs
  getJobs: (projectId) => apiClient.get('/jobs', { params: { project_id: projectId } }),
  getJob: (id) => apiClient.get(`/jobs/${id}`)
};
