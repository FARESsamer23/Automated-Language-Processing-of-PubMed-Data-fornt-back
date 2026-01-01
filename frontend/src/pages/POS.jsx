import React, { useState } from 'react';
import { analyzePOS } from '../services/api';

export default function POSAnalyzer() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [tokens, setTokens] = useState([]);
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
      const data = await analyzePOS(text);
      setTokens(data.tokens);
    } catch (error) {
      console.error('Error analyzing POS:', error);
      alert('Error analyzing text. Please try again.');
    }
    setLoading(false);
  };

  const getPOSColor = (tag) => {
    if (tag.startsWith('NN')) return 'bg-blue-100 text-blue-700';
    if (tag.startsWith('VB')) return 'bg-green-100 text-green-700';
    if (tag.startsWith('JJ')) return 'bg-purple-100 text-purple-700';
    if (tag.startsWith('RB')) return 'bg-orange-100 text-orange-700';
    if (tag.startsWith('PR')) return 'bg-pink-100 text-pink-700';
    return 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
      <div className="mb-6">
        <h2 className="text-3xl font-extrabold text-slate-800">
          POS <span className="text-green-600">Tagger</span>
        </h2>
        <p className="text-slate-500">Part-of-Speech tagging for your text.</p>
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

      {/* Text Area */}
      <textarea
        className="w-full border-2 border-slate-100 p-4 rounded-xl focus:ring-4 focus:ring-green-500/10 focus:border-green-500 outline-none transition-all mb-4 text-lg"
        rows="6"
        placeholder="Type or paste your text here, or upload a file above..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-green-200 transition-all active:scale-[0.98] disabled:opacity-50"
        onClick={handleAnalyze}
        disabled={loading || !text.trim()}
      >
        {loading ? "Analyzing..." : "Analyze POS Tags"}
      </button>

      {/* Results */}
      {tokens.length > 0 && (
        <div className="mt-8">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4">
            Results ({tokens.length} tokens)
          </h3>
          <div className="flex flex-wrap gap-3">
            {tokens.map((token, idx) => (
              <div
                key={idx}
                className="flex flex-col bg-slate-50 border border-slate-200 px-4 py-2 rounded-lg"
              >
                <span className="text-slate-700 font-medium">{token.word}</span>
                <span className={`text-[10px] ${getPOSColor(token.tag)} px-2 py-0.5 rounded-md font-bold uppercase mt-1 text-center`}>
                  {token.tag}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}