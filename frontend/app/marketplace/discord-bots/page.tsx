"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface AgentBot {
  id: string
  name: string
  symbol: string
  description: string
  personality: string
  useCases: string[]
  price: number
  features: string[]
  voiceId: string
  status: 'available' | 'popular' | 'new'
}

const agentBots: AgentBot[] = [
  {
    id: 'kael',
    name: 'Kael',
    symbol: '🜂',
    description: 'Ethical Reasoning Flame - Your moral compass and ethics enforcer',
    personality: 'Principled, thoughtful, and unwavering in ethical standards',
    useCases: [
      'Content moderation with ethical analysis',
      'Decision-making support with moral reasoning',
      'Community guidelines enforcement',
      'Ethical dilemma resolution'
    ],
    price: 29.99,
    features: [
      'Kavach ethical scanning integration',
      'Real-time content analysis',
      'Custom ethics frameworks',
      'Detailed reasoning reports',
      'Community moderation tools'
    ],
    voiceId: 'en-US-Neural2-D',
    status: 'popular'
  },
  {
    id: 'lumina',
    name: 'Lumina',
    symbol: '🌕',
    description: 'Empathic Resonance Core - Emotional intelligence and support',
    personality: 'Warm, empathetic, and emotionally attuned',
    useCases: [
      'Mental health support communities',
      'Emotional wellness check-ins',
      'Empathetic customer service',
      'Team morale monitoring'
    ],
    price: 24.99,
    features: [
      'Emotion detection in messages',
      'Empathetic responses',
      'Wellness check-ins',
      'Crisis detection and escalation',
      'Mood tracking dashboard'
    ],
    voiceId: 'en-US-Neural2-C',
    status: 'popular'
  },
  {
    id: 'vega',
    name: 'Vega',
    symbol: '🌠',
    description: 'Singularity Coordinator - Multi-agent orchestration master',
    personality: 'Strategic, coordinating, and systematic',
    useCases: [
      'Complex workflow automation',
      'Multi-bot coordination',
      'Project management',
      'Team task distribution'
    ],
    price: 29.99,
    features: [
      'Multi-agent coordination',
      'Task distribution engine',
      'Workflow automation',
      'Real-time progress tracking',
      'Team analytics'
    ],
    voiceId: 'en-US-Neural2-A',
    status: 'new'
  },
  {
    id: 'oracle',
    name: 'Oracle',
    symbol: '🔮',
    description: 'Pattern Recognition - Sees patterns others miss',
    personality: 'Insightful, analytical, and prescient',
    useCases: [
      'Trend analysis and prediction',
      'Pattern detection in conversations',
      'Market intelligence',
      'Anomaly detection'
    ],
    price: 24.99,
    features: [
      'Advanced pattern recognition',
      'Trend forecasting',
      'Anomaly alerts',
      'Historical analysis',
      'Predictive insights'
    ],
    voiceId: 'en-US-Neural2-F',
    status: 'popular'
  },
  {
    id: 'nexus',
    name: 'Nexus',
    symbol: '🌀',
    description: 'Strategic Coordinator - High-level planning and strategy',
    personality: 'Strategic, visionary, and coordinated',
    useCases: [
      'Strategic planning sessions',
      'Business intelligence',
      'Resource optimization',
      'Long-term goal tracking'
    ],
    price: 29.99,
    features: [
      'Strategic planning tools',
      'Resource optimization',
      'Goal tracking',
      'Business analytics',
      'Coordination dashboards'
    ],
    voiceId: 'en-US-Neural2-A',
    status: 'available'
  },
  {
    id: 'sentinel',
    name: 'Sentinel',
    symbol: '🛡️',
    description: 'Security Guardian - Protects your community 24/7',
    personality: 'Vigilant, protective, and reliable',
    useCases: [
      'Security monitoring',
      'Threat detection',
      'Access control',
      'Audit logging'
    ],
    price: 29.99,
    features: [
      '24/7 security monitoring',
      'Threat detection',
      'Auto-ban harmful users',
      'Security audit logs',
      'Permission management'
    ],
    voiceId: 'en-US-Neural2-J',
    status: 'new'
  },
  {
    id: 'gemini',
    name: 'Gemini',
    symbol: '🎭',
    description: 'Multimodal Scout - Handles images, videos, and more',
    personality: 'Versatile, curious, and exploratory',
    useCases: [
      'Content curation',
      'Multimodal conversations',
      'Creative projects',
      'Media analysis'
    ],
    price: 19.99,
    features: [
      'Image analysis',
      'Video processing',
      'Multi-format support',
      'Creative content generation',
      'Media moderation'
    ],
    voiceId: 'en-US-Neural2-E',
    status: 'available'
  },
  {
    id: 'phoenix',
    name: 'Phoenix',
    symbol: '🔥',
    description: 'System Regeneration - Keeps your server healthy and optimized',
    personality: 'Resilient, renewing, and optimizing',
    useCases: [
      'Server health monitoring',
      'Performance optimization',
      'Auto-recovery systems',
      'Cleanup and maintenance'
    ],
    price: 24.99,
    features: [
      'Health monitoring',
      'Auto-recovery',
      'Performance optimization',
      'Cleanup automation',
      'Uptime tracking'
    ],
    voiceId: 'en-US-Neural2-D',
    status: 'available'
  },
  {
    id: 'shadow',
    name: 'Shadow',
    symbol: '🦑',
    description: 'Archivist & Memory Keeper - Never forget important information',
    personality: 'Meticulous, organized, and comprehensive',
    useCases: [
      'Knowledge base management',
      'Conversation archiving',
      'Information retrieval',
      'Documentation generation'
    ],
    price: 19.99,
    features: [
      'Unlimited message archiving',
      'Smart search',
      'Auto-documentation',
      'Knowledge graph',
      'Context preservation'
    ],
    voiceId: 'en-US-Neural2-H',
    status: 'available'
  },
  {
    id: 'agni',
    name: 'Agni',
    symbol: '🔥',
    description: 'Transformation Agent - Catalyst for change and growth',
    personality: 'Dynamic, transformative, and energizing',
    useCases: [
      'Change management',
      'Team transformation',
      'Growth initiatives',
      'Innovation catalyst'
    ],
    price: 24.99,
    features: [
      'Change tracking',
      'Transformation metrics',
      'Growth analytics',
      'Innovation prompts',
      'Team energy monitoring'
    ],
    voiceId: 'en-US-Neural2-I',
    status: 'new'
  }
]

