import React from 'react';
import { Activity, Clock, Shield, Zap } from 'lucide-react';
import CircularProgress from './CircularProgress';

const PerformanceMetrics: React.FC = () => {
  const metrics = [
    {
      icon: Activity,
      label: 'Success Rate',
      percentage: 99.9,
      value: '99.9%',
      color: '#10b981',
      description: 'Transaction success rate'
    },
    {
      icon: Clock,
      label: 'Avg Response Time',
      percentage: 85,
      value: '2.5s',
      color: '#3b82f6',
      description: 'Average processing time'
    },
    {
      icon: Shield,
      label: 'Security Score',
      percentage: 98,
      value: '98/100',
      color: '#8b5cf6',
      description: 'Security compliance'
    },
    {
      icon: Zap,
      label: 'Uptime',
      percentage: 99.95,
      value: '99.95%',
      color: '#f59e0b',
      description: 'System availability'
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Performance Metrics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => (
          <div key={index} className="text-center">
            <div className="flex items-center justify-center mb-4">
              <div className="relative">
                <CircularProgress
                  percentage={metric.percentage}
                  color={metric.color}
                  value={metric.value}
                  size={100}
                />
                <div className="absolute top-2 right-2">
                  <metric.icon className="w-5 h-5" style={{ color: metric.color }} />
                </div>
              </div>
            </div>
            <h3 className="font-semibold text-gray-800 mb-1">{metric.label}</h3>
            <p className="text-sm text-gray-600">{metric.description}</p>
          </div>
        ))}
      </div>
      
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4">
          <h4 className="font-semibold text-green-700 mb-2">System Health</h4>
          <p className="text-sm text-green-600">All systems operational</p>
          <div className="flex items-center mt-2">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
            <span className="text-xs text-green-600">Last updated: 2 min ago</span>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4">
          <h4 className="font-semibold text-blue-700 mb-2">Peak Load</h4>
          <p className="text-sm text-blue-600">Handling 50K TPS</p>
          <div className="flex items-center mt-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
            <span className="text-xs text-blue-600">Current capacity: 78%</span>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-4">
          <h4 className="font-semibold text-purple-700 mb-2">Error Rate</h4>
          <p className="text-sm text-purple-600">0.01% error rate</p>
          <div className="flex items-center mt-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
            <span className="text-xs text-purple-600">Within SLA limits</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceMetrics;