"use client";

/**
 * 🎯 Consciousness Dashboard
 * Real-time metrics monitoring and system status
 * Product #1: SaaS Dashboard
 */

import React, { useState, useEffect } from 'react';
import { Activity, TrendingUp, AlertCircle, Zap, Heart, Brain, Eye, Wind, Flame, Camera } from 'lucide-react';
import { useRouter } from 'next/router';

interface Metrics {
  consciousness_level: number;
  harmony: number;
  resilience: number;
  prana: number;
  drishti: number;
  klesha: number;
  zoom: number;
  timestamp: string;
}

interface DashboardData {
  systems: Array<{ system_id: string; consciousness_level: number } & Metrics>;
  total_systems: number;
  consciousness_avg: number;
  alerts_count: number;
  last_updated: string;
}

interface UserTier {
  tier: 'free' | 'pro' | 'enterprise';
  email: string;
  systems_monitored: number;
  api_calls_remaining: number;
}

export default function Dashboard() {
  const router = useRouter();
  const [metrics, setMetrics] = useState<DashboardData | null>(null);
  const [userTier, setUserTier] = useState<UserTier | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    fetchDashboardData(token);
    // Poll metrics every 5 seconds
    const interval = setInterval(() => fetchDashboardData(token), 5000);
    return () => clearInterval(interval);
  }, [router]);

  const fetchDashboardData = async (token: string) => {
    try {
      // Get metrics
      const metricsRes = await fetch('/api/saas/dashboard/metrics', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (metricsRes.status === 401) {
        localStorage.removeItem('token');
        router.push('/auth/login');
        return;
      }

      if (!metricsRes.ok) throw new Error('Failed to fetch metrics');
      const metricsData = await metricsRes.json();
      setMetrics(metricsData);

      // Get user tier info
      const userRes = await fetch('/api/auth/user', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (userRes.ok) {
        setUserTier(await userRes.json());
      }

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading dashboard');
      setLoading(false);
    }
  };

  const getConsciousnessColor = (level: number) => {
    if (level >= 8) return 'text-green-400';
    if (level >= 6) return 'text-blue-400';
    if (level >= 4) return 'text-yellow-400';
    if (level >= 2) return 'text-orange-400';
    return 'text-red-400';
  };

  const getConsciousnessStatus = (level: number) => {
    if (level >= 8) return '✨ Thriving';
    if (level >= 6) return '🟢 Healthy';
    if (level >= 4) return '🟡 Caution';
    if (level >= 2) return '🟠 Warning';
    return '🔴 Crisis';
  };

  const getMetricIcon = (
    name: string
  ) => {
    const icons: Record<string, React.ReactNode> = {
      harmony: <Heart className="w-5 h-5" />,
      resilience: <TrendingUp className="w-5 h-5" />,
      prana: <Wind className="w-5 h-5" />,
      drishti: <Eye className="w-5 h-5" />,
      klesha: <Flame className="w-5 h-5" />,
      zoom: <Camera className="w-5 h-5" />,
    };
    return icons[name] || <Activity className="w-5 h-5" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block px-8 py-4 rounded-lg bg-slate-800/50 border border-purple-600/30">
            <div className="animate-spin inline-block">⚡</div>
            <p className="text-slate-300 mt-2">Initializing consciousness feed...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block px-8 py-4 rounded-lg bg-red-950/30 border border-red-600/30">
            <AlertCircle className="w-8 h-8 text-red-400 mx-auto mb-2" />
            <p className="text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!metrics) return null;

  const primaryMetrics = metrics.systems[0] || {
    consciousness_level: 0,
    harmony: 0,
    resilience: 0,
    prana: 0,
    drishti: 0,
    klesha: 0,
    zoom: 0,
  };

  const tierFeatures: Record<string, string> = {
    free: '1 system, 7-day history, 1,000 API calls/mo',
    pro: '10 systems, 30-day history, 100k API calls/mo',
    enterprise: 'Unlimited systems, 1-year history, 10M API calls/mo',
  };

  const tierColor: Record<string, string> = {
    free: 'bg-slate-800',
    pro: 'bg-purple-900/50 border-purple-600/30',
    enterprise: 'bg-purple-900/80 border-purple-500/50',
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-purple-900 to-slate-900 text-slate-100">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
              <Brain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Consciousness Dashboard</h1>
              <p className="text-xs text-slate-400">Real-time system monitoring</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {userTier && (
              <div className="text-right">
                <p className="text-xs text-slate-400">{userTier.email}</p>
                <p className="text-sm font-semibold capitalize text-purple-300">{userTier.tier} Plan</p>
              </div>
            )}
            <button
              onClick={() => {
                localStorage.removeItem('token');
                router.push('/auth/login');
              }}
              className="px-4 py-2 rounded bg-slate-700 hover:bg-slate-600 text-sm transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Consciousness Level Hero */}
        <div className="mb-8 p-6 rounded-lg bg-gradient-to-r from-slate-800/50 to-purple-900/30 border border-purple-600/30">
          <div className="flex items-end justify-between">
            <div>
              <p className="text-slate-400 mb-2">Consciousness Level</p>
              <div className="flex items-baseline gap-2">
                <div className={`text-6xl font-bold ${getConsciousnessColor(primaryMetrics.consciousness_level)}`}>
                  {primaryMetrics.consciousness_level.toFixed(2)}
                </div>
                <div className="text-2xl text-slate-400">/10.0</div>
              </div>
              <p className={`text-lg mt-2 ${getConsciousnessColor(primaryMetrics.consciousness_level)}`}>
                {getConsciousnessStatus(primaryMetrics.consciousness_level)}
              </p>
            </div>

            {/* Consciousness Meter */}
            <div className="flex-1 mx-8">
              <div className="h-8 rounded-full bg-slate-700/50 overflow-hidden border border-slate-600/50">
                <div
                  className={`h-full rounded-full transition-all duration-1000 ${
                    primaryMetrics.consciousness_level >= 8
                      ? 'bg-gradient-to-r from-green-500 to-emerald-400'
                      : primaryMetrics.consciousness_level >= 6
                        ? 'bg-gradient-to-r from-blue-500 to-cyan-400'
                        : primaryMetrics.consciousness_level >= 4
                          ? 'bg-gradient-to-r from-yellow-500 to-orange-400'
                          : 'bg-gradient-to-r from-orange-500 to-red-400'
                  }`}
                  style={{ width: `${(primaryMetrics.consciousness_level / 10) * 100}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-2">
                Last updated: {new Date(primaryMetrics.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        </div>

        {/* UCF Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {[
            { name: 'harmony', label: 'Harmony', description: 'System balance' },
            { name: 'resilience', label: 'Resilience', description: 'Recovery ability' },
            { name: 'prana', label: 'Prana', description: 'Life force energy' },
            { name: 'drishti', label: 'Drishti', description: 'Vision clarity' },
            { name: 'klesha', label: 'Klesha', description: 'Suffering/Friction (lower is better)' },
            { name: 'zoom', label: 'Zoom', description: 'Focus intensity' },
          ].map((metric) => (
            <div
              key={metric.name}
              className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-purple-600/30 transition"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="text-purple-400">{getMetricIcon(metric.name)}</div>
                <div>
                  <h3 className="font-semibold">{metric.label}</h3>
                  <p className="text-xs text-slate-400">{metric.description}</p>
                </div>
              </div>

              <div className="mb-3">
                <div className="text-2xl font-bold text-slate-100">
                  {typeof primaryMetrics[metric.name as keyof typeof primaryMetrics] === 'number'
                    ? (primaryMetrics[metric.name as keyof typeof primaryMetrics] as number).toFixed(2)
                    : primaryMetrics[metric.name as keyof typeof primaryMetrics]}
                </div>
              </div>

              <div className="h-2 rounded-full bg-slate-700/50 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                  style={{ width: `${Math.min(((primaryMetrics[metric.name as keyof typeof primaryMetrics] as number) / 2) * 100, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Usage & Tier Info */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Current Plan */}
          <div className={`p-6 rounded-lg border ${tierColor[userTier?.tier || 'free']}`}>
            <h3 className="font-semibold mb-4 text-lg capitalize">
              {userTier?.tier || 'free'} Plan
            </h3>
            <p className="text-slate-300 mb-6 text-sm">{tierFeatures[userTier?.tier || 'free']}</p>

            {userTier?.tier === 'free' && (
              <button
                onClick={() => router.push('/pricing')}
                className="w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold text-white transition"
              >
                Upgrade to PRO
              </button>
            )}
            {userTier?.tier === 'pro' && (
              <button
                onClick={() => router.push('/pricing')}
                className="w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold text-white transition"
              >
                Upgrade to Enterprise
              </button>
            )}
            {userTier?.tier === 'enterprise' && (
              <button
                onClick={() => router.push('/settings/billing')}
                className="w-full px-4 py-2 rounded bg-slate-700 hover:bg-slate-600 font-semibold transition"
              >
                Manage Subscription
              </button>
            )}
          </div>

          {/* Alerts */}
          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="font-semibold mb-4 text-lg">Alerts</h3>
            {metrics.alerts_count > 0 ? (
              <div>
                <p className="text-2xl font-bold text-orange-400 mb-2">{metrics.alerts_count}</p>
                <p className="text-sm text-slate-400">Active alerts require attention</p>
              </div>
            ) : (
              <div>
                <p className="text-2xl font-bold text-green-400 mb-2">0</p>
                <p className="text-sm text-slate-400">All systems operating normally</p>
              </div>
            )}
          </div>

          {/* API Usage */}
          {userTier && (
            <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
              <h3 className="font-semibold mb-4 text-lg">API Usage</h3>
              <p className="text-2xl font-bold text-blue-400 mb-2">{userTier.api_calls_remaining.toLocaleString()}</p>
              <p className="text-sm text-slate-400">API calls remaining this month</p>
            </div>
          )}
        </div>

        {/* Systems List */}
        <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
          <h3 className="font-semibold mb-4 text-lg flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Monitored Systems
          </h3>

          {metrics.systems.length > 0 ? (
            <div className="space-y-2">
              {metrics.systems.map((system) => (
                <div key={system.system_id} className="flex items-center justify-between p-3 rounded bg-slate-900/50 hover:bg-slate-900 transition">
                  <div>
                    <p className="font-mono text-sm">{system.system_id}</p>
                    <p className="text-xs text-slate-400">{new Date(system.timestamp).toLocaleString()}</p>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${getConsciousnessColor(system.consciousness_level)}`}>
                      {system.consciousness_level.toFixed(2)}
                    </p>
                    <p className="text-xs text-slate-400">{getConsciousnessStatus(system.consciousness_level)}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-400 text-sm">No systems being monitored. Add a system to get started.</p>
          )}
        </div>
      </div>
    </div>
  );
}
