import React, { useState, useEffect } from 'react';

// Define the interface for DPR data
interface DPRData {
  id: string;
  file_name: string;
  uploaded_at: string;
  extracted_data?: {
    project_title?: string;
  };
  completeness_score?: number;
  ai_risk_scores?: {
    cost_overruns?: number;
    schedule_delays?: number;
    resource_shortages?: number;
    environmental_risks?: number;
  };
}

export default function TestDashboardData() {
  const [dprData, setDprData] = useState<DPRData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/dpr/organization/dashboard', {
          credentials: 'include'
        });
        
        if (response.ok) {
          const data: DPRData[] = await response.json();
          setDprData(data);
          setError(null);
        } else {
          setError(`Failed to fetch data: ${response.status} ${response.statusText}`);
        }
      } catch (err: any) {
        setError(`Error fetching data: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-6">Loading DPR data...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Test Dashboard Data</h1>
      <p className="mb-4">This component tests the frontend-backend communication for the organization dashboard.</p>
      
      {dprData.length === 0 ? (
        <p>No DPR data found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {dprData.map((dpr) => (
            <div key={dpr.id} className="border p-4 rounded-lg">
              <h3 className="text-lg font-medium">{dpr.extracted_data?.project_title || 'Untitled Project'}</h3>
              <p><strong>File:</strong> {dpr.file_name}</p>
              <p><strong>Uploaded:</strong> {new Date(dpr.uploaded_at).toLocaleString()}</p>
              {dpr.completeness_score !== undefined && (
                <p><strong>Completeness Score:</strong> {dpr.completeness_score}%</p>
              )}
              {dpr.ai_risk_scores && (
                <div>
                  <strong>Risk Scores:</strong>
                  <ul className="list-disc list-inside">
                    <li>Cost Overruns: {dpr.ai_risk_scores.cost_overruns || 'N/A'}</li>
                    <li>Schedule Delays: {dpr.ai_risk_scores.schedule_delays || 'N/A'}</li>
                    <li>Resource Shortages: {dpr.ai_risk_scores.resource_shortages || 'N/A'}</li>
                    <li>Environmental: {dpr.ai_risk_scores.environmental_risks || 'N/A'}</li>
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}