import React, { useState } from 'react';
import api from '../utils/api';

const NetworkTest: React.FC = () => {
  const [testResult, setTestResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const testAPIConnection = async () => {
    setIsLoading(true);
    setTestResult('Testing API connection...');
    
    try {
      // Log the URL being used
      console.log('Testing URL:', api.getOrganizationDPRs);
      
      // Try a simple GET request to test connectivity
      const response = await fetch(api.getOrganizationDPRs, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include'
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      if (response.ok) {
        const data = await response.json();
        setTestResult(`Success! Received ${Array.isArray(data) ? data.length : 'data'} from API`);
      } else {
        const errorText = await response.text();
        setTestResult(`Error: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Network error:', error);
      setTestResult(`Network error: ${error.message || 'Failed to connect to server'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px', backgroundColor: '#f5f5f5' }}>
      <h2>Network Connection Test</h2>
      <p>This test will help diagnose the network error issue.</p>
      <button 
        onClick={testAPIConnection} 
        disabled={isLoading}
        style={{ 
          padding: '10px 20px', 
          margin: '10px 0', 
          backgroundColor: '#004D99', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px',
          cursor: isLoading ? 'not-allowed' : 'pointer'
        }}
      >
        {isLoading ? 'Testing...' : 'Test API Connection'}
      </button>
      <div>
        <h3>Test Result:</h3>
        <pre style={{ backgroundColor: 'white', padding: '10px', borderRadius: '4px' }}>{testResult}</pre>
      </div>
    </div>
  );
};

export default NetworkTest;