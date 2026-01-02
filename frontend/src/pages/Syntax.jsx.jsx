import React, { useState } from 'react';
import { analyzeSyntax } from '../services/api';

// Parse constituency tree string into tree structure
function parseTree(treeString) {
    const tokens = treeString.replace(/\(/g, ' ( ').replace(/\)/g, ' ) ').split(/\s+/).filter(t => t);
    let index = 0;

    function parse() {
        if (tokens[index] !== '(') return null;
        index++; // skip '('
        
        const label = tokens[index++];
        const children = [];
        
        while (tokens[index] !== ')') {
            if (tokens[index] === '(') {
                children.push(parse());
            } else {
                children.push({ label: tokens[index++], children: [] });
            }
        }
        index++; // skip ')'
        
        return { label, children };
    }

    return parse();
}

// Tree visualization component
function TreeNode({ node, depth = 0 }) {
    if (!node) return null;
    
    const isLeaf = node.children.length === 0;
    const hasChildren = node.children.length > 0;
    
    return (
        <div className="flex flex-col items-center">
            <div className={`px-3 py-1 rounded ${isLeaf ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'} font-semibold text-sm mb-2`}>
                {node.label}
            </div>
            
            {hasChildren && (
                <>
                    <div className="w-0.5 h-6 bg-slate-300"></div>
                    <div className="flex gap-4 relative">
                        {node.children.length > 1 && (
                            <div className="absolute top-0 left-0 right-0 h-0.5 bg-slate-300" style={{ width: '100%' }}></div>
                        )}
                        {node.children.map((child, i) => (
                            <div key={i} className="flex flex-col items-center">
                                <div className="w-0.5 h-6 bg-slate-300"></div>
                                <TreeNode node={child} depth={depth + 1} />
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}

export default function SyntaxAnalyzer() {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [result, setResult] = useState('');
    const [treeData, setTreeData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [viewMode, setViewMode] = useState('tree'); // 'tree' or 'text'

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
            const data = await analyzeSyntax(text);
            setResult(data.constituency_tree);
            
            // Parse the tree for visualization
            try {
                const parsed = parseTree(data.constituency_tree);
                setTreeData(parsed);
            } catch (parseError) {
                console.error('Error parsing tree:', parseError);
            }
        } catch (error) {
            console.error('Error analyzing syntax:', error);
            alert('Error analyzing text. Please try again.');
        }
        setLoading(false);
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
            <div className="mb-6">
                <h2 className="text-3xl font-extrabold text-slate-800 italic">
                    Syntax <span className="text-blue-600">Tree</span>
                </h2>
                <p className="text-slate-500">Analyze the grammatical structure and constituency tree of your sentences.</p>
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
                className="w-full border-2 border-slate-100 p-4 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all mb-4"
                rows="4"
                placeholder="Enter a sentence to parse, or upload a file above..."
                value={text}
                onChange={(e) => setText(e.target.value)}
            />

            <button
                className="w-full bg-slate-900 hover:bg-black text-white font-bold py-4 rounded-xl transition-all disabled:opacity-50"
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
            >
                {loading ? "Parsing..." : "Generate Syntax Tree"}
            </button>

            {result && (
                <div className="mt-8">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-semibold uppercase text-slate-400">Constituency Tree</h3>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setViewMode('tree')}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${viewMode === 'tree' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
                            >
                                Tree View
                            </button>
                            <button
                                onClick={() => setViewMode('text')}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${viewMode === 'text' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
                            >
                                Text View
                            </button>
                        </div>
                    </div>
                    
                    {viewMode === 'tree' && treeData ? (
                        <div className="bg-white border-2 border-slate-200 p-8 rounded-xl overflow-auto">
                            <TreeNode node={treeData} />
                        </div>
                    ) : (
                        <pre className="bg-slate-900 text-green-400 p-6 rounded-xl overflow-auto font-mono text-sm leading-relaxed border-l-4 border-blue-500 shadow-inner">
                            {result}
                        </pre>
                    )}
                </div>
            )}
        </div>
    );
}