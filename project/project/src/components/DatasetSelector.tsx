import React, { useState } from 'react';
import { Database, Download, FileText, Users, MapPin, TrendingUp, BarChart3, PieChart } from 'lucide-react';

interface DatasetOption {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  category: 'transaction' | 'user' | 'map' | 'top';
  dataPoints: string[];
  sampleSize: string;
  lastUpdated: string;
}

const DatasetSelector: React.FC = () => {
  const [selectedDataset, setSelectedDataset] = useState<string>('aggregate-transaction');
  const [selectedYear, setSelectedYear] = useState<string>('2024');
  const [selectedQuarter, setSelectedQuarter] = useState<string>('Q4');

  const datasets: DatasetOption[] = [
    {
      id: 'aggregate-transaction',
      title: 'Aggregate Transaction',
      description: 'State-wise transaction data aggregated by payment type and time period',
      icon: <BarChart3 className="w-6 h-6" />,
      category: 'transaction',
      dataPoints: ['Transaction Count', 'Transaction Amount', 'Payment Type', 'State', 'Year', 'Quarter'],
      sampleSize: '2.8M records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'aggregate-user',
      title: 'Aggregate User',
      description: 'User registration and engagement metrics by state and time period',
      icon: <Users className="w-6 h-6" />,
      category: 'user',
      dataPoints: ['Registered Users', 'App Opens', 'State', 'Brand', 'Year', 'Quarter'],
      sampleSize: '1.2M records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'map-transaction',
      title: 'Map Transaction',
      description: 'District-wise transaction data for geographical visualization',
      icon: <MapPin className="w-6 h-6" />,
      category: 'map',
      dataPoints: ['District', 'Transaction Count', 'Transaction Amount', 'State', 'Year', 'Quarter'],
      sampleSize: '750K records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'map-user',
      title: 'Map User',
      description: 'District-wise user data for geographical analysis',
      icon: <MapPin className="w-6 h-6" />,
      category: 'map',
      dataPoints: ['District', 'Registered Users', 'App Opens', 'State', 'Year', 'Quarter'],
      sampleSize: '650K records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'top-transaction-district',
      title: 'Top Transaction Districtwise',
      description: 'Top performing districts by transaction volume and value',
      icon: <TrendingUp className="w-6 h-6" />,
      category: 'top',
      dataPoints: ['District', 'Transaction Count', 'Transaction Amount', 'State', 'Year', 'Quarter'],
      sampleSize: '50K records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'top-transaction-pincode',
      title: 'Top Transaction Pincodewise',
      description: 'Top performing pincodes by transaction metrics',
      icon: <TrendingUp className="w-6 h-6" />,
      category: 'top',
      dataPoints: ['Pincode', 'Transaction Count', 'Transaction Amount', 'District', 'State', 'Year', 'Quarter'],
      sampleSize: '100K records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'top-user-district',
      title: 'Top User Districtwise',
      description: 'Top districts by user engagement and registration',
      icon: <Users className="w-6 h-6" />,
      category: 'top',
      dataPoints: ['District', 'Registered Users', 'App Opens', 'State', 'Year', 'Quarter'],
      sampleSize: '45K records',
      lastUpdated: 'Dec 2024'
    },
    {
      id: 'top-user-pincode',
      title: 'Top User Pincodewise',
      description: 'Top pincodes by user metrics and engagement',
      icon: <Users className="w-6 h-6" />,
      category: 'top',
      dataPoints: ['Pincode', 'Registered Users', 'App Opens', 'District', 'State', 'Year', 'Quarter'],
      sampleSize: '80K records',
      lastUpdated: 'Dec 2024'
    }
  ];

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'transaction': return 'bg-purple-100 text-purple-700 border-purple-200';
      case 'user': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'map': return 'bg-green-100 text-green-700 border-green-200';
      case 'top': return 'bg-orange-100 text-orange-700 border-orange-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'transaction': return <BarChart3 className="w-4 h-4" />;
      case 'user': return <Users className="w-4 h-4" />;
      case 'map': return <MapPin className="w-4 h-4" />;
      case 'top': return <TrendingUp className="w-4 h-4" />;
      default: return <Database className="w-4 h-4" />;
    }
  };

  const handleDownload = (format: 'csv' | 'json' | 'excel') => {
    const selectedData = datasets.find(d => d.id === selectedDataset);
    if (selectedData) {
      // Simulate download
      console.log(`Downloading ${selectedData.title} in ${format.toUpperCase()} format for ${selectedYear} ${selectedQuarter}`);
      
      // Create a mock download
      const element = document.createElement('a');
      const file = new Blob([`PhonePe ${selectedData.title} Data - ${selectedYear} ${selectedQuarter}`], { type: 'text/plain' });
      element.href = URL.createObjectURL(file);
      element.download = `phonepe_${selectedDataset}_${selectedYear}_${selectedQuarter}.${format}`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  };

  const generateReport = () => {
    const selectedData = datasets.find(d => d.id === selectedDataset);
    if (selectedData) {
      console.log(`Generating report for ${selectedData.title}`);
      // Simulate report generation
      alert(`Report generated for ${selectedData.title} - ${selectedYear} ${selectedQuarter}`);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Database className="w-8 h-8 text-purple-600" />
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Select Dataset</h2>
            <p className="text-gray-600">Choose from PhonePe Pulse data categories</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
          </select>
          <select
            value={selectedQuarter}
            onChange={(e) => setSelectedQuarter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="Q1">Q1</option>
            <option value="Q2">Q2</option>
            <option value="Q3">Q3</option>
            <option value="Q4">Q4</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            onClick={() => setSelectedDataset(dataset.id)}
            className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${
              selectedDataset === dataset.id
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className={`p-2 rounded-lg ${getCategoryColor(dataset.category)}`}>
                {dataset.icon}
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getCategoryColor(dataset.category)}`}>
                {getCategoryIcon(dataset.category)}
                <span>{dataset.category}</span>
              </span>
            </div>
            
            <h3 className="font-semibold text-gray-800 mb-2">{dataset.title}</h3>
            <p className="text-sm text-gray-600 mb-3">{dataset.description}</p>
            
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-500">Records:</span>
                <span className="font-medium">{dataset.sampleSize}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-500">Updated:</span>
                <span className="font-medium">{dataset.lastUpdated}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedDataset && (
        <div className="border-t pt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Dataset Details</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-800 mb-2">
                  {datasets.find(d => d.id === selectedDataset)?.title}
                </h4>
                <p className="text-sm text-gray-600 mb-3">
                  {datasets.find(d => d.id === selectedDataset)?.description}
                </p>
                
                <div className="space-y-2">
                  <h5 className="font-medium text-gray-700">Data Points:</h5>
                  <div className="flex flex-wrap gap-2">
                    {datasets.find(d => d.id === selectedDataset)?.dataPoints.map((point, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-600"
                      >
                        {point}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Download Options</h3>
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-3">
                  <button
                    onClick={() => handleDownload('csv')}
                    className="flex items-center justify-center space-x-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span>CSV</span>
                  </button>
                  <button
                    onClick={() => handleDownload('json')}
                    className="flex items-center justify-center space-x-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span>JSON</span>
                  </button>
                  <button
                    onClick={() => handleDownload('excel')}
                    className="flex items-center justify-center space-x-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span>Excel</span>
                  </button>
                </div>

                <button
                  onClick={generateReport}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
                >
                  <FileText className="w-4 h-4" />
                  <span>Generate Report</span>
                </button>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h5 className="font-medium text-blue-800 mb-2">Selected Configuration</h5>
                  <div className="space-y-1 text-sm text-blue-700">
                    <p><strong>Dataset:</strong> {datasets.find(d => d.id === selectedDataset)?.title}</p>
                    <p><strong>Period:</strong> {selectedYear} {selectedQuarter}</p>
                    <p><strong>Size:</strong> {datasets.find(d => d.id === selectedDataset)?.sampleSize}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-semibold text-gray-800">PhonePe Pulse Data</h4>
            <p className="text-sm text-gray-600">Real-time insights into India's digital payment ecosystem</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Made with</p>
            <p className="font-semibold text-purple-600">React & TypeScript</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatasetSelector;