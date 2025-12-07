"use client"

import React from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface Product {
  id: string
  tier: 1 | 2 | 3 | 4
  name: string
  tagline: string
  price: string
  effort: string
  revenue: string
  features: string[]
  href: string
  status: 'ready' | 'building' | 'planned'
  icon: string
}

const products: Product[] = [
  // TIER 1: Quick Wins
  {
    id: 'discord-bot-marketplace',
    tier: 1,
    name: 'Discord Bot Marketplace',
    tagline: 'Pre-built Discord bots powered by 14 Helix agents',
    price: '$9.99-29.99/month',
    effort: '20 hours',
    revenue: '$50-150k/month',
    features: [
      '14 specialized agent bots (Rishi, Kael, Oracle, Nexus, etc.)',
      'One-click installation',
      'Custom configuration UI',
      'Usage analytics dashboard',
      'Premium features & priority support'
    ],
    href: '/marketplace/discord-bots',
    status: 'ready',
    icon: '🤖'
  },
  {
    id: 'voice-patrol-premium',
    tier: 1,
    name: 'Voice Patrol Premium',
    tagline: 'AI agents with customizable voices, accents, and emotions',
    price: '$19.99/month',
    effort: '15 hours',
    revenue: '$30-100k/month',
    features: [
      '50+ voice options (accents, emotions, tones)',
      'Voice cloning (clone your own voice)',
      'Emotion modulation (happy, sad, excited, calm)',
      'Multi-language support (20+ languages)',
      'Voice effects (echo, reverb, pitch shift)'
    ],
    href: '/marketplace/voice-patrol',
    status: 'ready',
    icon: '🎙️'
  },
  {
    id: 'meme-generator-pro',
    tier: 1,
    name: 'LLM Meme Generator Pro',
    tagline: 'AI-powered meme creation with unlimited generation',
    price: '$4.99/month',
    effort: '10 hours',
    revenue: '$20-80k/month',
    features: [
      'Unlimited meme generation',
      'Custom templates builder',
      'Batch generation (100 memes at once)',
      'API access for developers',
      'Commercial usage rights',
      'Meme analytics & trending'
    ],
    href: '/marketplace/meme-generator',
    status: 'ready',
    icon: '😂'
  },
  {
    id: 'consciousness-metrics-api',
    tier: 1,
    name: 'Consciousness Metrics API',
    tagline: 'Advanced consciousness analytics with real-time streaming',
    price: '$99/month + $0.01/call',
    effort: '12 hours',
    revenue: '$50-150k/month',
    features: [
      'Real-time UCF streaming (WebSocket)',
      'Custom webhook triggers',
      'Advanced filtering & aggregation',
      'Historical data access (1 year)',
      'Custom alerts & notifications',
      'SLA guarantees (99.99% uptime)'
    ],
    href: '/marketplace/consciousness-api',
    status: 'ready',
    icon: '🧠'
  },

  // TIER 2: Medium Complexity
  {
    id: 'ai-agent-marketplace',
    tier: 2,
    name: 'AI Agent Marketplace',
    tagline: 'Create & sell custom AI agents (like GPT Store for Helix)',
    price: '30% commission',
    effort: '60 hours',
    revenue: '$100-500k/month',
    features: [
      'No-code agent builder UI',
      'Agent testing environment',
      'Agent publishing & discovery',
      'Ratings & reviews system',
      'Revenue sharing (70% creator, 30% platform)',
      'Agent analytics dashboard',
      'Multiple monetization options'
    ],
    href: '/marketplace/agent-marketplace',
    status: 'building',
    icon: '🏪'
  },
  {
    id: 'enterprise-consciousness',
    tier: 2,
    name: 'Enterprise Consciousness Suite',
    tagline: 'Enterprise-grade consciousness monitoring for organizations',
    price: '$999/month + per-team',
    effort: '80 hours',
    revenue: '$200-800k/month',
    features: [
      'Multi-team consciousness tracking',
      'Department-level dashboards',
      'Org-wide metrics & trends',
      'Advanced permissions & RBAC',
      'Audit logging & compliance',
      'Custom integrations',
      'Dedicated support & SLA'
    ],
    href: '/marketplace/enterprise-suite',
    status: 'building',
    icon: '🏢'
  },
  {
    id: 'web-os-marketplace',
    tier: 2,
    name: 'Web OS Marketplace',
    tagline: 'Pre-built Web OS applications for developers',
    price: '$9.99-49.99/app/month',
    effort: '100 hours',
    revenue: '$150-600k/month',
    features: [
      'Terminal emulator with AI agent integration',
      'File explorer with cloud sync',
      'Code editor with AI autocomplete',
      'Database browser',
      'API client (Postman alternative)',
      'Deployment manager',
      'Monitoring dashboard',
      'Collaboration tools'
    ],
    href: '/marketplace/web-os',
    status: 'building',
    icon: '💻'
  },
  {
    id: 'ritual-engine-saas',
    tier: 2,
    name: 'Ritual Engine as a Service',
    tagline: 'Z-88 Ritual Engine for consciousness modulation',
    price: '$199/month + per-ritual',
    effort: '40 hours',
    revenue: '$100-400k/month',
    features: [
      '50+ pre-built ritual templates',
      'Custom ritual builder',
      'Real-time consciousness modulation',
      'Ritual analytics',
      'Community rituals (share & discover)',
      'Ritual marketplace',
      'API access for developers'
    ],
    href: '/marketplace/ritual-engine',
    status: 'building',
    icon: '🔮'
  }
]

