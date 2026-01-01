import React, { useState } from 'react';
import { analyzeNER } from '../services/api';

export default function NERAnalyzer() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target.result;
        if (content.split(' ').length > 500) {
          alert('File is too large. Maximum 500 words allowed.');
          return;
        }
        setText(content);
        setFile(uploadedFile);
      };
      reader.readAsText(uploadedFile);
    }
  };

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    try {
      const data = await analyzeNER(text);
      setEntities(data.entities);
    } catch (error) {
      console.error('Error analyzing NER:', error);
      alert('Error analyzing text. Please try again.');
    }
    setLoading(false);
  };

  const getEntityColor = (label) => {
    const colors = {
      'PERSON': 'bg-blue-100 text-blue-700',
      'ORG': 'bg-green-100 text-green-700',
      'GPE': 'bg-purple-100 text-purple-700',
      'LOC': 'bg-orange-100 text-orange-700',
      'DATE': 'bg-pink-100 text-pink-700',
      'TIME': 'bg-yellow-100 text-yellow-700',
      'MONEY': 'bg-emerald-100 text-emerald-700'
    };
    return colors[label] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8 transition-all">
      <div className="mb-6">
        <h2 className="text-3xl font-extrabold text-slate-800">NER Analyzer</h2>
        <p className="text-slate-500">Extract names, locations, and organizations from your text.</p>
      </div>

      {/* File Upload */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-slate-700 mb-2">
          Upload Text File (max 500 words)
        </label>
        <input
          type="file"
          accept=".txt"
          onChange={handleFileUpload}
          className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
        />
        {file && (
          <p className="mt-2 text-xs text-green-600">✓ Loaded: {file.name}</p>
        )}
      </div>

      <textarea
        className="w-full border-2 border-slate-100 p-4 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all mb-4 text-lg"
        rows="6"
        placeholder="Type or paste your text here, or upload a file above..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-200 transition-all active:scale-[0.98] disabled:opacity-50"
        onClick={handleAnalyze}
        disabled={loading || !text.trim()}
      >
        {loading ? "Analyzing..." : "Run Analysis"}
      </button>

      {entities.length > 0 && (
        <div className="mt-8">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4">
            Results ({entities.length} entities found)
          </h3>
          <div className="flex flex-wrap gap-3">
            {entities.map((ent, idx) => (
              <div key={idx} className="flex items-center bg-slate-50 border border-slate-200 px-4 py-2 rounded-full">
                <span className="text-slate-700 mr-2 font-medium">{ent.text}</span>
                <span className={`text-[10px] ${getEntityColor(ent.label)} px-2 py-0.5 rounded-md font-bold uppercase`}>
                  {ent.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}