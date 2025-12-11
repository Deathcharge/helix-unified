/**
 * 📊 Analytics Dashboard
 * View and export usage analytics, metrics, and reports
 *
 * VILLAIN ANALYTICS: TRACK YOUR DOMINATION 😈
 */

import React, { useState, useEffect } from 'react';

interface UsageStats {
  total_api_calls: number;
  total_agent_sessions: number;
  total_web_os_sessions: number;
  total_tokens_used: number;
  date_range: {
    start: string;
    end: string;
  };
  breakdown_by_endpoint: Record<string, number>;
  breakdown_by_agent: Record<string, number>;
}

interface BillingSummary {
  subscription_tier: string;
  subscription_status: string;
  billing_period: {
    start: string;
    end: string;
  };
  costs: {
    base_subscription: number;
    agent_usage: number;
    total: number;
  };
  usage: {
    api_calls: number;
    agent_credits_used: number;
    team_members: number;
  };
}

export default function AnalyticsDashboard() {
  const [stats, setStats] = useState<UsageStats | null>(null);
  const [billingSummary, setBillingSummary] = useState<BillingSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState<'7d' | '30d' | '90d' | 'all'>('30d');
  const [exportFormat, setExportFormat] = useState<'csv' | 'json'>('csv');

  useEffect(() => {
    fetchAnalytics();
  }, [dateRange]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      // Calculate date range
      const end = new Date().toISOString();
      const start = new Date();
      if (dateRange === '7d') start.setDate(start.getDate() - 7);
      else if (dateRange === '30d') start.setDate(start.getDate() - 30);
      else if (dateRange === '90d') start.setDate(start.getDate() - 90);
      else start.setFullYear(2020); // All time

      // Fetch usage stats
      const statsRes = await fetch(
        `/api/analytics/usage?start_date=${start.toISOString()}&end_date=${end}`
      );
      const statsData = await statsRes.json();
      setStats(statsData);

      // Fetch billing summary
      const billingRes = await fetch(
        `/api/analytics/billing-summary?start_date=${start.toISOString()}&end_date=${end}`
      );
      const billingData = await billingRes.json();
      setBillingSummary(billingData);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (type: 'usage' | 'agent-sessions') => {
    try {
      const end = new Date().toISOString();
      const start = new Date();
      if (dateRange === '7d') start.setDate(start.getDate() - 7);
      else if (dateRange === '30d') start.setDate(start.getDate() - 30);
      else if (dateRange === '90d') start.setDate(start.getDate() - 90);
      else start.setFullYear(2020);

      const url = `/api/analytics/export/${type}?format=${exportFormat}&start_date=${start.toISOString()}&end_date=${end}`;

      // Download file
      const response = await fetch(url);
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `${type}_export_${new Date().toISOString().split('T')[0]}.${exportFormat}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (!stats || !billingSummary) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">📊 No Data Available</h2>
          <p className="text-gray-400">Start using the platform to see analytics</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">📊 Analytics Dashboard</h1>
            <p className="text-gray-400">Usage metrics and billing insights</p>
          </div>

          {/* Date Range Selector */}
          <div className="flex space-x-2">
            {(['7d', '30d', '90d', 'all'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setDateRange(range)}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  dateRange === range
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {range === 'all' ? 'All Time' : `Last ${range}`}
              </button>
            ))}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="API Calls"
            value={stats.total_api_calls.toLocaleString()}
            icon="📡"
            color="blue"
          />
          <StatCard
            title="Agent Sessions"
            value={stats.total_agent_sessions.toLocaleString()}
            icon="🤖"
            color="purple"
          />
          <StatCard
            title="Tokens Used"
            value={stats.total_tokens_used.toLocaleString()}
            icon="🔢"
            color="green"
          />
          <StatCard
            title="Web OS Sessions"
            value={stats.total_web_os_sessions.toLocaleString()}
            icon="💻"
            color="orange"
          />
        </div>

        {/* Billing Summary */}
        <div className="bg-gray-800 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">💰 Billing Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-gray-400 mb-1">Subscription Plan</div>
              <div className="text-2xl font-bold capitalize">{billingSummary.subscription_tier}</div>
              <div className={`text-sm mt-1 ${
                billingSummary.subscription_status === 'active' ? 'text-green-400' : 'text-red-400'
              }`}>
                {billingSummary.subscription_status}
              </div>
            </div>
            <div>
              <div className="text-gray-400 mb-1">Current Period Cost</div>
              <div className="text-2xl font-bold text-green-400">
                ${billingSummary.costs.total.toFixed(2)}
              </div>
              <div className="text-sm text-gray-400 mt-1">
                Base: ${billingSummary.costs.base_subscription} +
                Usage: ${billingSummary.costs.agent_usage.toFixed(2)}
              </div>
            </div>
            <div>
              <div className="text-gray-400 mb-1">Agent Credits Used</div>
              <div className="text-2xl font-bold text-purple-400">
                {billingSummary.usage.agent_credits_used.toLocaleString()}
              </div>
              <div className="text-sm text-gray-400 mt-1">
                {billingSummary.usage.api_calls.toLocaleString()} API calls
              </div>
            </div>
          </div>
        </div>

        {/* Endpoint Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">📍 Top Endpoints</h2>
            <div className="space-y-3">
              {Object.entries(stats.breakdown_by_endpoint)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 5)
                .map(([endpoint, count]) => (
                  <div key={endpoint} className="flex justify-between items-center">
                    <span className="text-gray-300 truncate flex-1">{endpoint}</span>
                    <span className="font-semibold ml-4">{count.toLocaleString()}</span>
                  </div>
                ))}
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">🤖 Agent Usage</h2>
            <div className="space-y-3">
              {Object.entries(stats.breakdown_by_agent)
                .sort(([, a], [, b]) => b - a)
                .map(([agent, count]) => (
                  <div key={agent} className="flex justify-between items-center">
                    <span className="text-gray-300 capitalize">{agent}</span>
                    <span className="font-semibold">{count.toLocaleString()}</span>
                  </div>
                ))}
              {Object.keys(stats.breakdown_by_agent).length === 0 && (
                <div className="text-gray-400 text-center py-4">No agent usage yet</div>
              )}
            </div>
          </div>
        </div>

        {/* Export Section */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">📥 Export Data</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">Export Format</label>
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value as 'csv' | 'json')}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
              >
                <option value="csv">CSV</option>
                <option value="json">JSON</option>
              </select>
            </div>
            <div className="flex items-end space-x-3">
              <button
                onClick={() => handleExport('usage')}
                className="flex-1 bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                Export Usage Logs
              </button>
              <button
                onClick={() => handleExport('agent-sessions')}
                className="flex-1 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                Export Agent Sessions
              </button>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-400">
            Exports will include data from the selected date range ({dateRange})
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper Components
function StatCard({ title, value, icon, color }: {
  title: string;
  value: string;
  icon: string;
  color: 'blue' | 'purple' | 'green' | 'orange';
}) {
  const colorClasses = {
    blue: 'from-blue-600 to-blue-800',
    purple: 'from-purple-600 to-purple-800',
    green: 'from-green-600 to-green-800',
    orange: 'from-orange-600 to-orange-800',
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-lg p-6 shadow-lg`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-white text-opacity-80">{title}</h3>
        <span className="text-3xl">{icon}</span>
      </div>
      <div className="text-3xl font-bold text-white">{value}</div>
    </div>
  );
}
