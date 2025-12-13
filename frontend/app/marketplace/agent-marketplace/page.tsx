"use client"

export const dynamic = "force-dynamic";

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface AgentListing {
  id: string
  name: string
  creator: string
  description: string
  category: string
  price: number
  priceModel: 'subscription' | 'pay-per-use' | 'one-time'
  rating: number
  reviews: number
  downloads: number
  featured: boolean
  capabilities: string[]
  tags: string[]
}

const featuredAgents: AgentListing[] = [
  {
    id: 'customer-support-pro',
    name: 'Customer Support Pro',
    creator: 'Helix Official',
    description: 'AI customer support agent with multi-channel support, ticket management, and CRM integration',
    category: 'Customer Service',
    price: 299,
    priceModel: 'subscription',
    rating: 4.9,
    reviews: 247,
    downloads: 1853,
    featured: true,
    capabilities: ['Email support', 'Live chat', 'Ticket management', 'CRM integration', 'Analytics'],
    tags: ['customer-service', 'support', 'crm', 'automation']
  },
  {
    id: 'sales-assistant',
    name: 'Sales Assistant Elite',
    creator: 'Revenue Boost Inc',
    description: 'AI sales representative with lead qualification, pipeline management, and proposal generation',
    category: 'Sales',
    price: 499,
    priceModel: 'subscription',
    rating: 4.8,
    reviews: 189,
    downloads: 943,
    featured: true,
    capabilities: ['Lead qualification', 'Pipeline management', 'Proposal generation', 'Contract mgmt'],
    tags: ['sales', 'revenue', 'crm', 'automation']
  },
  {
    id: 'code-reviewer',
    name: 'Code Review Master',
    creator: 'DevTools Co',
    description: 'AI code reviewer with security scanning, best practices enforcement, and automated suggestions',
    category: 'Development',
    price: 149,
    priceModel: 'subscription',
    rating: 4.7,
    reviews: 412,
    downloads: 2891,
    featured: true,
    capabilities: ['Code review', 'Security scanning', 'Best practices', 'Auto-fix suggestions'],
    tags: ['development', 'code-quality', 'security', 'automation']
  },
  {
    id: 'content-creator',
    name: 'Content Creation Suite',
    creator: 'Marketing Minds',
    description: 'AI content creator for blogs, social media, videos, and email campaigns',
    category: 'Marketing',
    price: 199,
    priceModel: 'subscription',
    rating: 4.6,
    reviews: 328,
    downloads: 1472,
    featured: true,
    capabilities: ['Blog posts', 'Social media', 'Email campaigns', 'SEO optimization'],
    tags: ['marketing', 'content', 'seo', 'automation']
  },
  {
    id: 'research-analyst',
    name: 'Research Analyst Pro',
    creator: 'Data Insights LLC',
    description: 'AI research analyst for market research, competitive analysis, and trend forecasting',
    category: 'Analytics',
    price: 0.05,
    priceModel: 'pay-per-use',
    rating: 4.9,
    reviews: 156,
    downloads: 687,
    featured: false,
    capabilities: ['Market research', 'Competitive analysis', 'Trend forecasting', 'Report generation'],
    tags: ['analytics', 'research', 'market-intelligence']
  },
  {
    id: 'hr-assistant',
    name: 'HR Assistant Plus',
    creator: 'People Ops Pro',
    description: 'AI HR assistant for recruitment, onboarding, performance reviews, and employee engagement',
    category: 'Human Resources',
    price: 249,
    priceModel: 'subscription',
    rating: 4.5,
    reviews: 203,
    downloads: 891,
    featured: false,
    capabilities: ['Recruitment', 'Onboarding', 'Performance reviews', 'Engagement tracking'],
    tags: ['hr', 'recruitment', 'people-ops']
  }
]

const categories = [
  'All Categories',
  'Customer Service',
  'Sales',
  'Development',
  'Marketing',
  'Analytics',
  'Human Resources',
  'Finance',
  'Operations'
]

