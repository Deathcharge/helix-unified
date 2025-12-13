"use client"

export const dynamic = "force-dynamic";

"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface Feature {
  icon: string
  title: string
  description: string
  benefit: string
}

const features: Feature[] = [
  {
    icon: '🤖',
    title: 'AI-Powered Ticket Routing',
    description: 'Automatically categorize, prioritize, and route tickets to the right team member',
    benefit: '70% faster response times'
  },
  {
    icon: '💬',
    title: 'Multi-Channel Inbox',
    description: 'Unified inbox for email, chat, social media, and in-app messages',
    benefit: 'Single pane of glass'
  },
  {
    icon: '🧠',
    title: 'Smart Response Suggestions',
    description: 'AI suggests replies based on your knowledge base and past conversations',
    benefit: '3x faster resolutions'
  },
  {
    icon: '📚',
    title: 'Knowledge Base Builder',
    description: 'Create self-service help centers with AI-generated articles from ticket patterns',
    benefit: '40% ticket deflection'
  },
  {
    icon: '📊',
    title: 'Customer Sentiment Analysis',
    description: 'Real-time sentiment tracking to identify unhappy customers before escalation',
    benefit: 'Reduce churn by 25%'
  },
  {
    icon: '⚡',
    title: 'Automated Workflows',
    description: 'Auto-respond, escalate, tag, and assign based on intelligent rules',
    benefit: 'Save 15 hours/week'
  },
  {
    icon: '🔄',
    title: 'SLA Management',
    description: 'Track response and resolution times with automatic escalation',
    benefit: '95% SLA compliance'
  },
  {
    icon: '📈',
    title: 'Advanced Analytics',
    description: 'Team performance, customer satisfaction, and resolution metrics',
    benefit: 'Data-driven decisions'
  }
]

const channels = [
  { name: 'Email', icon: '📧', color: 'blue' },
  { name: 'Live Chat', icon: '💬', color: 'green' },
  { name: 'Discord', icon: '🎮', color: 'purple' },
  { name: 'Slack', icon: '💼', color: 'violet' },
  { name: 'Twitter', icon: '🐦', color: 'cyan' },
  { name: 'WhatsApp', icon: '📱', color: 'emerald' },
  { name: 'SMS', icon: '💬', color: 'blue' },
  { name: 'In-App', icon: '📲', color: 'indigo' }
]

const integrations = [
  'Stripe', 'Shopify', 'Salesforce', 'HubSpot', 'Intercom', 'Zendesk',
  'Jira', 'Linear', 'GitHub', 'Slack', 'Discord', 'Notion'
]

