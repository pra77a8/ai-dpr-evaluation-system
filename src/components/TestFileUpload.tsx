import React, { useState } from 'react';

// Define the interface for the result
interface UploadResult {
  extracted_data?: {
    project_title?: string;
  };
  file_name?: string;
  uploaded_at?: string;
  // Add other properties as needed
}

export default function TestFileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('uploaded_by', 'test_user');

      const response = await fetch('/api/dpr/upload', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });

      if (response.ok) {
        const data: UploadResult = await response.json();
        setResult(data);
      } else {
        const errorText = await response.text();
        try {
          const error = JSON.parse(errorText);
          setError(`Error: ${error.detail || 'Failed to process the file'}`);
        } catch {
          setError(`Error: Failed to process the file. Server responded with status ${response.status}`);
        }
      }
    } catch (err: any) {
      setError(`Network error: ${err.message || 'Failed to connect to server'}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Test File Upload</h1>
      
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
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md disabled:opacity-50"
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-green-50 text-green-700 rounded-md">
          <h2 className="text-lg font-semibold mb-2">Upload Successful!</h2>
          <p className="mt-2"><strong>Project Title:</strong> {result.extracted_data?.project_title || 'N/A'}</p>
          <p><strong>File Name:</strong> {result.file_name}</p>
          <p><strong>Upload Time:</strong> {result.uploaded_at ? new Date(result.uploaded_at).toLocaleString() : 'N/A'}</p>
        </div>
      )}
    </div>
  );
}