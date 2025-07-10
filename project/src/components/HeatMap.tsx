import React from 'react';
import { MapPin, TrendingUp } from 'lucide-react';
import { stateData } from '../data/mockData';

const HeatMap: React.FC = () => {
  const getIntensityColor = (value: number, max: number) => {
    const intensity = value / max;
    if (intensity > 0.8) return 'bg-purple-600';
    if (intensity > 0.6) return 'bg-purple-500';
    if (intensity > 0.4) return 'bg-purple-400';
    if (intensity > 0.2) return 'bg-purple-300';
    return 'bg-purple-200';
  };

  const maxTransactions = Math.max(...stateData.map(s => s.transactions));

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Transaction Heat Map</h2>
        <MapPin className="w-6 h-6 text-purple-600" />
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {stateData.map((state) => (
          <div
            key={state.state}
            className={`${getIntensityColor(state.transactions, maxTransactions)} rounded-lg p-4 text-white hover:scale-105 transition-all duration-300 cursor-pointer`}
          >
            <h3 className="font-semibold text-sm mb-1">{state.state}</h3>
            <p className="text-xs opacity-90">{(state.transactions / 1000000).toFixed(1)}M</p>
            <div className="flex items-center mt-2">
              <TrendingUp className="w-3 h-3 mr-1" />
              <span className="text-xs">+{Math.floor(Math.random() * 20 + 5)}%</span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-6 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">Low</span>
          <div className="flex space-x-1">
            <div className="w-4 h-4 bg-purple-200 rounded"></div>
            <div className="w-4 h-4 bg-purple-300 rounded"></div>
            <div className="w-4 h-4 bg-purple-400 rounded"></div>
            <div className="w-4 h-4 bg-purple-500 rounded"></div>
            <div className="w-4 h-4 bg-purple-600 rounded"></div>
          </div>
          <span className="text-sm text-gray-600">High</span>
        </div>
        <div className="text-sm text-gray-600">
          Transaction Volume Intensity
        </div>
      </div>
    </div>
  );
};

export default HeatMap;