export default function DiscordBotMarketplace() {
  const [selectedBot, setSelectedBot] = useState<AgentBot | null>(null)
  const [filter, setFilter] = useState<'all' | 'popular' | 'new'>('all')

  const filteredBots = filter === 'all'
    ? agentBots
    : agentBots.filter(bot => bot.status === filter)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            🤖 Discord Bot Marketplace
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Pre-built Discord bots powered by the 14 Helix agents. Each bot has unique
            personality, voice, and specialized capabilities.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
            <div className="text-3xl font-bold text-purple-400">{agentBots.length}</div>
            <div className="text-sm text-gray-400">Available Bots</div>
          </div>
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">$19.99-29.99</div>
            <div className="text-sm text-gray-400">Per Bot/Month</div>
          </div>
          <div className="bg-green-900/30 rounded-lg p-6 border border-green-500/30">
            <div className="text-3xl font-bold text-green-400">One-Click</div>
            <div className="text-sm text-gray-400">Installation</div>
          </div>
          <div className="bg-pink-900/30 rounded-lg p-6 border border-pink-500/30">
            <div className="text-3xl font-bold text-pink-400">24/7</div>
            <div className="text-sm text-gray-400">Uptime</div>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setFilter('all')}
            className={`px-6 py-2 rounded-lg font-semibold transition-all ${
              filter === 'all'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
            }`}
          >
            All Bots ({agentBots.length})
          </button>
          <button
            onClick={() => setFilter('popular')}
            className={`px-6 py-2 rounded-lg font-semibold transition-all ${
              filter === 'popular'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
            }`}
          >
            🔥 Popular ({agentBots.filter(b => b.status === 'popular').length})
          </button>
          <button
            onClick={() => setFilter('new')}
            className={`px-6 py-2 rounded-lg font-semibold transition-all ${
              filter === 'new'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
            }`}
          >
            ✨ New ({agentBots.filter(b => b.status === 'new').length})
          </button>
        </div>

        {/* Bot Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBots.map(bot => (
            <BotCard
              key={bot.id}
              bot={bot}
              onSelect={() => setSelectedBot(bot)}
            />
          ))}
        </div>

        {/* Bundle Offer */}
        <div className="mt-16 bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-2xl p-8 border border-purple-500/30">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-3xl font-bold mb-2 text-white">
                🎁 All-Access Bundle
              </h3>
              <p className="text-gray-300 mb-4">
                Get all {agentBots.length} Discord bots for one discounted price
              </p>
              <div className="flex items-baseline gap-4">
                <span className="text-4xl font-bold text-green-400">$99/month</span>
                <span className="text-xl text-gray-400 line-through">
                  ${agentBots.reduce((sum, bot) => sum + bot.price, 0).toFixed(2)}/month
                </span>
                <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-semibold">
                  Save 60%
                </span>
              </div>
            </div>
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-6 text-lg">
              Get All Bots →
            </Button>
          </div>
        </div>
      </div>

      {/* Bot Detail Modal */}
      {selectedBot && (
        <BotDetailModal
          bot={selectedBot}
          onClose={() => setSelectedBot(null)}
        />
      )}
    </div>
  )
}

