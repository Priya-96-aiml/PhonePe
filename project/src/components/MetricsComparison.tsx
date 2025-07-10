import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricData {
  label: string;
  current: number;
  previous: number;
  format: 'currency' | 'number' | 'percentage';
}

const MetricsComparison: React.FC = () => {
  const metrics: MetricData[] = [
    { label: 'Total Transactions', current: 2280000000, previous: 2120000000, format: 'number' },
    { label: 'Transaction Value', current: 39200000000, previous: 36500000000, format: 'currency' },
    { label: 'Success Rate', current: 99.9, previous: 99.7, format: 'percentage' },
    { label: 'Average Transaction', current: 1720, previous: 1680, format: 'currency' },
    { label: 'Daily Active Users', current: 45000000, previous: 42000000, format: 'number' },
    { label: 'Merchant Adoption', current: 87.5, previous: 84.2, format: 'percentage' }
  ];

  const formatValue = (value: number, format: string) => {
    switch (format) {
      case 'currency':
        if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)} Cr`;
        if (value >= 100000) return `₹${(value / 100000).toFixed(1)} L`;
        if (value >= 1000) return `₹${(value / 1000).toFixed(1)} K`;
        return `₹${value}`;
      case 'number':
        if (value >= 10000000) return `${(value / 10000000).toFixed(1)} Cr`;
        if (value >= 100000) return `${(value / 100000).toFixed(1)} L`;
        if (value >= 1000) return `${(value / 1000).toFixed(1)} K`;
        return value.toString();
      case 'percentage':
        return `${value}%`;
      default:
        return value.toString();
    }
  };

  const getChangeIcon = (current: number, previous: number) => {
    if (current > previous) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (current < previous) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-500" />;
  };

  const getChangeColor = (current: number, previous: number) => {
    if (current > previous) return 'text-green-600';
    if (current < previous) return 'text-red-600';
    return 'text-gray-600';
  };

  const getChangePercentage = (current: number, previous: number) => {
    const change = ((current - previous) / previous) * 100;
    return Math.abs(change).toFixed(1);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Month-over-Month Comparison</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {metrics.map((metric, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <h3 className="text-sm font-medium text-gray-600 mb-2">{metric.label}</h3>
            
            <div className="flex items-center justify-between mb-3">
              <span className="text-2xl font-bold text-gray-800">
                {formatValue(metric.current, metric.format)}
              </span>
              {getChangeIcon(metric.current, metric.previous)}
            </div>
            
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">
                Previous: {formatValue(metric.previous, metric.format)}
              </span>
              <span className={`font-medium ${getChangeColor(metric.current, metric.previous)}`}>
                {metric.current > metric.previous ? '+' : metric.current < metric.previous ? '-' : ''}
                {getChangePercentage(metric.current, metric.previous)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MetricsComparison;