import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [analysisId, setAnalysisId] = useState(null);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);

  const startAnalysis = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/analyze`, {
        credentials: {
          instance_url: 'https://dev.service-now.com',
          username: 'demo',
          password: 'demo'
        },
        analysis_type: 'full'
      });
      
      setAnalysisId(response.data.workflow_id);
      checkStatus(response.data.workflow_id);
    } catch (error) {
      console.error('Failed to start analysis:', error);
      setLoading(false);
    }
  };

  const checkStatus = async (workflowId) => {
    try {
      const response = await axios.get(`${API_URL}/api/status/${workflowId}`);
      setStatus(response.data);
      
      if (response.data.status === 'completed') {
        getResults(workflowId);
        setLoading(false);
      } else {
        setTimeout(() => checkStatus(workflowId), 2000);
      }
    } catch (error) {
      console.error('Failed to check status:', error);
      setLoading(false);
    }
  };

  const getResults = async (workflowId) => {
    try {
      const response = await axios.get(`${API_URL}/api/results/${workflowId}`);
      setResults(response.data);
    } catch (error) {
      console.error('Failed to get results:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <style jsx global>{`
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
      `}</style>
      
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">
            AI ServiceNow Consultancy
          </h1>
          <nav className="space-x-4 text-sm">
            <a href="/generate" className="text-blue-600 hover:underline">Generate Config</a>
            <a href="/login" className="text-blue-600 hover:underline">Login</a>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Analysis Demo</h2>
          
          {!analysisId && (
            <button
              onClick={startAnalysis}
              disabled={loading}
              className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
              {loading ? 'Starting...' : 'Start Analysis'}
            </button>
          )}

          {status && (
            <div className="mt-6 p-4 bg-gray-100 rounded">
              <h3 className="font-semibold">Analysis Status</h3>
              <p>Status: {status.status}</p>
              <p>Progress: {status.progress}%</p>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                <div 
                  className="bg-blue-600 h-2.5 rounded-full" 
                  style={{width: `${status.progress}%`}}
                ></div>
              </div>
            </div>
          )}

          {results && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Analysis Results</h3>
              
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-blue-50 rounded">
                  <p className="text-sm text-gray-600">Health Score</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {results.health_score}/100
                  </p>
                </div>
                <div className="p-4 bg-green-50 rounded">
                  <p className="text-sm text-gray-600">Estimated Savings</p>
                  <p className="text-2xl font-bold text-green-600">
                    {results.estimated_savings}
                  </p>
                </div>
              </div>

              <h4 className="font-semibold mb-2">Key Recommendations:</h4>
              <ul className="space-y-2">
                {results.recommendations.map((rec, idx) => (
                  <li key={idx} className="p-3 bg-gray-50 rounded">
                    <span className="font-medium">{rec.title}</span>
                    <span className={`ml-2 text-xs px-2 py-1 rounded ${
                      rec.priority === 'high' ? 'bg-red-100 text-red-700' : 
                      'bg-yellow-100 text-yellow-700'
                    }`}>
                      {rec.priority}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}