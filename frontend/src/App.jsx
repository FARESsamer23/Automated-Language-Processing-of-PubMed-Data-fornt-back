import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import NERAnalyzer from './pages/NER.jsx';
import SyntaxAnalyzer from './pages/Syntax.jsx';
import TopicAnalyzer from './pages/Topics';
import POSAnalyzer from './pages/POS';
import StatisticsDashboard from './pages/Statistics';
import Home from './pages/Home';

function App() {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-12 max-w-6xl">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/statistics" element={<StatisticsDashboard />} />
            <Route path="/syntax" element={<SyntaxAnalyzer />} />
            <Route path="/pos" element={<POSAnalyzer />} />
            <Route path="/ner" element={<NERAnalyzer />} />
            <Route path="/topics" element={<TopicAnalyzer />} />
          </Routes>
        </main>
        <Footer />
      </div>
    );
  }

export default App;