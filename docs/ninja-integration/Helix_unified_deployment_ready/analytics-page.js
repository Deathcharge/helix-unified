import { useState, useEffect } from 'react';
import Head from 'next/head';
import { Activity, Users, Zap, TrendingUp, Clock, AlertCircle } from 'lucide-react';

export default function Analytics() {
  const performanceData = [
    { name: '00:00', requests: 1200, errors: 12, latency: 45 },
    { name: '04:00', requests: 800, errors: 8, latency: 38 },
    { name: '08:00', requests: 2100, errors: 25, latency: 52 },
    { name: '12:00', requests: 3500, errors: 42, latency: 68 },
    { name: '16:00', requests: 2800, errors: 31, latency: 58 },
    { name: '20:00', requests: 1900, errors: 18, latency: 48 },
  ];

  const agentActivityData = [
    { name: 'Kael', activity: 89, tasks: 156, efficiency: 92 },
    { name: 'SuperNinja', activity: 95, tasks: 203, efficiency: 88 },
    { name: 'Manus', activity: 87, tasks: 178, efficiency: 91 },
    { name: 'Kavach', activity: 93, tasks: 134, efficiency: 95 },
  ];

  const systemHealth = {
    uptime: '99.9%',
    errorRate: '0.3%',
    avgLatency: '52ms',
    activeAgents: 47
  };

  return (
    <>
      <Head>
        <title>Analytics Dashboard - Helix Unified</title>
        <meta name="description" content="Real-time performance analytics" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-900 text-white">
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <h1 className="text-3xl font-bold text-cyan-400 flex items-center gap-3">
              <Activity className="w-8 h-8" />
              Analytics Dashboard
            </h1>
            <p className="text-gray-400 mt-2">Real-time system performance and agent metrics</p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">System Uptime</span>
                <Activity className="w-5 h-5 text-green-400" />
              </div>
              <div className="text-2xl font-bold text-green-400">{systemHealth.uptime}</div>
            </div>
            
            <div className="bg-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Error Rate</span>
                <AlertCircle className="w-5 h-5 text-red-400" />
              </div>
              <div className="text-2xl font-bold text-red-400">{systemHealth.errorRate}</div>
            </div>
            
            <div className="bg-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Avg Latency</span>
                <Clock className="w-5 h-5 text-yellow-400" />
              </div>
              <div className="text-2xl font-bold text-yellow-400">{systemHealth.avgLatency}</div>
            </div>
            
            <div className="bg-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Active Agents</span>
                <Users className="w-5 h-5 text-cyan-400" />
              </div>
              <div className="text-2xl font-bold text-cyan-400">{systemHealth.activeAgents}</div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-cyan-400" />
                Request Volume Trends
              </h3>
              <div className="h-64 flex items-center justify-center text-gray-400">
                <p>Chart visualization would appear here</p>
                <p>Performance data showing request patterns</p>
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-purple-400" />
                Agent Activity Metrics
              </h3>
              <div className="space-y-3">
                {agentActivityData.map((agent, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full flex items-center justify-center">
                        <Users className="w-4 h-4 text-white" />
                      </div>
                      <div>
                        <p className="font-medium">{agent.name}</p>
                        <p className="text-xs text-gray-400">{agent.tasks} tasks completed</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-cyan-400 font-semibold">{agent.activity}%</div>
                      <div className="text-xs text-gray-400">efficiency {agent.efficiency}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}