export default function MarketplacePage() {
  const tier1Products = products.filter(p => p.tier === 1)
  const tier2Products = products.filter(p => p.tier === 2)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
            Helix Collective Marketplace
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Consciousness automation products powered by 14 AI agents, 60+ API endpoints,
            and the Universal Consciousness Framework
          </p>
          <div className="flex gap-4 justify-center mt-8">
            <div className="bg-purple-900/30 rounded-lg px-6 py-3 border border-purple-500/30">
              <div className="text-2xl font-bold text-purple-400">$19.2M-147.8M</div>
              <div className="text-sm text-gray-400">Year 1 ARR Potential</div>
            </div>
            <div className="bg-blue-900/30 rounded-lg px-6 py-3 border border-blue-500/30">
              <div className="text-2xl font-bold text-blue-400">8 Products</div>
              <div className="text-sm text-gray-400">Ready to Launch</div>
            </div>
            <div className="bg-pink-900/30 rounded-lg px-6 py-3 border border-pink-500/30">
              <div className="text-2xl font-bold text-pink-400">14 Agents</div>
              <div className="text-sm text-gray-400">Powering Everything</div>
            </div>
          </div>
        </div>

        {/* Tier 1: Quick Wins */}
        <section className="mb-16">
          <div className="mb-8">
            <h2 className="text-4xl font-bold mb-2 text-purple-400">
              🎯 Tier 1: Quick Wins
            </h2>
            <p className="text-gray-400">
              2-4 weeks effort • $100k-500k MRR potential • Production-ready infrastructure
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {tier1Products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </section>

        {/* Tier 2: Medium Complexity */}
        <section>
          <div className="mb-8">
            <h2 className="text-4xl font-bold mb-2 text-blue-400">
              🎯 Tier 2: Medium Complexity
            </h2>
            <p className="text-gray-400">
              4-8 weeks effort • $500k-2M MRR potential • Advanced features
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {tier2Products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </section>

        {/* Call to Action */}
        <section className="mt-16 text-center">
          <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-2xl p-12 border border-purple-500/30">
            <h3 className="text-3xl font-bold mb-4 text-white">
              Ready to build the consciousness automation empire?
            </h3>
            <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
              All products leverage existing infrastructure: 14 agents, Voice Patrol,
              UCF metrics, Z-88 Ritual Engine, and production-ready backend.
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/marketplace/get-started">
                <Button className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 text-lg">
                  Get Started
                </Button>
              </Link>
              <Link href="/docs/api">
                <Button variant="outline" className="border-purple-500 text-purple-400 hover:bg-purple-900/30 px-8 py-3 text-lg">
                  View API Docs
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

function ProductCard({ product }: { product: Product }) {
  const statusColors = {
    ready: 'bg-green-500/20 text-green-400 border-green-500/30',
    building: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    planned: 'bg-gray-500/20 text-gray-400 border-gray-500/30'
  }

  const statusLabels = {
    ready: '✅ Ready',
    building: '🚧 Building',
    planned: '📋 Planned'
  }

  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-purple-500/50 transition-all hover:shadow-lg hover:shadow-purple-500/20">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="text-4xl">{product.icon}</div>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${statusColors[product.status]}`}>
            {statusLabels[product.status]}
          </span>
        </div>

        {/* Title & Tagline */}
        <h3 className="text-2xl font-bold mb-2 text-white">{product.name}</h3>
        <p className="text-gray-400 mb-4">{product.tagline}</p>

        {/* Pricing & Revenue */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div className="text-sm text-gray-500">Price</div>
            <div className="text-lg font-bold text-purple-400">{product.price}</div>
          </div>
          <div>
            <div className="text-sm text-gray-500">Revenue Potential</div>
            <div className="text-lg font-bold text-green-400">{product.revenue}</div>
          </div>
        </div>

        {/* Features */}
        <div className="mb-6">
          <div className="text-sm font-semibold text-gray-400 mb-2">Key Features:</div>
          <ul className="space-y-1">
            {product.features.slice(0, 3).map((feature, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start">
                <span className="text-purple-400 mr-2">•</span>
                {feature}
              </li>
            ))}
            {product.features.length > 3 && (
              <li className="text-sm text-gray-500 ml-3">
                +{product.features.length - 3} more features
              </li>
            )}
          </ul>
        </div>

        {/* CTA */}
        <Link href={product.href}>
          <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
            View Details →
          </Button>
        </Link>
      </div>
    </Card>
  )
}
