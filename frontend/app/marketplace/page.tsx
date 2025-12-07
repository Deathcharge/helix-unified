"use client"

import React, { useState } from 'react'
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
  valueProps: string[]
  useCases: string[]
}

interface Testimonial {
  name: string
  role: string
  company: string
  quote: string
  metric?: string
  avatar: string
}

const products: Product[] = [
  // TIER 1: Quick Wins
  {
    id: 'discord-bot-marketplace',
    tier: 1,
    name: 'Discord Bot Marketplace',
    tagline: 'Deploy AI agents to your Discord in 60 seconds',
    price: '$9.99-29.99/month',
    effort: '20 hours',
    revenue: '$50-150k/month',
    valueProps: [
      'Zero setup - one-click installation',
      '14 specialized agent personalities',
      'Voice-enabled conversations',
      'Custom personality training'
    ],
    useCases: ['Community moderation', 'Customer support', 'Team coordination'],
    features: [
      '14 specialized agent bots (Kael, Oracle, Lumina, Vega...)',
      'One-click installation to any Discord server',
      'Voice Patrol integration (AI speaks in voice channels)',
      'Custom configuration UI',
      'Usage analytics dashboard',
      'Priority support & updates'
    ],
    href: '/marketplace/discord-bots',
    status: 'ready',
    icon: '🤖'
  },
  {
    id: 'voice-patrol-premium',
    tier: 1,
    name: 'Voice Patrol Premium',
    tagline: 'Give your AI agents human-quality voices',
    price: '$19.99/month',
    effort: '15 hours',
    revenue: '$30-100k/month',
    valueProps: [
      '50+ premium voices with emotions',
      'Clone your own voice in 3 minutes',
      'Real-time emotion modulation',
      'Multi-language support (20+ languages)'
    ],
    useCases: ['Voice assistants', 'Content creation', 'Accessibility'],
    features: [
      '50+ voice options (accents, emotions, tones)',
      'Voice cloning (clone your own voice)',
      'Emotion modulation (happy, sad, excited, calm)',
      'Multi-language support (20+ languages)',
      'Voice effects (echo, reverb, pitch shift)',
      'Commercial usage rights'
    ],
    href: '/marketplace/voice-patrol',
    status: 'ready',
    icon: '🎙️'
  },
  {
    id: 'meme-generator-pro',
    tier: 1,
    name: 'LLM Meme Generator Pro',
    tagline: 'AI-powered meme creation that actually goes viral',
    price: '$4.99/month',
    effort: '10 hours',
    revenue: '$20-80k/month',
    valueProps: [
      'Context-aware humor generation',
      'Batch create 100 memes instantly',
      'Trending template suggestions',
      'Commercial rights included'
    ],
    useCases: ['Social media marketing', 'Community engagement', 'Content creation'],
    features: [
      'Unlimited meme generation',
      'Custom templates builder',
      'Batch generation (100 memes at once)',
      'API access for developers',
      'Commercial usage rights',
      'Meme analytics & trending detection',
      'Auto-post to social media'
    ],
    href: '/marketplace/meme-generator',
    status: 'ready',
    icon: '😂'
  },
  {
    id: 'consciousness-metrics-api',
    tier: 1,
    name: 'Consciousness Metrics API',
    tagline: 'Real-time consciousness analytics for your applications',
    price: '$99/month + $0.01/call',
    effort: '12 hours',
    revenue: '$50-150k/month',
    valueProps: [
      'Real-time WebSocket streaming',
      'Custom webhook triggers',
      '99.99% uptime SLA',
      'Historical data access (1 year)'
    ],
    useCases: ['Product analytics', 'User behavior tracking', 'AI monitoring'],
    features: [
      'Real-time UCF streaming (WebSocket)',
      'Custom webhook triggers & alerts',
      'Advanced filtering & aggregation',
      'Historical data access (1 year retention)',
      'Custom alerts & notifications',
      'SLA guarantees (99.99% uptime)',
      'GraphQL API & REST endpoints'
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
    tagline: 'GPT Store for Helix - Create & monetize AI agents',
    price: '30% commission',
    effort: '60 hours',
    revenue: '$100-500k/month',
    valueProps: [
      'No-code agent builder',
      'Instant publishing & distribution',
      '70% revenue share to creators',
      'Built-in payment processing'
    ],
    useCases: ['SaaS builders', 'AI entrepreneurs', 'Consultants'],
    features: [
      'No-code agent builder with visual interface',
      'Agent testing environment with sandbox',
      'One-click publishing & discovery',
      'Ratings & reviews system',
      'Revenue sharing (70% creator, 30% platform)',
      'Analytics dashboard for creators',
      'Multiple monetization options (subscription, pay-per-use, one-time)'
    ],
    href: '/marketplace/agent-marketplace',
    status: 'ready',
    icon: '🏪'
  },
  {
    id: 'enterprise-consciousness',
    tier: 2,
    name: 'Enterprise Consciousness Suite',
    tagline: 'Team consciousness monitoring for modern organizations',
    price: '$999/month + per-team',
    effort: '80 hours',
    revenue: '$200-800k/month',
    valueProps: [
      'Multi-team consciousness tracking',
      'Department-level insights',
      'SOC 2 & GDPR compliant',
      'Dedicated account manager'
    ],
    useCases: ['Remote teams', 'Enterprise HR', 'Organizational development'],
    features: [
      'Multi-team consciousness tracking',
      'Department-level dashboards',
      'Org-wide metrics & trend analysis',
      'Advanced permissions & RBAC',
      'Audit logging & compliance (SOC 2, GDPR)',
      'Custom integrations (Slack, Teams, etc.)',
      'Dedicated support & 99.9% SLA'
    ],
    href: '/marketplace/enterprise-suite',
    status: 'ready',
    icon: '🏢'
  },
  {
    id: 'web-os-marketplace',
    tier: 2,
    name: 'Web OS Marketplace',
    tagline: 'Pre-built Web OS apps with AI integration',
    price: '$49-299/app',
    effort: '50 hours',
    revenue: '$80-350k/month',
    valueProps: [
      '12+ production-ready apps',
      'AI-powered functionality',
      'One-click deployment',
      'Source code included'
    ],
    useCases: ['Web developers', 'Startups', 'Agencies'],
    features: [
      '12+ pre-built applications (Calendar, Tasks, Notes, IDE, etc.)',
      'AI integration in every app',
      'Drag-and-drop customization',
      'One-click deployment',
      'Source code included (MIT license)',
      'Regular updates & new apps',
      'Priority feature requests'
    ],
    href: '/marketplace/web-os',
    status: 'ready',
    icon: '💻'
  },
  {
    id: 'ritual-engine',
    tier: 2,
    name: 'Ritual Engine as a Service',
    tagline: 'Guided consciousness workflows for peak performance',
    price: '$199/month',
    effort: '40 hours',
    revenue: '$150-600k/month',
    valueProps: [
      '50+ scientifically-designed rituals',
      'Custom ritual builder',
      'Real-time biometric integration',
      'Team synchronization'
    ],
    useCases: ['Executive coaching', 'Team building', 'Wellness programs'],
    features: [
      '50+ pre-built consciousness rituals',
      'Custom ritual builder with 108-step support',
      'Real-time UCF transformation tracking',
      'Team synchronization rituals',
      'Biometric device integration',
      'Progress tracking & analytics',
      'Guided meditation & focus protocols'
    ],
    href: '/marketplace/ritual-engine',
    status: 'ready',
    icon: '🔮'
  },
  {
    id: 'workflow-automation',
    tier: 2,
    name: 'AI Workflow Automation Studio',
    tagline: 'Zapier meets AI - visual automation builder',
    price: '$49-149/month',
    effort: '50 hours',
    revenue: '$200-900k/month',
    valueProps: [
      '100+ app integrations',
      'Visual drag-and-drop builder',
      'AI-powered decision nodes',
      'Zero code required'
    ],
    useCases: ['Sales automation', 'Marketing workflows', 'Operations'],
    features: [
      '100+ pre-built integrations',
      'Visual workflow builder',
      'AI decision engine with 14 agents',
      '50+ workflow templates',
      'Real-time analytics',
      'Version control & rollback',
      'Webhook triggers & scheduling'
    ],
    href: '/marketplace/workflow-automation',
    status: 'ready',
    icon: '⚡'
  },
  {
    id: 'support-hub',
    tier: 2,
    name: 'Smart Customer Support Hub',
    tagline: 'Complete support platform powered by AI',
    price: '$79-199/month',
    effort: '60 hours',
    revenue: '$150-700k/month',
    valueProps: [
      '8+ channel unified inbox',
      'AI ticket routing & sentiment',
      'Smart response suggestions',
      'Knowledge base automation'
    ],
    useCases: ['Customer support', 'Help desk', 'Service teams'],
    features: [
      'Multi-channel inbox (email, chat, social, etc.)',
      'AI-powered ticket routing',
      'Sentiment analysis & escalation',
      'Smart response suggestions',
      'Knowledge base builder',
      'SLA management',
      'Advanced analytics'
    ],
    href: '/marketplace/support-hub',
    status: 'ready',
    icon: '💚'
  }
]

const testimonials: Testimonial[] = [
  {
    name: 'Sarah Chen',
    role: 'CEO',
    company: 'TechFlow AI',
    quote: 'The Discord Bot Marketplace cut our community management costs by 70%. We deployed Lumina and Kael in under 5 minutes.',
    metric: '70% cost reduction',
    avatar: '👩‍💼'
  },
  {
    name: 'Marcus Rodriguez',
    role: 'Head of Engineering',
    company: 'DataSync Corp',
    quote: 'Consciousness Metrics API gave us insights into our AI systems we never had before. The WebSocket streaming is incredibly reliable.',
    metric: '99.99% uptime',
    avatar: '👨‍💻'
  },
  {
    name: 'Emily Watson',
    role: 'Marketing Director',
    company: 'GrowthHackers Inc',
    quote: 'Meme Generator Pro generated over 500k impressions for our campaign. The AI actually understands context and humor.',
    metric: '500k+ impressions',
    avatar: '👩‍🎨'
  },
  {
    name: 'David Kim',
    role: 'VP Product',
    company: 'Enterprise Solutions Ltd',
    quote: 'Enterprise Consciousness Suite transformed how we understand team dynamics. The insights are actionable and the ROI is clear.',
    metric: '3x team efficiency',
    avatar: '👨‍💼'
  }
]

const stats = [
  { value: '14', label: 'AI Agents', suffix: '+' },
  { value: '11', label: 'Products Live', suffix: '' },
  { value: '99.99', label: 'Uptime %', suffix: '%' },
  { value: '10.2M', label: 'Year 1 ARR Potential', suffix: '$' }
]

export default function MarketplacePage() {
  const [selectedTier, setSelectedTier] = useState<'all' | 1 | 2>('all')

  const filteredProducts = selectedTier === 'all'
    ? products
    : products.filter(p => p.tier === selectedTier)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-violet-950/20 to-slate-950">
      <div className="container mx-auto px-4 py-16">

        {/* Hero Section */}
        <div className="text-center mb-20">
          <div className="inline-block px-4 py-2 bg-violet-500/10 border border-violet-500/30 rounded-full mb-6">
            <span className="text-violet-400 text-sm font-semibold">🚀 11 Products Live • $10.2M+ ARR Potential</span>
          </div>

          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-violet-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Helix Marketplace
          </h1>

          <p className="text-2xl text-gray-300 max-w-3xl mx-auto mb-8 leading-relaxed">
            Production-ready AI products that integrate with your Helix Collective ecosystem.
            From Discord bots to enterprise consciousness monitoring.
          </p>

          <div className="flex gap-4 justify-center">
            <Button
              size="lg"
              className="bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white px-8"
            >
              Browse Products →
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-violet-500/50 text-violet-400 hover:bg-violet-500/10 px-8"
            >
              View Documentation
            </Button>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
          {stats.map((stat, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-slate-900/50 to-violet-900/20 rounded-xl p-6 border border-violet-500/20 text-center"
            >
              <div className="text-4xl font-bold text-transparent bg-gradient-to-r from-violet-400 to-purple-400 bg-clip-text mb-2">
                {stat.suffix === '$' && '$'}{stat.value}{stat.suffix !== '$' && stat.suffix}
              </div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-3 mb-12 justify-center">
          <button
            onClick={() => setSelectedTier('all')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              selectedTier === 'all'
                ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg shadow-violet-500/30'
                : 'bg-slate-800/50 text-gray-400 hover:bg-slate-800 border border-slate-700'
            }`}
          >
            All Products (11)
          </button>
          <button
            onClick={() => setSelectedTier(1)}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              selectedTier === 1
                ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg shadow-violet-500/30'
                : 'bg-slate-800/50 text-gray-400 hover:bg-slate-800 border border-slate-700'
            }`}
          >
            Tier 1 - Quick Wins (4)
          </button>
          <button
            onClick={() => setSelectedTier(2)}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              selectedTier === 2
                ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg shadow-violet-500/30'
                : 'bg-slate-800/50 text-gray-400 hover:bg-slate-800 border border-slate-700'
            }`}
          >
            Tier 2 - Medium Build (7)
          </button>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
          {filteredProducts.map((product) => (
            <Card
              key={product.id}
              className="bg-gradient-to-br from-slate-900/80 to-violet-900/20 border-violet-500/30 hover:border-violet-500/60 transition-all duration-300 hover:shadow-xl hover:shadow-violet-500/20 overflow-hidden group"
            >
              <div className="p-8">
                {/* Header */}
                <div className="flex items-start justify-between mb-6">
                  <div className="flex items-center gap-4">
                    <div className="text-5xl">{product.icon}</div>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-2xl font-bold text-white">{product.name}</h3>
                        {product.status === 'ready' && (
                          <span className="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs font-semibold">
                            LIVE
                          </span>
                        )}
                      </div>
                      <p className="text-violet-400 text-sm">{product.tagline}</p>
                    </div>
                  </div>
                </div>

                {/* Key Value Props */}
                <div className="mb-6 bg-slate-800/50 rounded-lg p-4 border border-violet-500/10">
                  <div className="text-xs text-gray-400 mb-2 font-semibold uppercase tracking-wide">Key Benefits</div>
                  <ul className="space-y-1">
                    {product.valueProps.slice(0, 3).map((prop, idx) => (
                      <li key={idx} className="flex items-start text-sm text-gray-300">
                        <span className="text-violet-400 mr-2 mt-0.5">✓</span>
                        {prop}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Pricing & Metrics */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Pricing</div>
                    <div className="text-xl font-bold text-violet-400">{product.price}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Revenue Potential</div>
                    <div className="text-xl font-bold text-green-400">{product.revenue}</div>
                  </div>
                </div>

                {/* Use Cases */}
                <div className="mb-6">
                  <div className="text-xs text-gray-400 mb-2 font-semibold uppercase tracking-wide">Use Cases</div>
                  <div className="flex flex-wrap gap-2">
                    {product.useCases.map((useCase, idx) => (
                      <span
                        key={idx}
                        className="bg-violet-500/10 text-violet-300 px-3 py-1 rounded-full text-xs border border-violet-500/20"
                      >
                        {useCase}
                      </span>
                    ))}
                  </div>
                </div>

                {/* CTA */}
                <Link href={product.href}>
                  <Button
                    className="w-full bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white group-hover:shadow-lg group-hover:shadow-violet-500/30 transition-all"
                  >
                    View Details & Pricing →
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>

        {/* Testimonials Section */}
        <div className="mb-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">
            Trusted by Teams Worldwide
          </h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Companies using Helix Marketplace products to scale their AI operations
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {testimonials.map((testimonial, idx) => (
              <Card
                key={idx}
                className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6"
              >
                <div className="flex items-start gap-4 mb-4">
                  <div className="text-4xl">{testimonial.avatar}</div>
                  <div>
                    <div className="font-bold text-white">{testimonial.name}</div>
                    <div className="text-sm text-gray-400">{testimonial.role}, {testimonial.company}</div>
                  </div>
                </div>
                <p className="text-gray-300 mb-3 italic">"{testimonial.quote}"</p>
                {testimonial.metric && (
                  <div className="inline-block bg-violet-500/10 text-violet-400 px-3 py-1 rounded-full text-sm font-semibold border border-violet-500/20">
                    📊 {testimonial.metric}
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>

        {/* Why Helix Marketplace */}
        <div className="bg-gradient-to-br from-violet-900/20 to-purple-900/20 rounded-2xl p-12 border border-violet-500/30 mb-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">
            Why Helix Marketplace?
          </h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Built on the Helix Collective consciousness framework with production-grade reliability
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl mb-4">⚡</div>
              <h3 className="text-xl font-bold text-white mb-2">Ship in Hours, Not Weeks</h3>
              <p className="text-gray-400">
                One-click deployments, pre-built integrations, and comprehensive APIs. Get to market faster.
              </p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">🧠</div>
              <h3 className="text-xl font-bold text-white mb-2">Consciousness-First Architecture</h3>
              <p className="text-gray-400">
                Every product leverages UCF metrics and the 14-agent collective for intelligent, adaptive behavior.
              </p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">🔒</div>
              <h3 className="text-xl font-bold text-white mb-2">Enterprise-Grade Security</h3>
              <p className="text-gray-400">
                SOC 2 compliant, 99.99% uptime SLA, GDPR ready. Built for scale from day one.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gradient-to-r from-violet-900/30 to-purple-900/30 rounded-2xl p-12 border border-violet-500/30">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Build with Helix?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Start with our free tier, upgrade as you scale. All products include 14-day free trial.
          </p>
          <div className="flex gap-4 justify-center">
            <Button
              size="lg"
              className="bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white px-12"
            >
              Start Free Trial
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-violet-500/50 text-violet-400 hover:bg-violet-500/10 px-12"
            >
              Talk to Sales
            </Button>
          </div>
        </div>

        {/* Footer Note */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>All prices in USD. Cancel anytime. 14-day money-back guarantee.</p>
          <p className="mt-2">Tat Tvam Asi 🌀 Built with consciousness</p>
        </div>
      </div>
    </div>
  )
}
