import React, { useState } from 'react';
import { BarChart3, PieChart, Map, TrendingUp, Filter, Eye } from 'lucide-react';

interface VisualizationProps {
  selectedDataset: string;
}

const DataVisualization: React.FC<VisualizationProps> = ({ selectedDataset }) => {
  const [viewType, setViewType] = useState<'chart' | 'table' | 'map'>('chart');
  const [filterState, setFilterState] = useState<string>('all');

  const sampleData = {
    'aggregate-transaction': [
      { state: 'Maharashtra', transactions: 15420000, amount: 2840000000, type: 'P2P' },
      { state: 'Karnataka', transactions: 12350000, amount: 2100000000, type: 'P2P' },
      { state: 'Delhi', transactions: 9800000, amount: 1850000000, type: 'Merchant' },
      { state: 'Tamil Nadu', transactions: 8900000, amount: 1650000000, type: 'P2P' },
      { state: 'Gujarat', transactions: 7800000, amount: 1420000000, type: 'Merchant' }
    ],
    'aggregate-user': [
      { state: 'Maharashtra', users: 8500000, appOpens: 45000000, brand: 'Android' },
      { state: 'Karnataka', users: 7200000, appOpens: 38000000, brand: 'iOS' },
      { state: 'Delhi', users: 5800000, appOpens: 32000000, brand: 'Android' },
      { state: 'Tamil Nadu', users: 5200000, appOpens: 28000000, brand: 'Android' },
      { state: 'Gujarat', users: 4600000, appOpens: 25000000, brand: 'iOS' }
    ]
  };

  const getCurrentData = () => {
    return sampleData[selectedDataset as keyof typeof sampleData] || sampleData['aggregate-transaction'];
  };

  const formatNumber = (num: number) => {
    if (num >= 10000000) return `${(num / 10000000).toFixed(1)}Cr`;
    if (num >= 100000) return `${(num / 100000).toFixed(1)}L`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const formatCurrency = (amount: number) => {
    if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)}Cr`;
    if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)}L`;
    if (amount >= 1000) return `₹${(amount / 1000).toFixed(1)}K`;
    return `₹${amount}`;
  };

  const renderChart = () => {
    const data = getCurrentData();
    const maxValue = Math.max(...data.map(d => d.transactions || d.users || 0));

    return (
      <div className="space-y-4">
        {data.map((item, index) => (
          <div key={index} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="w-20 text-sm font-medium text-gray-700">{item.state}</div>
            <div className="flex-1 bg-gray-200 rounded-full h-4">
              <div
                className="bg-gradient-to-r from-purple-500 to-purple-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${((item.transactions || item.users || 0) / maxValue) * 100}%` }}
              />
            </div>
            <div className="w-24 text-sm font-medium text-right">
              {selectedDataset.includes('transaction') 
                ? formatNumber(item.transactions || 0)
                : formatNumber(item.users || 0)
              }
            </div>
            {selectedDataset.includes('transaction') && item.amount && (
              <div className="w-24 text-sm text-gray-600 text-right">
                {formatCurrency(item.amount)}
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderTable = () => {
    const data = getCurrentData();
    
    return (
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-200 px-4 py-2 text-left">State</th>
              {selectedDataset.includes('transaction') ? (
                <>
                  <th className="border border-gray-200 px-4 py-2 text-left">Transactions</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Amount</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Type</th>
                </>
              ) : (
                <>
                  <th className="border border-gray-200 px-4 py-2 text-left">Users</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">App Opens</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Brand</th>
                </>
              )}
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="border border-gray-200 px-4 py-2 font-medium">{item.state}</td>
                {selectedDataset.includes('transaction') ? (
                  <>
                    <td className="border border-gray-200 px-4 py-2">{formatNumber(item.transactions || 0)}</td>
                    <td className="border border-gray-200 px-4 py-2">{formatCurrency(item.amount || 0)}</td>
                    <td className="border border-gray-200 px-4 py-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        item.type === 'P2P' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {item.type}
                      </span>
                    </td>
                  </>
                ) : (
                  <>
                    <td className="border border-gray-200 px-4 py-2">{formatNumber(item.users || 0)}</td>
                    <td className="border border-gray-200 px-4 py-2">{formatNumber(item.appOpens || 0)}</td>
                    <td className="border border-gray-200 px-4 py-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        item.brand === 'Android' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {item.brand}
                      </span>
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderMap = () => {
    const data = getCurrentData();
    
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {data.map((item, index) => {
          const intensity = selectedDataset.includes('transaction') 
            ? (item.transactions || 0) / Math.max(...data.map(d => d.transactions || 0))
            : (item.users || 0) / Math.max(...data.map(d => d.users || 0));
          
          const getColor = () => {
            if (intensity > 0.8) return 'bg-purple-600';
            if (intensity > 0.6) return 'bg-purple-500';
            if (intensity > 0.4) return 'bg-purple-400';
            if (intensity > 0.2) return 'bg-purple-300';
            return 'bg-purple-200';
          };

          return (
            <div
              key={index}
              className={`${getColor()} rounded-lg p-4 text-white hover:scale-105 transition-all duration-300 cursor-pointer`}
            >
              <h3 className="font-semibold text-sm mb-1">{item.state}</h3>
              <p className="text-xs opacity-90">
                {selectedDataset.includes('transaction') 
                  ? formatNumber(item.transactions || 0)
                  : formatNumber(item.users || 0)
                }
              </p>
              <div className="flex items-center mt-2">
                <TrendingUp className="w-3 h-3 mr-1" />
                <span className="text-xs">+{Math.floor(Math.random() * 20 + 5)}%</span>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-800">Data Visualization</h3>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setViewType('chart')}
            className={`p-2 rounded-lg transition-colors ${
              viewType === 'chart' ? 'bg-purple-100 text-purple-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <BarChart3 className="w-5 h-5" />
          </button>
          <button
            onClick={() => setViewType('table')}
            className={`p-2 rounded-lg transition-colors ${
              viewType === 'table' ? 'bg-purple-100 text-purple-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Eye className="w-5 h-5" />
          </button>
          <button
            onClick={() => setViewType('map')}
            className={`p-2 rounded-lg transition-colors ${
              viewType === 'map' ? 'bg-purple-100 text-purple-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Map className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="mb-4">
        <select
          value={filterState}
          onChange={(e) => setFilterState(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="all">All States</option>
          <option value="maharashtra">Maharashtra</option>
          <option value="karnataka">Karnataka</option>
          <option value="delhi">Delhi</option>
          <option value="tamilnadu">Tamil Nadu</option>
          <option value="gujarat">Gujarat</option>
        </select>
      </div>

      <div className="min-h-[400px]">
        {viewType === 'chart' && renderChart()}
        {viewType === 'table' && renderTable()}
        {viewType === 'map' && renderMap()}
      </div>
    </div>
  );
};

export default DataVisualization;