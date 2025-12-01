import React, { useState, useEffect } from 'react';
import api from '../utils/api';

const APITest: React.FC = () => {
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
        setTestResult(`Success! Received ${data.length || 0} items from API`);
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

  useEffect(() => {
    // Log the base URL on component mount
    console.log('API Base URL:', api.getOrganizationDPRs.replace('/api/dpr/organization/dashboard', ''));
  }, []);

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px' }}>
      <h2>API Connection Test</h2>
      <button 
        onClick={testAPIConnection} 
        disabled={isLoading}
        style={{ padding: '10px 20px', margin: '10px 0' }}
      >
        {isLoading ? 'Testing...' : 'Test API Connection'}
      </button>
      <div>
        <h3>Test Result:</h3>
        <pre>{testResult}</pre>
      </div>
    </div>
  );
};

export default APITest;