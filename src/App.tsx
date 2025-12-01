import { useState } from 'react';
import Login from './components/Login';
import Signup from './components/Signup';
import OrganizationDashboard from './components/OrganizationDashboard';
import CivilianDashboard from './components/CivilianDashboard';
import TestDashboardData from './components/TestDashboardData';
import TestFileUpload from './components/TestFileUpload';

// API configuration
const apiConfig = {
  fetchActualDPRs: '/api/dprs',
  fetchExtractedDPR: '/api/dprs/extracted',
  submitFeedback: '/api/feedback',
  fetchFeedbacks: '/api/feedback',
  likeFeedback: '/api/feedback/like',
  chatWithAI: '/api/chat',
  analyzeDPR: '/api/dprs/analyze',
  generateAnalyticalReport: '/api/reports/analytical',
  generateRecommendationReport: '/api/reports/recommendation',
  uploadDPRFile: '/api/dprs/upload'
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [userRole, setUserRole] = useState<string | null>(null);

  const handleLogin = (role: string) => {
    setUserRole(role);
    setCurrentPage(role === 'Organization' ? 'organization' : 'civilian');
  };

  const handleLogout = () => {
    setUserRole(null);
    setCurrentPage('login');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {currentPage === 'login' && (
        <Login 
          onLogin={handleLogin}
          onGoToSignup={() => setCurrentPage('signup')}
        />
      )}
      {currentPage === 'signup' && (
        <Signup 
          onSignupSuccess={() => setCurrentPage('login')}
          onBackToLogin={() => setCurrentPage('login')}
        />
      )}
      {currentPage === 'organization' && (
        <OrganizationDashboard 
          onLogout={handleLogout} 
        />
      )}
      {currentPage === 'civilian' && (
        <CivilianDashboard onLogout={handleLogout} />
      )}
      {currentPage === 'test' && (
        <TestDashboardData />
      )}
      {currentPage === 'test-upload' && (
        <TestFileUpload />
      )}
    </div>
  );
}