import React from 'react';
import { MapPin, TrendingUp } from 'lucide-react';
import { stateData, formatCurrency, formatNumber } from '../data/mockData';

const StateMap: React.FC = () => {
  const topStates = stateData.slice(0, 5);
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Top Performing States</h2>
        <MapPin className="w-6 h-6 text-purple-600" />
      </div>
      
      <div className="space-y-4">
        {topStates.map((state, index) => (
          <div key={state.state} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  {index + 1}
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800">{state.state}</h3>
                <p className="text-sm text-gray-600">{state.district}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-4 text-right">
              <div>
                <p className="text-sm text-gray-600">Transactions</p>
                <p className="font-semibold">{formatNumber(state.transactions)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Amount</p>
                <p className="font-semibold">{formatCurrency(state.amount)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Users</p>
                <p className="font-semibold">{formatNumber(state.users)}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Growth Rate</p>
            <p className="text-lg font-bold text-purple-600">+18.5%</p>
          </div>
          <TrendingUp className="w-6 h-6 text-purple-600" />
        </div>
        <p className="text-sm text-gray-600 mt-2">Compared to previous quarter</p>
      </div>
    </div>
  );
};

export default StateMap;