import React from 'react';
import { TrendingUp, Award, Globe, Zap } from 'lucide-react';

const InsightCards: React.FC = () => {
  const insights = [
    {
      icon: TrendingUp,
      title: 'Digital Adoption',
      value: '89%',
      description: 'Indians now prefer digital payments',
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600'
    },
    {
      icon: Award,
      title: 'Market Leader',
      value: '#1',
      description: 'UPI payment platform in India',
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-600'
    },
    {
      icon: Globe,
      title: 'Rural Penetration',
      value: '78%',
      description: 'Coverage in rural areas',
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600'
    },
    {
      icon: Zap,
      title: 'Transaction Speed',
      value: '2.5s',
      description: 'Average transaction time',
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50',
      textColor: 'text-orange-600'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {insights.map((insight, index) => (
        <div key={index} className={`${insight.bgColor} rounded-xl p-6 border border-gray-100 hover:shadow-lg transition-all duration-300`}>
          <div className="flex items-center justify-between mb-4">
            <div className={`w-12 h-12 bg-gradient-to-r ${insight.color} rounded-lg flex items-center justify-center`}>
              <insight.icon className="w-6 h-6 text-white" />
            </div>
            <div className="text-right">
              <p className={`text-2xl font-bold ${insight.textColor}`}>{insight.value}</p>
            </div>
          </div>
          <h3 className={`font-semibold ${insight.textColor} mb-2`}>{insight.title}</h3>
          <p className="text-sm text-gray-600">{insight.description}</p>
        </div>
      ))}
    </div>
  );
};

export default InsightCards;