import React from 'react';
import { Calendar, Filter, BarChart3, LineChart } from 'lucide-react';
import FilterDropdown from './FilterDropdown';

interface DashboardFiltersProps {
  selectedPeriod: string;
  selectedState: string;
  selectedMetric: string;
  chartType: string;
  onPeriodChange: (period: string) => void;
  onStateChange: (state: string) => void;
  onMetricChange: (metric: string) => void;
  onChartTypeChange: (type: string) => void;
}

const DashboardFilters: React.FC<DashboardFiltersProps> = ({
  selectedPeriod,
  selectedState,
  selectedMetric,
  chartType,
  onPeriodChange,
  onStateChange,
  onMetricChange,
  onChartTypeChange
}) => {
  const periodOptions = [
    { value: 'last7days', label: 'Last 7 Days' },
    { value: 'last30days', label: 'Last 30 Days' },
    { value: 'last3months', label: 'Last 3 Months' },
    { value: 'last6months', label: 'Last 6 Months' },
    { value: 'lastyear', label: 'Last Year' },
    { value: 'all', label: 'All Time' }
  ];

  const stateOptions = [
    { value: 'all', label: 'All States' },
    { value: 'maharashtra', label: 'Maharashtra' },
    { value: 'karnataka', label: 'Karnataka' },
    { value: 'delhi', label: 'Delhi' },
    { value: 'tamilnadu', label: 'Tamil Nadu' },
    { value: 'gujarat', label: 'Gujarat' },
    { value: 'uttarpradesh', label: 'Uttar Pradesh' },
    { value: 'westbengal', label: 'West Bengal' },
    { value: 'rajasthan', label: 'Rajasthan' },
    { value: 'haryana', label: 'Haryana' },
    { value: 'punjab', label: 'Punjab' }
  ];

  const metricOptions = [
    { value: 'transactions', label: 'Transactions' },
    { value: 'amount', label: 'Transaction Amount' },
    { value: 'users', label: 'Active Users' }
  ];

  const chartTypeOptions = [
    { value: 'line', label: 'Line Chart' },
    { value: 'bar', label: 'Bar Chart' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Dashboard Filters</h2>
        <Filter className="w-6 h-6 text-purple-600" />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <FilterDropdown
          label="Time Period"
          value={selectedPeriod}
          options={periodOptions}
          onChange={onPeriodChange}
          icon={<Calendar className="w-4 h-4 text-gray-400" />}
        />
        
        <FilterDropdown
          label="State/Region"
          value={selectedState}
          options={stateOptions}
          onChange={onStateChange}
        />
        
        <FilterDropdown
          label="Metric"
          value={selectedMetric}
          options={metricOptions}
          onChange={onMetricChange}
        />
        
        <FilterDropdown
          label="Chart Type"
          value={chartType}
          options={chartTypeOptions}
          onChange={onChartTypeChange}
          icon={chartType === 'line' ? <LineChart className="w-4 h-4 text-gray-400" /> : <BarChart3 className="w-4 h-4 text-gray-400" />}
        />
      </div>
      
      <div className="mt-6 flex flex-wrap gap-2">
        <span className="text-sm text-gray-600">Quick filters:</span>
        <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm hover:bg-purple-200 transition-colors">
          Top 5 States
        </button>
        <button className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200 transition-colors">
          Peak Hours
        </button>
        <button className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm hover:bg-green-200 transition-colors">
          Mobile vs Web
        </button>
        <button className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm hover:bg-orange-200 transition-colors">
          Payment Methods
        </button>
      </div>
    </div>
  );
};

export default DashboardFilters;