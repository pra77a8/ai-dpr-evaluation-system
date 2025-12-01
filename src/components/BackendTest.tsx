import React, { useState, useEffect } from 'react';

const BackendTest: React.FC = () => {
  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const testBackendConnection = async () => {
    setLoading(true);
    setError('');
    setStatus('');
    
    try {
      // Test the health endpoint
      const response = await fetch('/api/health');
      const data = await response.json();
      
      if (data.status === 'healthy') {
        setStatus('✅ Backend connection successful!');
      } else {
        setStatus(`ℹ️ Backend responded: ${JSON.stringify(data)}`);
      }
    } catch (err: any) {
      setError(`❌ Backend connection failed: ${err.message}`);
      console.error('Backend test error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Auto-test on component mount
    testBackendConnection();
  }, []);

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Backend Connection Test</h2>
      
      <div className="mb-4">
        {loading && <p>Testing connection...</p>}
        {status && <p className="text-green-600">{status}</p>}
        {error && <p className="text-red-600">{error}</p>}
      </div>
      
      <button
        onClick={testBackendConnection}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? 'Testing...' : 'Test Connection'}
      </button>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>Backend URL: {(import.meta as any).env.VITE_BACKEND_URL || 'https://ai-dpr-backend-2.onrender.com'}</p>
        <p className="mt-2">This component tests the connection to your deployed backend.</p>
      </div>
    </div>
  );
};

export default BackendTest;