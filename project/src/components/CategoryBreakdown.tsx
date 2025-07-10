import React from 'react';
import { PieChart, Smartphone, ShoppingBag, Zap, Building } from 'lucide-react';
import { categoryData, formatNumber } from '../data/mockData';

const CategoryBreakdown: React.FC = () => {
  const icons = [Smartphone, ShoppingBag, Zap, Building];
  const colors = ['bg-purple-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500'];
  const lightColors = ['bg-purple-100', 'bg-blue-100', 'bg-green-100', 'bg-yellow-100'];
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Payment Categories</h2>
        <PieChart className="w-6 h-6 text-purple-600" />
      </div>
      
      <div className="space-y-4">
        {categoryData.map((category, index) => {
          const Icon = icons[index];
          return (
            <div key={category.category} className="flex items-center justify-between p-4 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-center space-x-4">
                <div className={`w-12 h-12 ${lightColors[index]} rounded-lg flex items-center justify-center`}>
                  <Icon className={`w-6 h-6 ${colors[index].replace('bg-', 'text-')}`} />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800">{category.category}</h3>
                  <p className="text-sm text-gray-600">{formatNumber(category.transactions)} transactions</p>
                </div>
              </div>
              
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-800">{category.percentage}%</p>
                <div className="w-24 bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className={`${colors[index]} h-2 rounded-full transition-all duration-500`}
                    style={{ width: `${category.percentage}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-6 p-4 bg-gradient-to-r from-gray-50 to-purple-50 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Most Popular</p>
            <p className="text-lg font-bold text-purple-600">Peer-to-peer payments</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Market Share</p>
            <p className="text-lg font-bold text-purple-600">52.6%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoryBreakdown;