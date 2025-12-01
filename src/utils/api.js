// API utility for handling requests with proper base URL
const getBaseURL = () => {
  // Log environment information for debugging
  console.log('Environment MODE:', import.meta.env.MODE);
  console.log('Environment PROD:', import.meta.env.PROD);
  console.log('Environment VITE_BACKEND_URL:', import.meta.env.VITE_BACKEND_URL);
  
  // In production, use the environment variable or default to your Render URL
  if (import.meta.env.PROD || import.meta.env.MODE === 'production') {
    // Try to get the backend URL from environment variables
    let url = import.meta.env.VITE_BACKEND_URL;
    
    // If not set, use the default
    if (!url) {
      url = 'https://ai-dpr-backend-2.onrender.com';
    }
    
    // Ensure the URL doesn't end with a slash
    if (url.endsWith('/')) {
      url = url.slice(0, -1);
    }
    
    console.log('Using production URL:', url);
    return url;
  }
  // In development, use the proxy
  console.log('Using development proxy');
  return '';
};

const API_BASE_URL = getBaseURL();

export const api = {
  // Auth endpoints
  login: `${API_BASE_URL}/api/auth/login`,
  signup: `${API_BASE_URL}/api/auth/signup`,
  
  // DPR endpoints
  uploadDPR: `${API_BASE_URL}/api/dpr/upload`,
  uploadDPRWithAI: `${API_BASE_URL}/api/dpr/upload_with_ai`,
  getUserDPRs: (userId) => `${API_BASE_URL}/api/dpr/user/${userId}`,
  getDPRById: (dprId) => `${API_BASE_URL}/api/dpr/${dprId}`,
  approveDPR: (dprId) => `${API_BASE_URL}/api/dpr/${dprId}/approve`,
  deleteDPR: (dprId) => `${API_BASE_URL}/api/dpr/${dprId}`,
  getOrganizationDPRs: `${API_BASE_URL}/api/dpr/organization/dashboard`,
  
  // Risk endpoints
  predictRisk: `${API_BASE_URL}/api/risk/predict`,
  getRiskAnalysis: (dprId) => `${API_BASE_URL}/api/risk/analysis/${dprId}`,
  assessRiskWithAI: (dprId) => `${API_BASE_URL}/api/risk/assess_with_ai/${dprId}`,
  
  // Feedback endpoints
  submitFeedback: `${API_BASE_URL}/api/feedback`,
  getAllFeedback: `${API_BASE_URL}/api/feedback/organization/dashboard`,
  likeFeedback: (feedbackId) => `${API_BASE_URL}/api/feedback/${feedbackId}/like`,
  dislikeFeedback: (feedbackId) => `${API_BASE_URL}/api/feedback/${feedbackId}/dislike`,
  
  // AI endpoints
  aiChat: `${API_BASE_URL}/api/ai/chat`,
  aiTranslate: `${API_BASE_URL}/api/ai/translate`,
  
  // Reports endpoints
  generateReport: `${API_BASE_URL}/api/reports/generate`,
  downloadReport: (reportId) => `${API_BASE_URL}/api/reports/download/${reportId}`,
};

export default api;