import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function GenerateConfig() {
  const [requirements, setRequirements] = useState('');
  const [complexity, setComplexity] = useState('medium');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await axios.post(`${API_URL}/api/generate_config`, { requirements, complexity });
      setResult(data.config);
    } catch (err) {
      setResult('Error generating configuration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <style jsx global>{`
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
      `}</style>
      <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-xl font-semibold mb-4">Generate ServiceNow Config</h1>
        <form onSubmit={submit} className="space-y-4">
          <textarea
            className="w-full border px-3 py-2 rounded"
            rows="5"
            placeholder="Enter requirements"
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            required
          ></textarea>
          <select
            value={complexity}
            onChange={(e) => setComplexity(e.target.value)}
            className="border px-3 py-2 rounded"
          >
            <option value="simple">Simple</option>
            <option value="medium">Medium</option>
            <option value="advanced">Advanced</option>
          </select>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate'}
          </button>
        </form>
        {result && (
          <div className="mt-6">
            <h2 className="font-semibold mb-2">Generated Configuration</h2>
            <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded text-sm">
{result}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
