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
  // System Health
  getHealth: () => apiClient.get('/health'),

  // Brand DNA
  getBrandDna: () => apiClient.get('/brand/nugi-properti'),

  // Templates & Design Brain
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
