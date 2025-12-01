import React, { useState } from 'react';
import api from '../utils/api';

const DebugUploadTest: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [corsTestResult, setCorsTestResult] = useState<string | null>(null);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toISOString()}: ${message}`]);
    console.log(message);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
      setLogs([]);
      addLog(`File selected: ${e.target.files[0].name}`);
    }
  };

  const testCORS = async () => {
    setCorsTestResult('Testing CORS...');
    addLog('Testing CORS configuration');
    
    try {
      // Test a simple GET request to check CORS
      const response = await fetch(`${api.login.replace('/api/auth/login', '/cors-test')}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setCorsTestResult('CORS Test Passed: ' + data.message);
        addLog(`CORS Test Passed: ${JSON.stringify(data)}`);
      } else {
        const errorText = await response.text();
        setCorsTestResult(`CORS Test Failed: ${response.status} - ${errorText}`);
        addLog(`CORS Test Failed: ${response.status} - ${errorText}`);
      }
    } catch (err: any) {
      setCorsTestResult(`CORS Test Error: ${err.message}`);
      addLog(`CORS Test Error: ${err.message}`);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      const errorMsg = 'Please select a file first';
      setError(errorMsg);
      addLog(errorMsg);
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);
    setLogs([]);
    addLog(`Starting upload for: ${file.name}`);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('uploaded_by', 'debug_user');
      formData.append('generate_reports', 'true');

      addLog('Creating fetch request with formData');
      for (let [key, value] of formData.entries()) {
        addLog(`FormData entry - ${key}: ${value instanceof File ? value.name : value}`);
      }

      // Call the backend API with detailed error handling
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout

      addLog(`Sending request to: ${api.uploadDPRWithAI}`);
      
      const response = await fetch(api.uploadDPRWithAI, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include'
      });

      clearTimeout(timeoutId);
      addLog(`Response received - Status: ${response.status}, OK: ${response.ok}`);
      
      // Log response headers for CORS debugging
      const responseHeaders: Record<string, string> = {};
      response.headers.forEach((value, key) => {
        responseHeaders[key] = value;
      });
      addLog(`Response headers: ${JSON.stringify(responseHeaders)}`);

      if (response.ok) {
        addLog('Parsing response JSON');
        const data = await response.json();
        addLog(`Response data: ${JSON.stringify(data, null, 2)}`);
        setResult(data);
        addLog('Upload completed successfully');
      } else {
        addLog(`Server error - Status: ${response.status}`);
        const errorText = await response.text();
        addLog(`Server error response: ${errorText}`);
        try {
          const error = JSON.parse(errorText);
          const errorMsg = `Server Error: ${error.detail || 'Failed to process the file'}`;
          setError(errorMsg);
          addLog(errorMsg);
        } catch {
          const errorMsg = `Server Error: Failed to process the file. Server responded with status ${response.status}`;
          setError(errorMsg);
          addLog(errorMsg);
        }
      }
    } catch (err: any) {
      addLog(`Network error: ${err.message || 'Unknown error'}`);
      if (err.name === 'AbortError') {
        const errorMsg = 'Request timed out. The file might be too large or the processing took too long.';
        setError(errorMsg);
        addLog(errorMsg);
      } else {
        const errorMsg = `Network error: ${err.message || 'Failed to connect to server. Please make sure the backend is running.'}`;
        setError(errorMsg);
        addLog(errorMsg);
      }
    } finally {
      setUploading(false);
      addLog('Upload process finished');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Debug DPR Upload Test</h1>
      
      <div className="mb-6 p-4 bg-blue-50 rounded-md">
        <h2 className="text-lg font-semibold mb-2">CORS Test</h2>
        <button
          onClick={testCORS}
          className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md mb-2"
        >
          Test CORS Configuration
        </button>
        {corsTestResult && (
          <div className="mt-2 p-2 bg-white rounded-md">
            <p>{corsTestResult}</p>
          </div>
        )}
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Select DPR File (PDF, DOCX, or image)
        </label>
        <input
          type="file"
          accept=".pdf,.docx,.doc,.png,.jpg,.jpeg"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-md file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100"
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={uploading || !file}
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md disabled:opacity-50 mb-6"
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </button>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-md">
          <h2 className="text-lg font-semibold mb-2">Error:</h2>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="mb-6 p-4 bg-green-50 text-green-700 rounded-md">
          <h2 className="text-lg font-semibold mb-2">Upload Successful!</h2>
          <pre className="text-sm overflow-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {logs.length > 0 && (
        <div className="p-4 bg-gray-50 rounded-md">
          <h2 className="text-lg font-semibold mb-2">Debug Logs:</h2>
          <div className="text-sm font-mono overflow-auto max-h-96">
            {logs.map((log, index) => (
              <div key={index} className="mb-1">{log}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DebugUploadTest;