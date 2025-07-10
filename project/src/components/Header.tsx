import React from 'react';
import { TrendingUp, Activity, Users, CreditCard } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
      <div className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
              <Activity className="w-8 h-8 text-purple-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold">PhonePe Pulse</h1>
              <p className="text-purple-100">The beat of progress</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-lg font-medium">Data as of December 2024</p>
            <p className="text-purple-100">Live dashboard insights</p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">Total Transactions</p>
                <p className="text-2xl font-bold">2.28 Cr</p>
                <p className="text-green-300 text-sm flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +12.5% from last month
                </p>
              </div>
              <CreditCard className="w-8 h-8 text-purple-200" />
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">Total Amount</p>
                <p className="text-2xl font-bold">₹39,200 Cr</p>
                <p className="text-green-300 text-sm flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +15.8% from last month
                </p>
              </div>
              <Activity className="w-8 h-8 text-purple-200" />
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">Registered Users</p>
                <p className="text-2xl font-bold">67 Cr</p>
                <p className="text-green-300 text-sm flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +3.2% from last month
                </p>
              </div>
              <Users className="w-8 h-8 text-purple-200" />
            </div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">Avg. Transaction</p>
                <p className="text-2xl font-bold">₹1,720</p>
                <p className="text-green-300 text-sm flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +2.8% from last month
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-purple-200" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;