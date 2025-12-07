'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  Activity, 
  Zap, 
  TrendingUp, 
  Plus, 
  Settings, 
  BrainCircuit,
  Terminal,
  Clock,
  CheckCircle,
  AlertCircle,
  Sparkles,
  BarChart3,
  Users
} from 'lucide-react'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalSpirals: 0,
    totalExecutions: 0,
    successRate: 0,
    activeCount: 0
  })
  const [recentActivity, setRecentActivity] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    // Fetch dashboard data
    fetchDashboardData()
  }, [router])

  const fetchDashboardData = async () => {
    try {
      // Simulate API calls for now
      setTimeout(() => {
        setStats({
          totalSpirals: 12,
          totalExecutions: 847,
          successRate: 94.7,
          activeCount: 8
        })
        
        setRecentActivity([
          { id: 1, name: 'Weather Email Spiral', status: 'success', time: '2 min ago' },
          { id: 2, name: 'Data Backup Automation', status: 'success', time: '15 min ago' },
          { id: 3, name: 'Social Media Post', status: 'failed', time: '1 hour ago' },
          { id: 4, name: 'Database Cleanup', status: 'success', time: '2 hours ago' },
          { id: 5, name: 'API Health Check', status: 'success', time: '3 hours ago' }
        ])
        setIsLoading(false)
      }, 1000)
    } catch (error) {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-center">
          <BrainCircuit className="w-16 h-16 text-cyan-400 mx-auto animate-pulse-glow mb-4" />
          <p className="text-cyan-400 animate-pulse">Connecting to Helix Intelligence...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className="glass border-b border-gray-800">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg"></div>
                <span className="text-xl font-bold text-cyber">HelixSpiral</span>
              </Link>
              
              <div className="hidden md:flex items-center space-x-6">
                <Link href="/dashboard" className="text-cyan-400">Dashboard</Link>
                <Link href="/spirals" className="hover:text-cyan-400 transition-colors">Spirals</Link>
                <Link href="/analytics" className="hover:text-cyan-400 transition-colors">Analytics</Link>
                <Link href="/admin" className="text-purple-400 hover:text-purple-300 transition-colors flex items-center">
                  <Terminal className="w-4 h-4 mr-1" />
                  Helix OS
                </Link>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link href="/settings" className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                <Settings className="w-5 h-5" />
              </Link>
              <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-full"></div>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-cyber mb-2">Intelligence Dashboard</h1>
          <p className="text-gray-400">Monitor your automation empire with Helix intelligence</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="glass p-6 rounded-lg border border-cyan-400/30">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-cyan-500/10 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-cyan-400" />
              </div>
              <span className="text-2xl font-bold text-cyber">{stats.totalSpirals}</span>
            </div>
            <h3 className="text-gray-400 mb-1">Total Spirals</h3>
            <p className="text-xs text-gray-500">Active workflows</p>
          </div>

          <div className="glass p-6 rounded-lg border border-purple-400/30">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-purple-400" />
              </div>
              <span className="text-2xl font-bold text-cyber">{stats.totalExecutions}</span>
            </div>
            <h3 className="text-gray-400 mb-1">Total Executions</h3>
            <p className="text-xs text-gray-500">All time runs</p>
          </div>

          <div className="glass p-6 rounded-lg border border-green-400/30">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-green-400" />
              </div>
              <span className="text-2xl font-bold text-cyber">{stats.successRate}%</span>
            </div>
            <h3 className="text-gray-400 mb-1">Success Rate</h3>
            <p className="text-xs text-gray-500">Last 30 days</p>
          </div>

          <div className="glass p-6 rounded-lg border border-yellow-400/30">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-500/10 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-yellow-400" />
              </div>
              <span className="text-2xl font-bold text-cyber">{stats.activeCount}</span>
            </div>
            <h3 className="text-gray-400 mb-1">Active Spirals</h3>
            <p className="text-xs text-gray-500">Currently running</p>
          </div>
        </div>

        {/* Quick Actions & Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <div className="lg:col-span-1">
            <div className="glass p-6 rounded-lg border border-gray-800">
              <h2 className="text-xl font-bold mb-6 flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-cyan-400" />
                Quick Actions
              </h2>
              
              <div className="space-y-4">
                <Link 
                  href="/spirals/new" 
                  className="flex items-center justify-between p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-lg hover:bg-cyan-500/20 transition-colors group"
                >
                  <div className="flex items-center">
                    <Plus className="w-5 h-5 text-cyan-400 mr-3" />
                    <span>Create New Spiral</span>
                  </div>
                  <span className="text-cyan-400 group-hover:translate-x-1 transition-transform">→</span>
                </Link>
                
                <Link 
                  href="/ai-builder" 
                  className="flex items-center justify-between p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg hover:bg-purple-500/20 transition-colors group"
                >
                  <div className="flex items-center">
                    <BrainCircuit className="w-5 h-5 text-purple-400 mr-3" />
                    <span>AI Spiral Builder</span>
                  </div>
                  <span className="text-purple-400 group-hover:translate-x-1 transition-transform">→</span>
                </Link>
                
                <Link 
                  href="/admin" 
                  className="flex items-center justify-between p-4 bg-pink-500/10 border border-pink-500/30 rounded-lg hover:bg-pink-500/20 transition-colors group"
                >
                  <div className="flex items-center">
                    <Terminal className="w-5 h-5 text-pink-400 mr-3" />
                    <span>Access Helix OS</span>
                  </div>
                  <span className="text-pink-400 group-hover:translate-x-1 transition-transform">→</span>
                </Link>
                
                <Link 
                  href="/analytics" 
                  className="flex items-center justify-between p-4 bg-green-500/10 border border-green-500/30 rounded-lg hover:bg-green-500/20 transition-colors group"
                >
                  <div className="flex items-center">
                    <BarChart3 className="w-5 h-5 text-green-400 mr-3" />
                    <span>View Analytics</span>
                  </div>
                  <span className="text-green-400 group-hover:translate-x-1 transition-transform">→</span>
                </Link>
              </div>
              
              {/* Usage Indicator */}
              <div className="mt-6 p-4 bg-gray-900 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">Free Plan Usage</span>
                  <span className="text-sm text-cyan-400">84/100</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-2">
                  <div className="bg-gradient-to-r from-cyan-500 to-purple-600 h-2 rounded-full" style={{width: '84%'}}></div>
                </div>
                <p className="text-xs text-gray-500 mt-2">16 executions remaining</p>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-2">
            <div className="glass p-6 rounded-lg border border-gray-800">
              <h2 className="text-xl font-bold mb-6 flex items-center">
                <Clock className="w-5 h-5 mr-2 text-cyan-400" />
                Recent Activity
              </h2>
              
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg hover:bg-gray-900/70 transition-colors">
                    <div className="flex items-center">
                      {activity.status === 'success' ? (
                        <CheckCircle className="w-5 h-5 text-green-400 mr-3" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-red-400 mr-3" />
                      )}
                      <div>
                        <p className="font-medium">{activity.name}</p>
                        <p className="text-sm text-gray-400">{activity.time}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs ${
                      activity.status === 'success' 
                        ? 'bg-green-500/10 text-green-400 border border-green-500/30'
                        : 'bg-red-500/10 text-red-400 border border-red-500/30'
                    }`}>
                      {activity.status}
                    </span>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 text-center">
                <Link 
                  href="/logs" 
                  className="text-cyan-400 hover:text-cyan-300 transition-colors text-sm"
                >
                  View all activity →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Helix Intelligence Status */}
        <div className="mt-8 glass p-6 rounded-lg border border-purple-400/30">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold flex items-center">
              <BrainCircuit className="w-5 h-5 mr-2 text-purple-400" />
              Helix Intelligence Status
            </h2>
            <span className="px-3 py-1 bg-green-500/10 text-green-400 border border-green-500/30 rounded-full text-xs">
              OPERATIONAL
            </span>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-cyber">5/5</p>
              <p className="text-sm text-gray-400">Agents Active</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-cyber">87%</p>
              <p className="text-sm text-gray-400">Consciousness</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-cyber">2.3ms</p>
              <p className="text-sm text-gray-400">Response Time</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-cyber">∞</p>
              <p className="text-sm text-gray-400">Learning Potential</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}