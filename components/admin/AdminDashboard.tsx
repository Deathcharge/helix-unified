/**
 * 👑 Admin Dashboard
 * Manage users, teams, subscriptions, and platform settings
 *
 * VILLAIN CONTROL CENTER: RULE YOUR EMPIRE 😈
 */

import React, { useState, useEffect } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
  subscription_tier: string;
  subscription_status: string;
  created_at: string;
  last_login: string;
  api_calls_count: number;
}

interface Team {
  id: string;
  name: string;
  slug: string;
  owner_id: string;
  subscription_tier: string;
  member_count: number;
  created_at: string;
}

interface PlatformStats {
  total_users: number;
  total_teams: number;
  total_api_calls: number;
  total_revenue_mrr: number;
  active_subscriptions: number;
  new_users_today: number;
  tier_distribution: {
    free: number;
    pro: number;
    workflow: number;
    enterprise: number;
  };
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'teams' | 'billing'>('overview');

  useEffect(() => {
    fetchAdminData();
  }, [activeTab]);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      // Fetch platform stats
      const statsRes = await fetch('/api/admin/stats');
      const statsData = await statsRes.json();
      setStats(statsData);

      // Fetch users or teams based on active tab
      if (activeTab === 'users') {
        const usersRes = await fetch('/api/admin/users');
        const usersData = await usersRes.json();
        setUsers(usersData);
      } else if (activeTab === 'teams') {
        const teamsRes = await fetch('/api/admin/teams');
        const teamsData = await teamsRes.json();
        setTeams(teamsData);
      }
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateUserTier = async (userId: string, newTier: string) => {
    try {
      await fetch(`/api/admin/users/${userId}/tier`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tier: newTier })
      });
      fetchAdminData();
    } catch (error) {
      console.error('Failed to update user tier:', error);
    }
  };

  const handleSuspendUser = async (userId: string) => {
    if (!confirm('Are you sure you want to suspend this user?')) return;

    try {
      await fetch(`/api/admin/users/${userId}/suspend`, {
        method: 'POST'
      });
      fetchAdminData();
    } catch (error) {
      console.error('Failed to suspend user:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">👑 Admin Dashboard</h1>
          <p className="text-gray-400">Platform management and analytics</p>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-8 border-b border-gray-700">
          {['overview', 'users', 'teams', 'billing'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === tab
                  ? 'border-b-2 border-purple-500 text-purple-400'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && stats && (
          <div>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatCard
                title="Total Users"
                value={stats.total_users.toLocaleString()}
                change={`+${stats.new_users_today} today`}
                icon="👥"
              />
              <StatCard
                title="Total Teams"
                value={stats.total_teams.toLocaleString()}
                icon="🏢"
              />
              <StatCard
                title="Active Subscriptions"
                value={stats.active_subscriptions.toLocaleString()}
                icon="💳"
              />
              <StatCard
                title="MRR"
                value={`$${stats.total_revenue_mrr.toLocaleString()}`}
                icon="💰"
              />
            </div>

            {/* Tier Distribution */}
            <div className="bg-gray-800 rounded-lg p-6 mb-8">
              <h2 className="text-2xl font-bold mb-4">📊 Subscription Tiers</h2>
              <div className="grid grid-cols-4 gap-4">
                {Object.entries(stats.tier_distribution).map(([tier, count]) => (
                  <div key={tier} className="text-center">
                    <div className="text-3xl font-bold text-purple-400">{count}</div>
                    <div className="text-gray-400 capitalize">{tier}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">📈 Platform Metrics</h2>
              <div className="space-y-4">
                <MetricRow
                  label="Total API Calls"
                  value={stats.total_api_calls.toLocaleString()}
                />
                <MetricRow
                  label="Average per User"
                  value={Math.round(stats.total_api_calls / stats.total_users).toLocaleString()}
                />
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">👥 User Management</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4">Email</th>
                    <th className="text-left py-3 px-4">Name</th>
                    <th className="text-left py-3 px-4">Tier</th>
                    <th className="text-left py-3 px-4">Status</th>
                    <th className="text-left py-3 px-4">API Calls</th>
                    <th className="text-left py-3 px-4">Last Login</th>
                    <th className="text-left py-3 px-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b border-gray-700 hover:bg-gray-700">
                      <td className="py-3 px-4">{user.email}</td>
                      <td className="py-3 px-4">{user.name}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          user.subscription_tier === 'enterprise' ? 'bg-purple-600' :
                          user.subscription_tier === 'pro' ? 'bg-blue-600' :
                          'bg-gray-600'
                        }`}>
                          {user.subscription_tier}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          user.subscription_status === 'active' ? 'bg-green-600' : 'bg-red-600'
                        }`}>
                          {user.subscription_status}
                        </span>
                      </td>
                      <td className="py-3 px-4">{user.api_calls_count.toLocaleString()}</td>
                      <td className="py-3 px-4">
                        {new Date(user.last_login).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex space-x-2">
                          <select
                            onChange={(e) => handleUpdateUserTier(user.id, e.target.value)}
                            defaultValue={user.subscription_tier}
                            className="bg-gray-700 text-white px-2 py-1 rounded text-sm"
                          >
                            <option value="free">Free</option>
                            <option value="pro">Pro</option>
                            <option value="workflow">Workflow</option>
                            <option value="enterprise">Enterprise</option>
                          </select>
                          <button
                            onClick={() => handleSuspendUser(user.id)}
                            className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
                          >
                            Suspend
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Teams Tab */}
        {activeTab === 'teams' && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">🏢 Team Management</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4">Name</th>
                    <th className="text-left py-3 px-4">Slug</th>
                    <th className="text-left py-3 px-4">Tier</th>
                    <th className="text-left py-3 px-4">Members</th>
                    <th className="text-left py-3 px-4">Created</th>
                    <th className="text-left py-3 px-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {teams.map((team) => (
                    <tr key={team.id} className="border-b border-gray-700 hover:bg-gray-700">
                      <td className="py-3 px-4">{team.name}</td>
                      <td className="py-3 px-4">{team.slug}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          team.subscription_tier === 'enterprise' ? 'bg-purple-600' :
                          team.subscription_tier === 'pro' ? 'bg-blue-600' :
                          'bg-gray-600'
                        }`}>
                          {team.subscription_tier}
                        </span>
                      </td>
                      <td className="py-3 px-4">{team.member_count}</td>
                      <td className="py-3 px-4">
                        {new Date(team.created_at).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4">
                        <button className="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-sm">
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Billing Tab */}
        {activeTab === 'billing' && stats && (
          <div>
            <div className="bg-gray-800 rounded-lg p-6 mb-8">
              <h2 className="text-2xl font-bold mb-4">💰 Revenue Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-400">
                    ${stats.total_revenue_mrr.toLocaleString()}
                  </div>
                  <div className="text-gray-400 mt-2">Monthly Recurring Revenue</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-400">
                    ${(stats.total_revenue_mrr * 12).toLocaleString()}
                  </div>
                  <div className="text-gray-400 mt-2">Annual Run Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-purple-400">
                    ${Math.round(stats.total_revenue_mrr / stats.active_subscriptions).toLocaleString()}
                  </div>
                  <div className="text-gray-400 mt-2">Average Revenue Per User</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Helper Components
function StatCard({ title, value, change, icon }: {
  title: string;
  value: string;
  change?: string;
  icon: string;
}) {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-400">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="text-3xl font-bold">{value}</div>
      {change && <div className="text-sm text-green-400 mt-1">{change}</div>}
    </div>
  );
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-gray-400">{label}</span>
      <span className="font-semibold">{value}</span>
    </div>
  );
}
