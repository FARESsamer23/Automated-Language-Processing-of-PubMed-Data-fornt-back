import React, { useState } from 'react';
import { analyzeTopics } from '../services/api';

export default function TopicAnalyzer() {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [topics, setTopics] = useState([]);
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
            const data = await analyzeTopics(text);
            // Only show top 3 topics as required
            setTopics(data.topics.slice(0, 3));
        } catch (error) {
            console.error('Error analyzing topics:', error);
            alert('Error analyzing text. Please try again.');
        }
        setLoading(false);
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
            <div className="mb-6 flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-extrabold text-slate-800">Topic Modeling</h2>
                    <p className="text-slate-500">Discover the 3 main themes in your text data.</p>
                </div>
                <div className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-bold uppercase">LDA Algorithm</div>
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
                    className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100 cursor-pointer"
                />
                {file && (
                    <p className="mt-2 text-xs text-green-600">✓ Loaded: {file.name}</p>
                )}
            </div>

            <textarea
                className="w-full border-2 border-slate-100 p-4 rounded-xl focus:ring-4 focus:ring-purple-500/10 focus:border-purple-500 outline-none transition-all mb-4"
                rows="4"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Provide a large paragraph or multiple sentences, or upload a file above..."
            />

            <button
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 rounded-xl shadow-lg shadow-purple-200 transition-all disabled:opacity-50"
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
            >
                {loading ? "Extracting Topics..." : "Extract Top 3 Topics"}
            </button>

            {topics.length > 0 && (
                <div className="mt-10 grid grid-cols-1 gap-4">
                    <div className="text-sm text-slate-500 mb-2">
                        Showing top 3 main topics:
                    </div>
                    {topics.map((t, idx) => (
                        <div key={idx} className="group p-5 border border-slate-100 bg-slate-50 rounded-xl hover:bg-white hover:shadow-md transition-all">
                            <div className="flex justify-between items-center mb-3">
                                <span className="font-bold text-slate-800">Topic #{t.topic_id}</span>
                                <span className="text-xs bg-white border px-2 py-1 rounded-md text-slate-500">
                                    Match: {(t.probability * 100).toFixed(1)}%
                                </span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {t.keywords.map((kw, i) => (
                                    <span key={i} className="text-sm text-purple-600 font-medium italic">#{kw}</span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}