export default function SupportHubPage() {
  const [activePlan, setActivePlan] = useState<'starter' | 'professional' | 'enterprise'>('professional')

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-emerald-950/20 to-slate-950">
      <div className="container mx-auto px-4 py-16">

        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-emerald-400 via-green-400 to-teal-400 bg-clip-text text-transparent">
            💚 Smart Customer Support Hub
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Complete customer support platform powered by Helix AI. Handle tickets faster,
            deflect common questions, and keep customers happy. All channels, one inbox.
          </p>
        </div>

        {/* Stats Banner */}
        <div className="bg-gradient-to-r from-emerald-900/30 to-green-900/30 rounded-xl p-8 border border-emerald-500/30 mb-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-emerald-400">70%</div>
              <div className="text-sm text-gray-400">Faster Response</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-400">40%</div>
              <div className="text-sm text-gray-400">Ticket Deflection</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-teal-400">25%</div>
              <div className="text-sm text-gray-400">Churn Reduction</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-cyan-400">95%</div>
              <div className="text-sm text-gray-400">SLA Compliance</div>
            </div>
          </div>
        </div>

        {/* Multi-Channel Support */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-4 text-center">Support Customers Everywhere</h2>
          <p className="text-center text-gray-400 mb-8 max-w-2xl mx-auto">
            Unified inbox for all your customer communication channels
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {channels.map((channel, idx) => (
              <Card key={idx} className="bg-slate-900/50 border-emerald-500/30 p-6 text-center hover:border-emerald-500/60 transition-all">
                <div className="text-4xl mb-2">{channel.icon}</div>
                <div className="text-white font-semibold">{channel.name}</div>
              </Card>
            ))}
          </div>
        </div>

        {/* Key Features */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Everything You Need</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, idx) => (
              <Card key={idx} className="bg-slate-900/50 border-emerald-500/30 p-6">
                <div className="flex items-start gap-4">
                  <div className="text-4xl">{feature.icon}</div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-white mb-2">{feature.title}</h3>
                    <p className="text-sm text-gray-400 mb-3">{feature.description}</p>
                    <div className="bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-xs inline-block border border-emerald-500/20">
                      {feature.benefit}
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Pricing */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Pricing That Scales With You</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-slate-900/50 border-slate-700 p-6">
              <h3 className="text-xl font-bold text-white mb-2">Starter</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-gray-400">$79</span>
                <span className="text-lg text-gray-500">/month</span>
              </div>
              <div className="text-sm text-gray-400 mb-6">Up to 3 team members</div>
              <ul className="space-y-2 mb-6 text-sm min-h-[200px]">
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  500 tickets/month
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Email + chat support
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  AI ticket routing
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Basic knowledge base
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Response templates
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Email support
                </li>
              </ul>
              <Button className="w-full bg-slate-800 hover:bg-slate-700 text-white border border-emerald-500/30">
                Start Free Trial
              </Button>
            </Card>

            <Card className="bg-gradient-to-br from-emerald-900/50 to-green-900/50 border-emerald-500/50 p-6 shadow-lg shadow-emerald-500/20 scale-105">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-bold text-white">Professional</h3>
                <span className="bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded text-xs font-semibold">
                  POPULAR
                </span>
              </div>
              <div className="mb-4">
                <span className="text-4xl font-bold text-emerald-400">$199</span>
                <span className="text-lg text-gray-400">/month</span>
              </div>
              <div className="text-sm text-gray-400 mb-6">Up to 10 team members</div>
              <ul className="space-y-2 mb-6 text-sm min-h-[200px]">
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  2,000 tickets/month
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  All channels (8+)
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  Advanced AI routing + sentiment
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  Advanced knowledge base + AI articles
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  Smart response suggestions
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  SLA management
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  Advanced analytics
                </li>
                <li className="flex items-start text-gray-200">
                  <span className="text-emerald-400 mr-2">✓</span>
                  Priority support
                </li>
              </ul>
              <Button className="w-full bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white">
                Start Free Trial
              </Button>
            </Card>

            <Card className="bg-slate-900/50 border-slate-700 p-6">
              <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-gray-400">Custom</span>
              </div>
              <div className="text-sm text-gray-400 mb-6">Unlimited team members</div>
              <ul className="space-y-2 mb-6 text-sm min-h-[200px]">
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Unlimited tickets
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Custom channels
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Custom AI training
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  White-label support portal
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  SSO & advanced security
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Custom integrations
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  99.99% SLA
                </li>
                <li className="flex items-start text-gray-300">
                  <span className="text-green-400 mr-2">✓</span>
                  Dedicated account manager
                </li>
              </ul>
              <Button variant="outline" className="w-full border-gray-600 text-gray-400 hover:bg-slate-800">
                Contact Sales
              </Button>
            </Card>
          </div>
        </div>

        {/* Integrations */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Integrates With Your Stack</h2>

          <div className="flex flex-wrap gap-3 justify-center">
            {integrations.map((integration, idx) => (
              <div
                key={idx}
                className="bg-slate-900/50 border border-emerald-500/20 rounded-lg px-6 py-3 text-center hover:border-emerald-500/50 transition-all"
              >
                <div className="text-sm text-white font-medium">{integration}</div>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">How It Works</h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card className="bg-slate-900/50 border-emerald-500/30 p-6 text-center">
              <div className="text-5xl mb-4">📥</div>
              <div className="text-xl font-bold text-white mb-2">1. Ticket Arrives</div>
              <p className="text-sm text-gray-400">
                Customer reaches out via email, chat, social, or any channel
              </p>
            </Card>

            <Card className="bg-slate-900/50 border-emerald-500/30 p-6 text-center">
              <div className="text-5xl mb-4">🧠</div>
              <div className="text-xl font-bold text-white mb-2">2. AI Analyzes</div>
              <p className="text-sm text-gray-400">
                Helix AI categorizes, prioritizes, detects sentiment, and routes to right person
              </p>
            </Card>

            <Card className="bg-slate-900/50 border-emerald-500/30 p-6 text-center">
              <div className="text-5xl mb-4">💬</div>
              <div className="text-xl font-bold text-white mb-2">3. Agent Responds</div>
              <p className="text-sm text-gray-400">
                AI suggests responses from knowledge base. Agent reviews and sends
              </p>
            </Card>

            <Card className="bg-slate-900/50 border-emerald-500/30 p-6 text-center">
              <div className="text-5xl mb-4">✅</div>
              <div className="text-xl font-bold text-white mb-2">4. Customer Happy</div>
              <p className="text-sm text-gray-400">
                Fast resolution, tracked in analytics. System learns for next time
              </p>
            </Card>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-r from-emerald-900/30 to-green-900/30 rounded-2xl p-12 border border-emerald-500/30">
          <h2 className="text-4xl font-bold text-white mb-4">
            Turn Support Into a Superpower
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Resolve tickets 3x faster with AI. Make customers happier. Start your 14-day free trial.
          </p>
          <Button
            size="lg"
            className="bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-700 hover:to-green-700 text-white px-12"
          >
            Start Free Trial →
          </Button>
          <p className="text-sm text-gray-400 mt-4">No credit card required • Cancel anytime • 14-day money-back guarantee</p>
        </div>

      </div>
    </div>
  )
}
