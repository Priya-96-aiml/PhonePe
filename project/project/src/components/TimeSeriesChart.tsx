import React from 'react';
import { LineChart, BarChart3 } from 'lucide-react';
import { timeSeriesData, formatCurrency, formatNumber } from '../data/mockData';

interface TimeSeriesChartProps {
  selectedMetric: string;
  chartType: string;
}

const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ selectedMetric, chartType }) => {
  const getMetricValue = (data: any, metric: string) => {
    switch (metric) {
      case 'transactions': return data.transactions;
      case 'amount': return data.amount;
      case 'users': return data.users;
      default: return data.transactions;
    }
  };

  const formatMetricValue = (value: number, metric: string) => {
    switch (metric) {
      case 'amount': return formatCurrency(value);
      default: return formatNumber(value);
    }
  };

  const maxValue = Math.max(...timeSeriesData.map(d => getMetricValue(d, selectedMetric)));
  const minValue = Math.min(...timeSeriesData.map(d => getMetricValue(d, selectedMetric)));

  const getGradientColor = (metric: string) => {
    switch (metric) {
      case 'transactions': return 'from-purple-500 to-purple-600';
      case 'amount': return 'from-blue-500 to-blue-600';
      case 'users': return 'from-green-500 to-green-600';
      default: return 'from-purple-500 to-purple-600';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">
          {selectedMetric.charAt(0).toUpperCase() + selectedMetric.slice(1)} Trends
        </h2>
        <div className="flex items-center space-x-2">
          {chartType === 'line' ? (
            <LineChart className="w-6 h-6 text-purple-600" />
          ) : (
            <BarChart3 className="w-6 h-6 text-purple-600" />
          )}
        </div>
      </div>

      {chartType === 'line' ? (
        <div className="relative h-64">
          <svg className="w-full h-full" viewBox="0 0 800 200">
            <defs>
              <linearGradient id={`gradient-${selectedMetric}`} x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor={selectedMetric === 'transactions' ? '#8b5cf6' : selectedMetric === 'amount' ? '#3b82f6' : '#10b981'} stopOpacity="0.3" />
                <stop offset="100%" stopColor={selectedMetric === 'transactions' ? '#8b5cf6' : selectedMetric === 'amount' ? '#3b82f6' : '#10b981'} stopOpacity="0" />
              </linearGradient>
            </defs>
            
            {/* Grid lines */}
            {[0, 1, 2, 3, 4].map(i => (
              <line
                key={i}
                x1="0"
                y1={i * 40 + 20}
                x2="800"
                y2={i * 40 + 20}
                stroke="#e5e7eb"
                strokeWidth="1"
              />
            ))}
            
            {/* Data line */}
            <polyline
              fill="none"
              stroke={selectedMetric === 'transactions' ? '#8b5cf6' : selectedMetric === 'amount' ? '#3b82f6' : '#10b981'}
              strokeWidth="3"
              points={timeSeriesData.map((data, index) => {
                const x = (index / (timeSeriesData.length - 1)) * 800;
                const y = 180 - ((getMetricValue(data, selectedMetric) - minValue) / (maxValue - minValue)) * 160;
                return `${x},${y}`;
              }).join(' ')}
            />
            
            {/* Area fill */}
            <polygon
              fill={`url(#gradient-${selectedMetric})`}
              points={`0,180 ${timeSeriesData.map((data, index) => {
                const x = (index / (timeSeriesData.length - 1)) * 800;
                const y = 180 - ((getMetricValue(data, selectedMetric) - minValue) / (maxValue - minValue)) * 160;
                return `${x},${y}`;
              }).join(' ')} 800,180`}
            />
            
            {/* Data points */}
            {timeSeriesData.map((data, index) => {
              const x = (index / (timeSeriesData.length - 1)) * 800;
              const y = 180 - ((getMetricValue(data, selectedMetric) - minValue) / (maxValue - minValue)) * 160;
              return (
                <circle
                  key={index}
                  cx={x}
                  cy={y}
                  r="4"
                  fill={selectedMetric === 'transactions' ? '#8b5cf6' : selectedMetric === 'amount' ? '#3b82f6' : '#10b981'}
                  className="hover:r-6 transition-all duration-200"
                />
              );
            })}
          </svg>
          
          {/* X-axis labels */}
          <div className="flex justify-between mt-2 text-sm text-gray-600">
            {timeSeriesData.filter((_, index) => index % 2 === 0).map((data) => (
              <span key={data.date}>
                {new Date(data.date).toLocaleDateString('en-US', { month: 'short' })}
              </span>
            ))}
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {timeSeriesData.slice(-8).map((data, index) => (
            <div key={data.date} className="flex items-center space-x-3">
              <div className="w-16 text-sm text-gray-600">
                {new Date(data.date).toLocaleDateString('en-US', { month: 'short' })}
              </div>
              <div className="flex-1 bg-gray-200 rounded-full h-4">
                <div 
                  className={`bg-gradient-to-r ${getGradientColor(selectedMetric)} h-4 rounded-full transition-all duration-500 flex items-center justify-end pr-2`}
                  style={{ width: `${(getMetricValue(data, selectedMetric) / maxValue) * 100}%` }}
                >
                  <span className="text-xs text-white font-medium">
                    {formatMetricValue(getMetricValue(data, selectedMetric), selectedMetric)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">Peak</p>
          <p className="text-lg font-bold text-gray-800">
            {formatMetricValue(maxValue, selectedMetric)}
          </p>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">Average</p>
          <p className="text-lg font-bold text-gray-800">
            {formatMetricValue(
              timeSeriesData.reduce((sum, d) => sum + getMetricValue(d, selectedMetric), 0) / timeSeriesData.length,
              selectedMetric
            )}
          </p>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">Growth</p>
          <p className="text-lg font-bold text-green-600">
            +{(((getMetricValue(timeSeriesData[timeSeriesData.length - 1], selectedMetric) - 
                 getMetricValue(timeSeriesData[0], selectedMetric)) / 
                 getMetricValue(timeSeriesData[0], selectedMetric)) * 100).toFixed(1)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default TimeSeriesChart;