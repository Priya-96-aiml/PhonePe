import React from 'react';
import { BarChart3, Calendar } from 'lucide-react';
import { timeSeriesData, formatCurrency, formatNumber } from '../data/mockData';

const TransactionChart: React.FC = () => {
  const maxTransactions = Math.max(...timeSeriesData.map(d => d.transactions));
  const maxAmount = Math.max(...timeSeriesData.map(d => d.amount));
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Transaction Trends 2024</h2>
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-6 h-6 text-purple-600" />
          <Calendar className="w-6 h-6 text-purple-600" />
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Transaction Volume</h3>
          <div className="space-y-3">
            {timeSeriesData.slice(-6).map((data, index) => (
              <div key={data.date} className="flex items-center space-x-3">
                <div className="w-16 text-sm text-gray-600">
                  {new Date(data.date).toLocaleDateString('en-US', { month: 'short' })}
                </div>
                <div className="flex-1 bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-purple-500 to-purple-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${(data.transactions / maxTransactions) * 100}%` }}
                  />
                </div>
                <div className="w-24 text-sm font-medium text-right">
                  {formatNumber(data.transactions)}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Transaction Amount</h3>
          <div className="space-y-3">
            {timeSeriesData.slice(-6).map((data, index) => (
              <div key={data.date} className="flex items-center space-x-3">
                <div className="w-16 text-sm text-gray-600">
                  {new Date(data.date).toLocaleDateString('en-US', { month: 'short' })}
                </div>
                <div className="flex-1 bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${(data.amount / maxAmount) * 100}%` }}
                  />
                </div>
                <div className="w-24 text-sm font-medium text-right">
                  {formatCurrency(data.amount)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-purple-600 font-medium">Peak Month</p>
          <p className="text-xl font-bold text-purple-700">December</p>
          <p className="text-sm text-purple-600">{formatNumber(timeSeriesData[timeSeriesData.length - 1].transactions)} transactions</p>
        </div>
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-600 font-medium">Growth Rate</p>
          <p className="text-xl font-bold text-blue-700">+168%</p>
          <p className="text-sm text-blue-600">Year over year</p>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <p className="text-sm text-green-600 font-medium">Avg. Monthly</p>
          <p className="text-xl font-bold text-green-700">1.55 Cr</p>
          <p className="text-sm text-green-600">Transactions</p>
        </div>
      </div>
    </div>
  );
};

export default TransactionChart;