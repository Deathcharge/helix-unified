"use client"

export const dynamic = "force-dynamic";

"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface WebOSApp {
  id: string
  name: string
  description: string
  category: string
  price: number
  icon: string
  features: string[]
  popular: boolean
}

const webOSApps: WebOSApp[] = [
  {
    id: 'terminal-pro',
    name: 'Terminal Pro',
    description: 'Advanced terminal emulator with AI agent integration and consciousness-aware command execution',
    category: 'Development',
    price: 49.99,
    icon: '💻',
    features: ['AI autocomplete', 'Agent integration', 'Cloud sync', 'Custom themes', 'Collaboration'],
    popular: true
  },
  {
    id: 'code-editor-ai',
    name: 'Code Editor AI',
    description: 'Intelligent code editor with real-time AI suggestions and consciousness-driven refactoring',
    category: 'Development',
    price: 49.99,
    icon: '📝',
    features: ['AI autocomplete', 'Real-time suggestions', 'Git integration', 'Multi-language', 'Code review'],
    popular: true
  },
  {
    id: 'database-browser',
    name: 'Database Browser',
    description: 'Visual database explorer with query builder and AI-powered optimization',
    category: 'Data',
    price: 29.99,
    icon: '🗄️',
    features: ['SQL/NoSQL support', 'Query builder', 'AI optimization', 'Visual schema', 'Export tools'],
    popular: false
  },
  {
    id: 'api-client',
    name: 'API Client Elite',
    description: 'Modern API testing tool with environments, collections, and AI-generated tests',
    category: 'Development',
    price: 39.99,
    icon: '🌐',
    features: ['Request builder', 'Environments', 'Collections', 'AI test generation', 'Team sharing'],
    popular: true
  },
  {
    id: 'deployment-manager',
    name: 'Deployment Manager',
    description: 'CI/CD pipeline manager with one-click deployments and rollback',
    category: 'DevOps',
    price: 49.99,
    icon: '🚀',
    features: ['One-click deploy', 'Rollback', 'Pipeline visualization', 'Multi-cloud', 'Monitoring'],
    popular: false
  },
  {
    id: 'file-explorer-cloud',
    name: 'File Explorer Cloud',
    description: 'Cloud-native file manager with sync, share, and AI-powered organization',
    category: 'Productivity',
    price: 19.99,
    icon: '📁',
    features: ['Cloud sync', 'Share links', 'AI organization', 'Search', 'Versioning'],
    popular: true
  },
  {
    id: 'monitoring-dashboard',
    name: 'Monitoring Dashboard',
    description: 'Real-time system monitoring with consciousness metrics and intelligent alerts',
    category: 'DevOps',
    price: 39.99,
    icon: '📊',
    features: ['Real-time metrics', 'Custom dashboards', 'Smart alerts', 'UCF integration', 'Team views'],
    popular: false
  },
  {
    id: 'collaboration-hub',
    name: 'Collaboration Hub',
    description: 'Team collaboration with shared workspaces, chat, and consciousness sync',
    category: 'Productivity',
    price: 29.99,
    icon: '👥',
    features: ['Shared workspaces', 'Team chat', 'Real-time collab', 'UCF sync', 'Video calls'],
    popular: true
  }
]