export default function AgentMarketplacePage() {
  const [selectedCategory, setSelectedCategory] = useState('All Categories')
  const [selectedAgent, setSelectedAgent] = useState<AgentListing | null>(null)
  const [view, setView] = useState<'browse' | 'create'>('browse')

  const filteredAgents = selectedCategory === 'All Categories'
    ? featuredAgents
    : featuredAgents.filter(a => a.category === selectedCategory)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                🏪 AI Agent Marketplace
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl">
                Discover, create, and sell custom AI agents. Like GPT Store but for Helix.
                Creators earn 70% revenue share.
              </p>
            </div>
            <div className="hidden md:flex gap-4">
              <Button
                onClick={() => setView('browse')}
                className={view === 'browse' ? 'bg-purple-600' : 'bg-slate-700'}
              >
                Browse Agents
              </Button>
              <Button
                onClick={() => setView('create')}
                className={view === 'create' ? 'bg-purple-600' : 'bg-slate-700'}
              >
                Create Agent →
              </Button>
            </div>
          </div>
        </div>

        {view === 'browse' ? (
          <>
            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
              <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
                <div className="text-3xl font-bold text-purple-400">{featuredAgents.length}+</div>
                <div className="text-sm text-gray-400">Available Agents</div>
              </div>
              <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
                <div className="text-3xl font-bold text-blue-400">1,247</div>
                <div className="text-sm text-gray-400">Creators Earning</div>
              </div>
              <div className="bg-green-900/30 rounded-lg p-6 border border-green-500/30">
                <div className="text-3xl font-bold text-green-400">$1.2M+</div>
                <div className="text-sm text-gray-400">Paid to Creators</div>
              </div>
              <div className="bg-pink-900/30 rounded-lg p-6 border border-pink-500/30">
                <div className="text-3xl font-bold text-pink-400">70%</div>
                <div className="text-sm text-gray-400">Revenue Share</div>
              </div>
            </div>

            {/* Category Filter */}
            <div className="mb-8">
              <div className="flex gap-2 overflow-x-auto pb-4">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
                      selectedCategory === cat
                        ? 'bg-purple-600 text-white'
                        : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* Agent Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
              {filteredAgents.map(agent => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onSelect={() => setSelectedAgent(agent)}
                />
              ))}
            </div>

            {/* Creator Call to Action */}
            <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-2xl p-8 border border-purple-500/30">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                <div>
                  <h3 className="text-3xl font-bold text-white mb-4">
                    🚀 Become a Creator
                  </h3>
                  <p className="text-gray-300 mb-6">
                    Build custom AI agents with our no-code builder. Earn 70% revenue
                    share on every sale. Join 1,247 creators already earning.
                  </p>
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <div className="text-2xl font-bold text-purple-400">70%</div>
                      <div className="text-sm text-gray-400">Revenue Share</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-400">$8,400</div>
                      <div className="text-sm text-gray-400">Avg Creator/Month</div>
                    </div>
                  </div>
                  <Button
                    onClick={() => setView('create')}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
                  >
                    Start Creating →
                  </Button>
                </div>
                <div className="bg-slate-900/50 rounded-xl p-6 border border-purple-500/30">
                  <h4 className="text-lg font-bold text-white mb-4">Top Creators</h4>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white font-semibold">DevTools Co</div>
                        <div className="text-xs text-gray-400">12 agents published</div>
                      </div>
                      <div className="text-green-400 font-bold">$24k/mo</div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white font-semibold">Revenue Boost Inc</div>
                        <div className="text-xs text-gray-400">8 agents published</div>
                      </div>
                      <div className="text-green-400 font-bold">$18k/mo</div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-white font-semibold">Marketing Minds</div>
                        <div className="text-xs text-gray-400">15 agents published</div>
                      </div>
                      <div className="text-green-400 font-bold">$15k/mo</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <AgentBuilder onBack={() => setView('browse')} />
        )}
      </div>

      {/* Agent Detail Modal */}
      {selectedAgent && (
        <AgentDetailModal
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
        />
      )}
    </div>
  )
}

function AgentCard({ agent, onSelect }: { agent: AgentListing; onSelect: () => void }) {
  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-purple-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-1">{agent.name}</h3>
            <div className="text-sm text-gray-400">{agent.creator}</div>
          </div>
          {agent.featured && (
            <span className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded text-xs font-semibold">
              ⭐ Featured
            </span>
          )}
        </div>

        {/* Description */}
        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{agent.description}</p>

        {/* Category */}
        <div className="mb-4">
          <span className="bg-purple-900/30 text-purple-300 px-2 py-1 rounded text-xs">
            {agent.category}
          </span>
        </div>

        {/* Rating & Downloads */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="flex items-center">
              <span className="text-yellow-400">★</span>
              <span className="text-white font-semibold ml-1">{agent.rating}</span>
              <span className="text-gray-500 text-sm ml-1">({agent.reviews})</span>
            </div>
          </div>
          <div className="text-sm text-gray-400">
            {agent.downloads.toLocaleString()} downloads
          </div>
        </div>

        {/* Capabilities */}
        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-2">Key Capabilities:</div>
          <div className="flex flex-wrap gap-1">
            {agent.capabilities.slice(0, 3).map((cap, idx) => (
              <span key={idx} className="bg-slate-800 text-gray-300 px-2 py-1 rounded text-xs">
                {cap}
              </span>
            ))}
          </div>
        </div>

        {/* Price */}
        <div className="flex items-baseline justify-between">
          <div>
            {agent.priceModel === 'subscription' && (
              <>
                <span className="text-2xl font-bold text-purple-400">${agent.price}</span>
                <span className="text-gray-500 text-sm">/month</span>
              </>
            )}
            {agent.priceModel === 'pay-per-use' && (
              <>
                <span className="text-2xl font-bold text-purple-400">${agent.price}</span>
                <span className="text-gray-500 text-sm">/use</span>
              </>
            )}
            {agent.priceModel === 'one-time' && (
              <span className="text-2xl font-bold text-purple-400">${agent.price}</span>
            )}
          </div>
          <Button className="bg-purple-600 hover:bg-purple-700 text-white text-sm">
            View Details →
          </Button>
        </div>
      </div>
    </Card>
  )
}

