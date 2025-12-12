/**
 * 📊 Comprehensive Metrics Dashboard
 * Track all key business metrics in one powerful dashboard
 *
 * VILLAIN METRICS: MEASURING WORLD DOMINATION 😈
 */

import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';

// ============================================================================
// TYPES
// ============================================================================

interface MetricsSummary {
  total_users: number;
  new_signups: number;
  active_users_daily: number;
  active_users_monthly: number;
  activation_rate: number;
  mrr: number;
  arr: number;
  churn_rate: number;
  total_api_calls: number;
  total_agent_sessions: number;
  error_rate: number;
  api_uptime: number;
  open_tickets: number;
  avg_resolution_time_hours: number;
  nps_score: number;
  nps_responses: number;
  top_features: Array<{
    feature: string;
    usage_count: number;
    avg_response_time_ms: number;
  }>;
  date_range: {
    start: string;
    end: string;
    days: number;
  };
}

interface DailyMetrics {
  dates: string[];
  signups: number[];
  dau: number[];
  mau: number[];
  mrr: number[];
  error_rate: number[];
  api_calls: number[];
}

interface RevenueBreakdown {
  free_users: number;
  pro_users: number;
  workflow_users: number;
  enterprise_users: number;
  total_mrr: number;
  avg_revenue_per_user: number;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function MetricsDashboard() {
  const [summary, setSummary] = useState<MetricsSummary | null>(null);
  const [dailyMetrics, setDailyMetrics] = useState<DailyMetrics | null>(null);
  const [revenueBreakdown, setRevenueBreakdown] = useState<RevenueBreakdown | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<7 | 30 | 90>(30);

  useEffect(() => {
    fetchAllMetrics();
  }, [timeRange]);

  const fetchAllMetrics = async () => {
    setLoading(true);
    try {
      // Fetch summary
      const summaryRes = await fetch(`/api/metrics/summary?days=${timeRange}`);
      const summaryData = await summaryRes.json();
      setSummary(summaryData);

      // Fetch daily metrics
      const dailyRes = await fetch(`/api/metrics/daily?days=${timeRange}`);
      const dailyData = await dailyRes.json();
      setDailyMetrics(dailyData);

      // Fetch revenue breakdown
      const revenueRes = await fetch('/api/metrics/revenue-breakdown');
      const revenueData = await revenueRes.json();
      setRevenueBreakdown(revenueData);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-950">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading metrics...</p>
        </div>
      </div>
    );
  }

  if (!summary || !dailyMetrics || !revenueBreakdown) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">📊 No Data Available</h2>
          <p className="text-gray-400">Metrics data could not be loaded</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const growthChartData = dailyMetrics.dates.map((date, i) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    signups: dailyMetrics.signups[i],
    dau: dailyMetrics.dau[i],
    mau: dailyMetrics.mau[i]
  }));

  const revenueChartData = dailyMetrics.dates.map((date, i) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    mrr: dailyMetrics.mrr[i]
  }));

  const usageChartData = dailyMetrics.dates.map((date, i) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    api_calls: dailyMetrics.api_calls[i],
    error_rate: dailyMetrics.error_rate[i]
  }));

  const tierDistributionData = [
    { name: 'Free', value: revenueBreakdown.free_users, color: '#6b7280' },
    { name: 'Pro', value: revenueBreakdown.pro_users, color: '#8b5cf6' },
    { name: 'Workflow', value: revenueBreakdown.workflow_users, color: '#3b82f6' },
    { name: 'Enterprise', value: revenueBreakdown.enterprise_users, color: '#10b981' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-purple-950 to-gray-900 text-white p-6">
      <div className="max-w-[1800px] mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              📊 Metrics Dashboard
            </h1>
            <p className="text-gray-400">
              Comprehensive business intelligence and analytics
            </p>
          </div>

          {/* Time Range Selector */}
          <div className="flex gap-2">
            {([7, 30, 90] as const).map((days) => (
              <button
                key={days}
                onClick={() => setTimeRange(days)}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  timeRange === days
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {days}d
              </button>
            ))}
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4 mb-8">
          <MetricCard
            title="Total Users"
            value={summary.total_users.toLocaleString()}
            icon="👥"
            color="purple"
            subtitle={`${summary.new_signups} new this period`}
          />
          <MetricCard
            title="DAU"
            value={summary.active_users_daily.toLocaleString()}
            icon="📈"
            color="blue"
            subtitle="Daily Active Users"
          />
          <MetricCard
            title="MRR"
            value={`$${summary.mrr.toLocaleString()}`}
            icon="💰"
            color="green"
            subtitle="Monthly Recurring Revenue"
          />
          <MetricCard
            title="Churn Rate"
            value={`${summary.churn_rate}%`}
            icon="📉"
            color={summary.churn_rate > 5 ? "red" : "green"}
            subtitle="Customer churn"
          />
          <MetricCard
            title="NPS Score"
            value={summary.nps_score.toFixed(0)}
            icon="⭐"
            color={summary.nps_score > 50 ? "green" : summary.nps_score > 0 ? "yellow" : "red"}
            subtitle={`${summary.nps_responses} responses`}
          />
          <MetricCard
            title="API Uptime"
            value={`${summary.api_uptime}%`}
            icon="🟢"
            color={summary.api_uptime > 99 ? "green" : "yellow"}
            subtitle="Service availability"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* User Growth Chart */}
          <ChartCard title="📈 User Growth" description="Signups and active users over time">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={growthChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Legend />
                <Line type="monotone" dataKey="signups" stroke="#8b5cf6" strokeWidth={2} name="Signups" />
                <Line type="monotone" dataKey="dau" stroke="#3b82f6" strokeWidth={2} name="DAU" />
                <Line type="monotone" dataKey="mau" stroke="#10b981" strokeWidth={2} name="MAU" />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Revenue Growth */}
          <ChartCard title="💰 Revenue Growth" description="MRR trends over time">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={revenueChartData}>
                <defs>
                  <linearGradient id="mrrGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                  formatter={(value: number) => [`$${value.toLocaleString()}`, 'MRR']}
                />
                <Area type="monotone" dataKey="mrr" stroke="#10b981" fillOpacity={1} fill="url(#mrrGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* User Tier Distribution */}
          <ChartCard title="🎯 User Distribution" description="Users by subscription tier">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={tierDistributionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {tierDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* API Usage & Errors */}
          <ChartCard title="🚀 API Usage & Errors" description="API calls and error rates">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={usageChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis yAxisId="left" stroke="#9ca3af" />
                <YAxis yAxisId="right" orientation="right" stroke="#ef4444" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Legend />
                <Area
                  yAxisId="left"
                  type="monotone"
                  dataKey="api_calls"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.6}
                  name="API Calls"
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="error_rate"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Error Rate %"
                />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Bottom Row - Stats & Features */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Activation & Revenue Stats */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <h3 className="text-xl font-bold mb-4">🎯 Key Stats</h3>
            <div className="space-y-4">
              <StatRow label="Activation Rate" value={`${summary.activation_rate}%`} />
              <StatRow label="ARR" value={`$${summary.arr.toLocaleString()}`} />
              <StatRow label="ARPU" value={`$${revenueBreakdown.avg_revenue_per_user.toFixed(2)}`} />
              <StatRow label="API Calls" value={summary.total_api_calls.toLocaleString()} />
              <StatRow label="Agent Sessions" value={summary.total_agent_sessions.toLocaleString()} />
              <StatRow label="Error Rate" value={`${summary.error_rate}%`} />
            </div>
          </div>

          {/* Top Features */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 lg:col-span-2">
            <h3 className="text-xl font-bold mb-4">🔥 Top Features</h3>
            <div className="space-y-2">
              {summary.top_features.slice(0, 8).map((feature, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b border-gray-800">
                  <div className="flex-1">
                    <span className="text-gray-300 font-mono text-sm">{feature.feature}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-purple-400 font-semibold">
                      {feature.usage_count.toLocaleString()}
                    </span>
                    <span className="text-gray-500 text-sm">
                      {feature.avg_response_time_ms.toFixed(0)}ms
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Support Stats */}
        <div className="mt-6 bg-gray-900 rounded-xl p-6 border border-gray-800">
          <h3 className="text-xl font-bold mb-4">🎫 Support Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-gray-400 mb-1">Open Tickets</div>
              <div className="text-3xl font-bold text-orange-400">{summary.open_tickets}</div>
            </div>
            <div>
              <div className="text-gray-400 mb-1">Avg Resolution Time</div>
              <div className="text-3xl font-bold text-blue-400">
                {summary.avg_resolution_time_hours.toFixed(1)}h
              </div>
            </div>
            <div>
              <div className="text-gray-400 mb-1">Customer Satisfaction</div>
              <div className="text-3xl font-bold text-green-400">
                {summary.nps_score > 0 ? '+' : ''}{summary.nps_score.toFixed(0)} NPS
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// HELPER COMPONENTS
// ============================================================================

function MetricCard({ title, value, icon, color, subtitle }: {
  title: string;
  value: string;
  icon: string;
  color: string;
  subtitle?: string;
}) {
  const colorClasses = {
    purple: 'from-purple-600 to-purple-800',
    blue: 'from-blue-600 to-blue-800',
    green: 'from-green-600 to-green-800',
    red: 'from-red-600 to-red-800',
    yellow: 'from-yellow-600 to-yellow-800',
    orange: 'from-orange-600 to-orange-800',
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} rounded-xl p-4 shadow-lg`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-white text-opacity-90 text-sm font-medium">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="text-2xl font-bold text-white mb-1">{value}</div>
      {subtitle && <div className="text-xs text-white text-opacity-70">{subtitle}</div>}
    </div>
  );
}

function ChartCard({ title, description, children }: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
      <div className="mb-4">
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="text-sm text-gray-400">{description}</p>
      </div>
      {children}
    </div>
  );
}

function StatRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-gray-800">
      <span className="text-gray-400">{label}</span>
      <span className="font-semibold text-white">{value}</span>
    </div>
  );
}