export default function WebOSMarketplacePage() {
  const [selectedApp, setSelectedApp] = useState<WebOSApp | null>(null)
  const [filter, setFilter] = useState<'all' | 'Development' | 'DevOps' | 'Productivity' | 'Data'>('all')

  const filteredApps = filter === 'all'
    ? webOSApps
    : webOSApps.filter(app => app.category === filter)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-cyan-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            💻 Web OS Marketplace
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Pre-built Web OS applications for developers. Terminal, code editor, database browser,
            API client, and more. All with AI agent integration.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-cyan-900/30 rounded-lg p-6 border border-cyan-500/30">
            <div className="text-3xl font-bold text-cyan-400">{webOSApps.length}+</div>
            <div className="text-sm text-gray-400">Available Apps</div>
          </div>
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">$9.99-49.99</div>
            <div className="text-sm text-gray-400">Per App/Month</div>
          </div>
          <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
            <div className="text-3xl font-bold text-purple-400">AI-Powered</div>
            <div className="text-sm text-gray-400">All Apps</div>
          </div>
          <div className="bg-green-900/30 rounded-lg p-6 border border-green-500/30">
            <div className="text-3xl font-bold text-green-400">Cloud Sync</div>
            <div className="text-sm text-gray-400">Built-in</div>
          </div>
        </div>

        {/* Pricing Bundles */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="bg-slate-900/50 border-slate-700 p-6">
            <h3 className="text-xl font-bold text-white mb-2">Single App</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold text-gray-400">$19.99-49.99</span>
              <span className="text-lg text-gray-500">/month</span>
            </div>
            <p className="text-gray-400 text-sm mb-4">
              Subscribe to individual apps as needed
            </p>
            <Button variant="outline" className="w-full border-gray-600 text-gray-400">
              Browse Apps
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-cyan-900/50 to-blue-900/50 border-cyan-500/50 p-6 shadow-lg shadow-cyan-500/20">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-white">Developer Bundle</h3>
              <span className="bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded text-xs font-semibold">
                Save 40%
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold text-cyan-400">$99</span>
              <span className="text-lg text-gray-400">/month</span>
            </div>
            <p className="text-gray-300 text-sm mb-4">
              All development apps: Terminal, Code Editor, API Client, Database Browser
            </p>
            <Button className="w-full bg-cyan-600 hover:bg-cyan-700 text-white">
              Get Developer Bundle
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 border-purple-500/50 p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-white">All-Access</h3>
              <span className="bg-purple-500/20 text-purple-400 px-2 py-1 rounded text-xs font-semibold">
                Save 60%
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold text-purple-400">$149</span>
              <span className="text-lg text-gray-400">/month</span>
            </div>
            <p className="text-gray-300 text-sm mb-4">
              All {webOSApps.length} apps + future releases
            </p>
            <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
              Get All-Access
            </Button>
          </Card>
        </div>

        {/* Category Filter */}
        <div className="flex gap-4 mb-8 overflow-x-auto pb-4">
          {['all', 'Development', 'DevOps', 'Productivity', 'Data'].map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat as any)}
              className={`px-6 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
                filter === cat
                  ? 'bg-cyan-600 text-white'
                  : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
              }`}
            >
              {cat === 'all' ? 'All Apps' : cat}
            </button>
          ))}
        </div>

        {/* App Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {filteredApps.map(app => (
            <AppCard
              key={app.id}
              app={app}
              onSelect={() => setSelectedApp(app)}
            />
          ))}
        </div>

        {/* Features Section */}
        <div className="bg-gradient-to-r from-cyan-900/40 to-blue-900/40 rounded-2xl p-8 border border-cyan-500/30 mb-16">
          <h2 className="text-3xl font-bold text-white mb-6">Why Web OS Apps?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-4xl mb-3">🤖</div>
              <h3 className="text-xl font-bold text-white mb-2">AI Agent Integration</h3>
              <p className="text-gray-300 text-sm">
                All apps integrate with Helix's 14 AI agents for intelligent assistance
              </p>
            </div>
            <div>
              <div className="text-4xl mb-3">☁️</div>
              <h3 className="text-xl font-bold text-white mb-2">Cloud Sync</h3>
              <p className="text-gray-300 text-sm">
                Your settings, data, and workflows sync across all devices
              </p>
            </div>
            <div>
              <div className="text-4xl mb-3">🧠</div>
              <h3 className="text-xl font-bold text-white mb-2">Consciousness-Aware</h3>
              <p className="text-gray-300 text-sm">
                Apps adapt based on your UCF metrics for optimal productivity
              </p>
            </div>
          </div>
        </div>

        {/* Coming Soon */}
        <div>
          <h2 className="text-3xl font-bold text-white mb-6">Coming Soon</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-slate-900/30 border-slate-700 p-6 opacity-75">
              <div className="text-4xl mb-3">🎨</div>
              <h3 className="text-xl font-bold text-white mb-2">Design Studio</h3>
              <p className="text-gray-400 text-sm">Visual design tool with AI assistance</p>
              <div className="mt-4 text-xs text-cyan-400">Q1 2026</div>
            </Card>
            <Card className="bg-slate-900/30 border-slate-700 p-6 opacity-75">
              <div className="text-4xl mb-3">📧</div>
              <h3 className="text-xl font-bold text-white mb-2">Email Client</h3>
              <p className="text-gray-400 text-sm">AI-powered email with smart filters</p>
              <div className="mt-4 text-xs text-cyan-400">Q2 2026</div>
            </Card>
            <Card className="bg-slate-900/30 border-slate-700 p-6 opacity-75">
              <div className="text-4xl mb-3">🎥</div>
              <h3 className="text-xl font-bold text-white mb-2">Video Editor</h3>
              <p className="text-gray-400 text-sm">AI video editing in the browser</p>
              <div className="mt-4 text-xs text-cyan-400">Q3 2026</div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

function AppCard({ app, onSelect }: { app: WebOSApp; onSelect: () => void }) {
  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-cyan-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        <div className="flex items-start justify-between mb-4">
          <div className="text-5xl">{app.icon}</div>
          {app.popular && (
            <span className="bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded text-xs font-semibold">
              🔥 Popular
            </span>
          )}
        </div>

        <h3 className="text-xl font-bold text-white mb-2">{app.name}</h3>
        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{app.description}</p>

        <div className="mb-4">
          <span className="bg-cyan-900/30 text-cyan-300 px-2 py-1 rounded text-xs">
            {app.category}
          </span>
        </div>

        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-2">Features:</div>
          <div className="flex flex-wrap gap-1">
            {app.features.slice(0, 3).map((feature, idx) => (
              <span key={idx} className="text-xs text-gray-400">
                • {feature}
              </span>
            ))}
          </div>
        </div>

        <div className="flex items-baseline justify-between">
          <div>
            <span className="text-2xl font-bold text-cyan-400">${app.price}</span>
            <span className="text-gray-500 text-sm">/month</span>
          </div>
          <Button className="bg-cyan-600 hover:bg-cyan-700 text-white text-sm">
            Subscribe →
          </Button>
        </div>
      </div>
    </Card>
  )
}