function AgentDetailModal({ agent, onClose }: { agent: AgentListing; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-slate-900 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-purple-500/30" onClick={e => e.stopPropagation()}>
        <div className="p-8">
          {/* Header */}
          <div className="flex items-start justify-between mb-6">
            <div>
              <h2 className="text-4xl font-bold text-white mb-2">{agent.name}</h2>
              <div className="text-gray-400">by {agent.creator}</div>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">
              ×
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-slate-800/50 rounded-lg p-4">
              <div className="flex items-center text-yellow-400 mb-2">
                <span>★</span>
                <span className="text-white font-bold ml-1">{agent.rating}</span>
              </div>
              <div className="text-xs text-gray-400">{agent.reviews} reviews</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-purple-400">{agent.downloads.toLocaleString()}</div>
              <div className="text-xs text-gray-400">Downloads</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-green-400">${agent.price}</div>
              <div className="text-xs text-gray-400">/month</div>
            </div>
          </div>

          {/* Description */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Description</h3>
            <p className="text-gray-300">{agent.description}</p>
          </div>

          {/* Capabilities */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Capabilities</h3>
            <ul className="grid grid-cols-2 gap-3">
              {agent.capabilities.map((cap, idx) => (
                <li key={idx} className="flex items-center text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  {cap}
                </li>
              ))}
            </ul>
          </div>

          {/* Tags */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {agent.tags.map((tag, idx) => (
                <span key={idx} className="bg-purple-900/30 text-purple-300 px-3 py-1 rounded-full text-sm">
                  #{tag}
                </span>
              ))}
            </div>
          </div>

          {/* CTAs */}
          <div className="flex gap-4">
            <Button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-4 text-lg">
              Install Agent →
            </Button>
            <Button variant="outline" className="border-purple-500 text-purple-400 hover:bg-purple-900/30 px-8 py-4">
              Try Demo
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

function AgentBuilder({ onBack }: { onBack: () => void }) {
  return (
    <div className="bg-slate-900/50 rounded-2xl p-8 border border-purple-500/30">
      <div className="mb-8">
        <button onClick={onBack} className="text-purple-400 hover:text-purple-300 mb-4">
          ← Back to Browse
        </button>
        <h2 className="text-4xl font-bold text-white mb-4">🔨 Agent Builder</h2>
        <p className="text-gray-300">
          Create custom AI agents with our no-code builder. No programming required!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="bg-slate-800/50 border-slate-700 p-6">
          <div className="text-4xl mb-4">1️⃣</div>
          <h3 className="text-xl font-bold text-white mb-2">Define Agent</h3>
          <p className="text-gray-400 text-sm">
            Name, description, personality, and capabilities
          </p>
        </Card>
        <Card className="bg-slate-800/50 border-slate-700 p-6">
          <div className="text-4xl mb-4">2️⃣</div>
          <h3 className="text-xl font-bold text-white mb-2">Configure</h3>
          <p className="text-gray-400 text-sm">
            Set up integrations, data sources, and workflows
          </p>
        </Card>
        <Card className="bg-slate-800/50 border-slate-700 p-6">
          <div className="text-4xl mb-4">3️⃣</div>
          <h3 className="text-xl font-bold text-white mb-2">Publish</h3>
          <p className="text-gray-400 text-sm">
            Test, price, and publish to the marketplace
          </p>
        </Card>
      </div>

      <Button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-6 text-lg">
        Start Building Your Agent →
      </Button>
    </div>
  )
}
