import React from 'react';
import { Link } from 'react-router-dom';

const FeatureCard = ({ title, desc, path, icon, color }) => (
  <Link to={path} className="group p-8 bg-white border border-slate-100 rounded-3xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all">
    <div className={`${color} w-12 h-12 rounded-2xl mb-6 flex items-center justify-center text-white text-xl shadow-lg`}>
      {icon}
    </div>
    <h3 className="text-xl font-bold text-slate-800 mb-2 group-hover:text-blue-600 transition-colors">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
  </Link>
);

export default function Home() {
  return (
    <div className="py-10">
      <div className="text-center mb-16">
        <h1 className="text-5xl font-black text-slate-900 mb-4 tracking-tight">
          Advanced <span className="text-blue-600">NLP</span> Studio
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          A powerful suite of natural language processing tools. Extract entities, parse syntax, and discover topics instantly.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <FeatureCard 
          title="Syntax Parser" 
          desc="Break down sentences into their grammatical constituents with visual trees."
          path="/syntax"
          icon="🌲"
          color="bg-slate-800"
        />
        <FeatureCard 
          title="NER Extraction" 
          desc="Identify and classify key entities like Names, Dates, and Organizations."
          path="/ner"
          icon="🏷️"
          color="bg-blue-600"
        />
        <FeatureCard 
          title="Topic Modeling" 
          desc="Uncover the underlying themes and keywords within large bodies of text."
          path="/topics"
          icon="🎯"
          color="bg-purple-600"
        />
      </div>
    </div>
  );
}