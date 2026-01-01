import React, { useState, useEffect } from 'react';
import { getStatistics, getLanguageStatistics } from '../services/api';

export default function StatisticsDashboard() {
  const [stats, setStats] = useState(null);
  const [langStats, setLangStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getStatistics();
      const langData = await getLanguageStatistics();
      
      setStats(data);
      setLangStats(langData);
      
      console.log("Main Stats:", data);
      console.log("Language Stats:", langData);
    } catch (error) {
      console.error("Error loading statistics:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <div className="text-slate-500 font-medium">Analyzing dataset...</div>
        </div>
      </div>
    );
  }

  // Calculate average sentence length from the response data
  const avgSentenceLength = stats?.total_words && stats?.total_sentences 
    ? (stats.total_words / stats.total_sentences).toFixed(2) 
    : "0.00";

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
        <h2 className="text-3xl font-extrabold text-slate-800 mb-6">Dataset Statistics</h2>
        
        {/* Overview Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard 
            title="Total Sentences" 
            value={stats?.total_sentences?.toLocaleString()} 
            color="blue" 
          />
          <StatCard 
            title="Total Words" 
            value={stats?.total_words?.toLocaleString()} 
            color="green" 
          />
          <StatCard 
            title="Unique Words" 
            value={langStats?.vocabulary_size > 0 ? langStats.vocabulary_size.toLocaleString() : "N/A"} 
            color="purple" 
          />
          <StatCard 
            title="Avg Sentence Length" 
            value={avgSentenceLength} 
            color="orange" 
          />
        </div>

        {/* Most Frequent Words */}
        <div className="mb-8">
          <h3 className="text-lg font-bold text-slate-700 mb-4 flex items-center">
            <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded mr-2 text-xs uppercase font-bold">Top 20</span>
            Most Frequent Words
          </h3>
          <div className="flex flex-wrap gap-2">
            {stats?.most_common_words?.map(([word, count], idx) => (
              <div key={idx} className="bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium shadow-sm border border-blue-200">
                <span className="font-bold">{word}</span>
                <span className="text-blue-500 ml-2">×{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Bigrams */}
        <div className="mb-8">
          <h3 className="text-lg font-bold text-slate-700 mb-4 flex items-center">
            <span className="bg-green-100 text-green-700 px-2 py-1 rounded mr-2 text-xs uppercase font-bold">Bigrams</span>
            Most Common Word Pairs
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {stats?.most_common_bigrams?.slice(0, 10).map(([bigram, count], idx) => (
              <div key={idx} className="flex justify-between items-center bg-slate-50 hover:bg-white p-4 rounded-lg border border-slate-200 transition-all group shadow-sm">
                <span className="font-mono text-slate-700 font-medium group-hover:text-blue-600">"{bigram}"</span>
                <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Language Model Details */}
        {langStats && (
          <div className="mt-10 pt-6 border-t border-slate-100">
            <h3 className="text-lg font-bold text-slate-700 mb-4 flex items-center">
              <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded mr-2 text-xs uppercase font-bold">Model info</span>
              N-Gram Engine Status
            </h3>
            
            {langStats.vocabulary_size === 0 ? (
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start space-x-3">
                <span className="text-amber-500 text-xl">⚠️</span>
                <div>
                  <div className="text-amber-800 font-bold text-sm">Action Required</div>
                  <div className="text-amber-700 text-sm">{langStats.message || "Please train the model to see advanced language statistics."}</div>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InfoCard label="Vocabulary Size" value={langStats.vocabulary_size?.toLocaleString()} />
                <InfoCard label="Total Bigrams" value={langStats.total_bigrams?.toLocaleString()} />
                <InfoCard label="Unique Bigrams" value={langStats.unique_bigrams?.toLocaleString()} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Reusable Stat Card Component
 */
function StatCard({ title, value, color = "blue" }) {
  const colorClasses = {
    blue: "from-blue-50 to-blue-100 text-blue-700 border-blue-200",
    green: "from-green-50 to-green-100 text-green-700 border-green-200",
    purple: "from-purple-50 to-purple-100 text-purple-700 border-purple-200",
    orange: "from-orange-50 to-orange-100 text-orange-700 border-orange-200"
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} p-6 rounded-xl shadow-sm border`}>
      <div className="text-xs font-semibold uppercase tracking-wider opacity-75 mb-2">{title}</div>
      <div className="text-3xl font-black">{value || "0"}</div>
    </div>
  );
}

/**
 * Reusable Info Card Component
 */
function InfoCard({ label, value }) {
  return (
    <div className="bg-slate-50 border border-slate-200 p-4 rounded-lg">
      <div className="text-xs text-slate-500 uppercase font-semibold mb-1">{label}</div>
      <div className="text-xl font-bold text-slate-800">{value || "0"}</div>
    </div>
  );
}