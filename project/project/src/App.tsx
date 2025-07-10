import React, { useState } from 'react';
import Header from './components/Header';
import InsightCards from './components/InsightCards';
import DashboardFilters from './components/DashboardFilters';
import DatasetSelector from './components/DatasetSelector';
import DataVisualization from './components/DataVisualization';
import TimeSeriesChart from './components/TimeSeriesChart';
import StateMap from './components/StateMap';
import CategoryBreakdown from './components/CategoryBreakdown';
import UserGrowth from './components/UserGrowth';
import HeatMap from './components/HeatMap';
import MetricsComparison from './components/MetricsComparison';
import PerformanceMetrics from './components/PerformanceMetrics';
import Footer from './components/Footer';

function App() {
  const [selectedPeriod, setSelectedPeriod] = useState('last6months');
  const [selectedState, setSelectedState] = useState('all');
  const [selectedMetric, setSelectedMetric] = useState('transactions');
  const [chartType, setChartType] = useState('line');
  const [selectedDataset, setSelectedDataset] = useState('aggregate-transaction');

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <InsightCards />
        
        <DatasetSelector />
        
        <DataVisualization selectedDataset={selectedDataset} />
        
        <DashboardFilters
          selectedPeriod={selectedPeriod}
          selectedState={selectedState}
          selectedMetric={selectedMetric}
          chartType={chartType}
          onPeriodChange={setSelectedPeriod}
          onStateChange={setSelectedState}
          onMetricChange={setSelectedMetric}
          onChartTypeChange={setChartType}
        />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <TimeSeriesChart selectedMetric={selectedMetric} chartType={chartType} />
          </div>
          <div>
            <StateMap />
          </div>
        </div>
        
        <div className="mb-8">
          <HeatMap />
        </div>
        
        <div className="mb-8">
          <MetricsComparison />
        </div>
        
        <div className="mb-8">
          <PerformanceMetrics />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <CategoryBreakdown />
          <UserGrowth />
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Key Highlights 2024</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
              <h3 className="text-lg font-semibold text-purple-700 mb-2">Digital Revolution</h3>
              <p className="text-sm text-purple-600">India processes 12 billion UPI transactions monthly, making it the world's largest real-time payment system.</p>
            </div>
            <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
              <h3 className="text-lg font-semibold text-blue-700 mb-2">Financial Inclusion</h3>
              <p className="text-sm text-blue-600">Over 67 crore Indians now have access to digital payment services, bridging the urban-rural divide.</p>
            </div>
            <div className="text-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
              <h3 className="text-lg font-semibold text-green-700 mb-2">Economic Impact</h3>
              <p className="text-sm text-green-600">Digital payments contribute to 15% of India's GDP growth, driving the digital economy forward.</p>
            </div>
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;