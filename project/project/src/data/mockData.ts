// Mock PhonePe Pulse data for 2024
export interface TransactionData {
  state: string;
  district: string;
  transactions: number;
  amount: number;
  users: number;
}

export interface TimeSeriesData {
  date: string;
  transactions: number;
  amount: number;
  users: number;
}

export interface CategoryData {
  category: string;
  transactions: number;
  percentage: number;
}

export const stateData: TransactionData[] = [
  { state: "Maharashtra", district: "Mumbai", transactions: 15420000, amount: 2840000000, users: 8500000 },
  { state: "Karnataka", district: "Bengaluru", transactions: 12350000, amount: 2100000000, users: 7200000 },
  { state: "Delhi", district: "New Delhi", transactions: 9800000, amount: 1850000000, users: 5800000 },
  { state: "Tamil Nadu", district: "Chennai", transactions: 8900000, amount: 1650000000, users: 5200000 },
  { state: "Gujarat", district: "Ahmedabad", transactions: 7800000, amount: 1420000000, users: 4600000 },
  { state: "Uttar Pradesh", district: "Lucknow", transactions: 7200000, amount: 1320000000, users: 4200000 },
  { state: "West Bengal", district: "Kolkata", transactions: 6500000, amount: 1180000000, users: 3800000 },
  { state: "Rajasthan", district: "Jaipur", transactions: 5800000, amount: 1050000000, users: 3400000 },
  { state: "Haryana", district: "Gurugram", transactions: 5200000, amount: 980000000, users: 3100000 },
  { state: "Punjab", district: "Ludhiana", transactions: 4600000, amount: 850000000, users: 2700000 },
];

export const timeSeriesData: TimeSeriesData[] = [
  { date: "2024-01", transactions: 850000000, amount: 15200000000, users: 45000000 },
  { date: "2024-02", transactions: 920000000, amount: 16800000000, users: 47000000 },
  { date: "2024-03", transactions: 1050000000, amount: 18500000000, users: 49000000 },
  { date: "2024-04", transactions: 1180000000, amount: 20200000000, users: 51000000 },
  { date: "2024-05", transactions: 1320000000, amount: 22800000000, users: 53000000 },
  { date: "2024-06", transactions: 1450000000, amount: 24500000000, users: 55000000 },
  { date: "2024-07", transactions: 1580000000, amount: 26200000000, users: 57000000 },
  { date: "2024-08", transactions: 1720000000, amount: 28800000000, users: 59000000 },
  { date: "2024-09", transactions: 1850000000, amount: 31200000000, users: 61000000 },
  { date: "2024-10", transactions: 1980000000, amount: 33800000000, users: 63000000 },
  { date: "2024-11", transactions: 2120000000, amount: 36500000000, users: 65000000 },
  { date: "2024-12", transactions: 2280000000, amount: 39200000000, users: 67000000 },
];

export const categoryData: CategoryData[] = [
  { category: "Peer-to-peer payments", transactions: 1200000000, percentage: 52.6 },
  { category: "Merchant payments", transactions: 650000000, percentage: 28.5 },
  { category: "Recharge & bill payments", transactions: 280000000, percentage: 12.3 },
  { category: "Financial services", transactions: 150000000, percentage: 6.6 },
];

export const formatCurrency = (amount: number): string => {
  if (amount >= 10000000) {
    return `₹${(amount / 10000000).toFixed(1)} Cr`;
  } else if (amount >= 100000) {
    return `₹${(amount / 100000).toFixed(1)} L`;
  } else if (amount >= 1000) {
    return `₹${(amount / 1000).toFixed(1)} K`;
  }
  return `₹${amount}`;
};

export const formatNumber = (num: number): string => {
  if (num >= 10000000) {
    return `${(num / 10000000).toFixed(1)} Cr`;
  } else if (num >= 100000) {
    return `${(num / 100000).toFixed(1)} L`;
  } else if (num >= 1000) {
    return `${(num / 1000).toFixed(1)} K`;
  }
  return num.toString();
};