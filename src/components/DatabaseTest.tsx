import React, { useState } from 'react';
import api from '../utils/api';

const DatabaseTest: React.FC = () => {
  const [testResult, setTestResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const testDatabaseConnection = async () => {
    setIsLoading(true);
    setTestResult('Testing database connection through backend...');
    
    try {
      // Try to fetch organization DPRs which will require database access
      const response = await fetch(api.getOrganizationDPRs, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include'
      });
      
      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        setTestResult(`Database connection successful! Retrieved ${Array.isArray(data) ? data.length : 'data'} records.`);
      } else if (response.status === 500) {
        setTestResult('Database connection error: Server error (500). Check backend logs for MongoDB connection issues.');
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
    <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px', backgroundColor: '#fff3cd' }}>
      <h2>Database Connection Test</h2>
      <p>This test checks if the backend can connect to MongoDB.</p>
      <button 
        onClick={testDatabaseConnection} 
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
        {isLoading ? 'Testing...' : 'Test Database Connection'}
      </button>
      <div>
        <h3>Test Result:</h3>
        <pre style={{ backgroundColor: 'white', padding: '10px', borderRadius: '4px', whiteSpace: 'pre-wrap' }}>{testResult}</pre>
      </div>
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f8d7da', border: '1px solid #f5c6cb', borderRadius: '4px' }}>
        <h4>If you see a database connection error:</h4>
        <ul>
          <li>Check that your backend's MongoDB connection string uses the SRV format (mongodb+srv://)</li>
          <li>Verify that your MongoDB Atlas cluster is running and accessible</li>
          <li>Ensure the IP whitelist in MongoDB Atlas includes your backend server's IP</li>
          <li>Confirm that the database credentials are correct</li>
        </ul>
      </div>
    </div>
  );
};

export default DatabaseTest;