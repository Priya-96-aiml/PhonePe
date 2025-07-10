import React from 'react';
import { Users, TrendingUp, UserPlus, Target } from 'lucide-react';
import { timeSeriesData, formatNumber } from '../data/mockData';

const UserGrowth: React.FC = () => {
  const latestData = timeSeriesData[timeSeriesData.length - 1];
  const previousData = timeSeriesData[timeSeriesData.length - 2];
  const growthRate = ((latestData.users - previousData.users) / previousData.users * 100).toFixed(1);
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">User Growth Analytics</h2>
        <Users className="w-6 h-6 text-purple-600" />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center">
                <Users className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-purple-600">Total Users</p>
                <p className="text-xl font-bold text-purple-700">{formatNumber(latestData.users)}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-purple-600">Growth</p>
              <p className="text-lg font-bold text-purple-700">+{growthRate}%</p>
            </div>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                <UserPlus className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm text-blue-600">New Users</p>
                <p className="text-xl font-bold text-blue-700">{formatNumber(latestData.users - previousData.users)}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-blue-600">This Month</p>
              <p className="text-lg font-bold text-blue-700">Active</p>
            </div>
          </div>
        </div>
        
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-700">Monthly Growth Trend</h3>
          <div className="space-y-2">
            {timeSeriesData.slice(-6).map((data, index) => {
              const maxUsers = Math.max(...timeSeriesData.map(d => d.users));
              return (
                <div key={data.date} className="flex items-center space-x-3">
                  <div className="w-16 text-sm text-gray-600">
                    {new Date(data.date).toLocaleDateString('en-US', { month: 'short' })}
                  </div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${(data.users / maxUsers) * 100}%` }}
                    />
                  </div>
                  <div className="w-20 text-sm font-medium text-right">
                    {formatNumber(data.users)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600">Active Rate</p>
              <p className="text-xl font-bold text-green-700">87.3%</p>
            </div>
            <Target className="w-6 h-6 text-green-600" />
          </div>
        </div>
        <div className="bg-orange-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-600">Retention</p>
              <p className="text-xl font-bold text-orange-700">94.2%</p>
            </div>
            <TrendingUp className="w-6 h-6 text-orange-600" />
          </div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-600">Avg. Monthly</p>
              <p className="text-xl font-bold text-purple-700">2.1 Cr</p>
            </div>
            <UserPlus className="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserGrowth;