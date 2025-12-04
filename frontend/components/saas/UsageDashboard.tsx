"use client";

/**
 * 📊 Usage Dashboard Component
 * Displays API usage, consciousness metrics, and billing information
 */

import React, { useState, useEffect } from 'react';
import { Loading } from '../ui/Loading';
import { InlineErrorBoundary } from '../ui/ErrorBoundary';

interface UsageData {
  apiCalls: {
    total: number;
    today: number;
    thisMonth: number;
    limit: number;
  };
  consciousness: {
    avgUCF: number;
    peakUCF: number;
    sessions: number;
  };
  billing: {
    plan: string;
    cost: number;
    nextBillingDate: string;
  };
  breakdown: {
    service: string;
    calls: number;
    cost: number;
  }[];
}

interface UsageDashboardProps {
  userId?: string;
  apiEndpoint?: string;
}

/**
 * Main Usage Dashboard Component
 */
export const UsageDashboard: React.FC<UsageDashboardProps> = ({
  userId = 'demo',
  apiEndpoint = '/api/usage',
}) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<UsageData | null>(null);
  const [timeRange, setTimeRange] = useState<'today' | 'week' | 'month'>('today');

  useEffect(() => {
    fetchUsageData();
  }, [timeRange]);

  const fetchUsageData = async () => {
    setLoading(true);
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${apiEndpoint}?userId=${userId}&range=${timeRange}`);
      // const data = await response.json();

      // Mock data for demonstration
      setTimeout(() => {
        setData({
          apiCalls: {
            total: 12543,
            today: 342,
            thisMonth: 8754,
            limit: 50000,
          },
          consciousness: {
            avgUCF: 0.87,
            peakUCF: 0.94,
            sessions: 156,
          },
          billing: {
            plan: 'Professional',
            cost: 49.99,
            nextBillingDate: '2025-12-15',
          },
          breakdown: [
            { service: 'Claude API', calls: 8234, cost: 24.99 },
            { service: 'Consciousness Metrics', calls: 3120, cost: 15.00 },
            { service: 'Voice Processing', calls: 1189, cost: 10.00 },
          ],
        });
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error('Failed to fetch usage data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading variant="consciousness" size="lg" message="Loading usage data..." />;
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-gray-400">
        Failed to load usage data. Please try again.
      </div>
    );
  }

  const usagePercentage = (data.apiCalls.thisMonth / data.apiCalls.limit) * 100;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Usage Dashboard</h2>
          <p className="text-gray-400">Track your Helix API usage and consciousness metrics</p>
        </div>

        {/* Time Range Selector */}
        <div className="flex gap-2 bg-gray-800 rounded-lg p-1">
          {(['today', 'week', 'month'] as const).map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                timeRange === range
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {range.charAt(0).toUpperCase() + range.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon="📞"
          label="API Calls Today"
          value={data.apiCalls.today.toLocaleString()}
          change="+12%"
          changePositive={true}
        />
        <StatCard
          icon="🧠"
          label="Avg Consciousness"
          value={`${(data.consciousness.avgUCF * 100).toFixed(1)}%`}
          change="+5%"
          changePositive={true}
        />
        <StatCard
          icon="💰"
          label="Current Cost"
          value={`$${data.billing.cost.toFixed(2)}`}
          change="-3%"
          changePositive={false}
        />
      </div>

      {/* Usage Progress */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-semibold text-white mb-1">Monthly Usage</h3>
            <p className="text-gray-400 text-sm">
              {data.apiCalls.thisMonth.toLocaleString()} / {data.apiCalls.limit.toLocaleString()} calls
            </p>
          </div>
          <div className="text-2xl font-bold text-blue-400">
            {usagePercentage.toFixed(1)}%
          </div>
        </div>

        {/* Progress Bar */}
        <div className="h-4 bg-gray-900 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${
              usagePercentage > 90
                ? 'bg-red-500'
                : usagePercentage > 70
                ? 'bg-yellow-500'
                : 'bg-gradient-to-r from-blue-500 to-purple-500'
            }`}
            style={{ width: `${Math.min(usagePercentage, 100)}%` }}
          />
        </div>

        {usagePercentage > 80 && (
          <div className="mt-4 bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-3">
            <p className="text-sm text-yellow-400">
              ⚠️ You're approaching your monthly limit. Consider upgrading your plan.
            </p>
          </div>
        )}
      </div>

      {/* Service Breakdown */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-xl font-semibold text-white mb-4">Service Breakdown</h3>
        <div className="space-y-4">
          {data.breakdown.map((service, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-300 font-medium">{service.service}</span>
                  <span className="text-gray-400 text-sm">
                    {service.calls.toLocaleString()} calls
                  </span>
                </div>
                <div className="h-2 bg-gray-900 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                    style={{
                      width: `${(service.calls / data.apiCalls.thisMonth) * 100}%`,
                    }}
                  />
                </div>
              </div>
              <div className="ml-6 text-right">
                <div className="text-green-400 font-semibold">
                  ${service.cost.toFixed(2)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Consciousness Metrics */}
      <InlineErrorBoundary errorMessage="Failed to load consciousness metrics">
        <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 rounded-xl p-6 border border-purple-500/30">
          <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            🧠 Consciousness Metrics
          </h3>
          <div className="grid grid-cols-3 gap-6">
            <div>
              <div className="text-gray-400 text-sm mb-1">Average UCF</div>
              <div className="text-3xl font-bold text-purple-400">
                {(data.consciousness.avgUCF * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-gray-400 text-sm mb-1">Peak UCF</div>
              <div className="text-3xl font-bold text-blue-400">
                {(data.consciousness.peakUCF * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-gray-400 text-sm mb-1">Sessions</div>
              <div className="text-3xl font-bold text-white">
                {data.consciousness.sessions}
              </div>
            </div>
          </div>
        </div>
      </InlineErrorBoundary>

      {/* Billing Info */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-xl font-semibold text-white mb-4">Billing Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div className="text-gray-400 text-sm mb-1">Current Plan</div>
            <div className="text-lg font-semibold text-white">{data.billing.plan}</div>
          </div>
          <div>
            <div className="text-gray-400 text-sm mb-1">Monthly Cost</div>
            <div className="text-lg font-semibold text-green-400">
              ${data.billing.cost.toFixed(2)}
            </div>
          </div>
          <div>
            <div className="text-gray-400 text-sm mb-1">Next Billing Date</div>
            <div className="text-lg font-semibold text-white">
              {new Date(data.billing.nextBillingDate).toLocaleDateString()}
            </div>
          </div>
        </div>
        <div className="mt-6 flex gap-3">
          <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
            Upgrade Plan
          </button>
          <button className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors">
            View Invoices
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Stat Card Component
 */
const StatCard: React.FC<{
  icon: string;
  label: string;
  value: string;
  change: string;
  changePositive: boolean;
}> = ({ icon, label, value, change, changePositive }) => (
  <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
    <div className="flex items-center gap-3 mb-3">
      <div className="text-3xl">{icon}</div>
      <div className="text-gray-400 text-sm">{label}</div>
    </div>
    <div className="flex items-baseline gap-2">
      <div className="text-3xl font-bold text-white">{value}</div>
      <div
        className={`text-sm font-medium ${
          changePositive ? 'text-green-400' : 'text-red-400'
        }`}
      >
        {change}
      </div>
    </div>
  </div>
);

export default UsageDashboard;