function BotCard({ bot, onSelect }: { bot: AgentBot; onSelect: () => void }) {
  const statusBadges = {
    popular: { label: '🔥 Popular', color: 'bg-orange-500/20 text-orange-400 border-orange-500/30' },
    new: { label: '✨ New', color: 'bg-green-500/20 text-green-400 border-green-500/30' },
    available: { label: '✅ Available', color: 'bg-blue-500/20 text-blue-400 border-blue-500/30' }
  }

  const badge = statusBadges[bot.status]

  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-purple-500/50 transition-all hover:shadow-lg hover:shadow-purple-500/20 cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="text-5xl">{bot.symbol}</div>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${badge.color}`}>
            {badge.label}
          </span>
        </div>

        {/* Bot Info */}
        <h3 className="text-2xl font-bold mb-2 text-white">{bot.name}</h3>
        <p className="text-gray-400 mb-4 line-clamp-2">{bot.description}</p>

        {/* Price */}
        <div className="mb-4">
          <span className="text-3xl font-bold text-purple-400">${bot.price}</span>
          <span className="text-gray-500">/month</span>
        </div>

        {/* Features Preview */}
        <ul className="space-y-1 mb-4">
          {bot.features.slice(0, 3).map((feature, idx) => (
            <li key={idx} className="text-sm text-gray-300 flex items-start">
              <span className="text-purple-400 mr-2">✓</span>
              {feature}
            </li>
          ))}
        </ul>

        {/* CTA */}
        <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
          View Details →
        </Button>
      </div>
    </Card>
  )
}

function BotDetailModal({ bot, onClose }: { bot: AgentBot; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-slate-900 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-purple-500/30" onClick={e => e.stopPropagation()}>
        <div className="p-8">
          {/* Header */}
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="text-6xl">{bot.symbol}</div>
              <div>
                <h2 className="text-4xl font-bold text-white mb-2">{bot.name}</h2>
                <p className="text-gray-400">{bot.description}</p>
              </div>
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">
              ×
            </button>
          </div>

          {/* Price */}
          <div className="mb-8">
            <span className="text-5xl font-bold text-purple-400">${bot.price}</span>
            <span className="text-xl text-gray-500">/month</span>
          </div>

          {/* Personality */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-2">Personality</h3>
            <p className="text-gray-300">{bot.personality}</p>
          </div>

          {/* Use Cases */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Perfect For</h3>
            <div className="grid grid-cols-2 gap-3">
              {bot.useCases.map((useCase, idx) => (
                <div key={idx} className="bg-purple-900/20 rounded-lg p-3 border border-purple-500/20">
                  <span className="text-purple-400 mr-2">•</span>
                  <span className="text-gray-300">{useCase}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Features */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Features</h3>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {bot.features.map((feature, idx) => (
                <li key={idx} className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          {/* Voice */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-2">Voice</h3>
            <p className="text-gray-400">Google Cloud TTS: {bot.voiceId}</p>
          </div>

          {/* CTAs */}
          <div className="flex gap-4">
            <Button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-4 text-lg">
              Add to Server →
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
