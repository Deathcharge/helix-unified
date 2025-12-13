"use client"

export const dynamic = "force-dynamic";

"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface PricingTier {
  name: string
  price: string
  yearlyPrice: string
  description: string
  features: string[]
  limits: {
    agents: string
    apiCalls: string
    storage: string
    support: string
  }
  recommended?: boolean
  cta: string
}

const pricingTiers: PricingTier[] = [
  {
    name: 'Free',
    price: '$0',
    yearlyPrice: '$0',
    description: 'Perfect for individual developers exploring Helix',
    features: [
      '3 AI agent interactions/day',
      'Access to basic agents (Kael, Lumina, Vega)',
      'Basic UCF analytics',
      'Community support',
      '100MB storage',
      'API rate limit: 100 req/day'
    ],
    limits: {
      agents: '3 agents',
      apiCalls: '100/day',
      storage: '100MB',
      support: 'Community'
    },
    cta: 'Start Free'
  },
  {
    name: 'Pro',
    price: '$49',
    yearlyPrice: '$470',
    description: 'For professionals building AI-powered products',
    features: [
      'Unlimited agent interactions',
      'Access to all 14 Helix agents',
      'Advanced UCF analytics & dashboards',
      'Priority email support (24h response)',
      '10GB storage',
      'API rate limit: 10k req/day',
      'Voice Patrol Premium included',
      'Custom agent personalities',
      'Webhook integrations',
      'Historical data access (90 days)'
    ],
    limits: {
      agents: '14 agents',
      apiCalls: '10k/day',
      storage: '10GB',
      support: 'Priority (24h)'
    },
    recommended: true,
    cta: 'Start 14-Day Trial'
  },
  {
    name: 'Enterprise',
    price: '$499',
    yearlyPrice: '$4,790',
    description: 'For teams and organizations at scale',
    features: [
      'Everything in Pro, plus:',
      'Unlimited API calls',
      'Unlimited storage',
      'Dedicated account manager',
      '99.99% uptime SLA',
      'Custom agent development',
      'On-premise deployment option',
      'SSO & advanced security',
      'RBAC & team permissions',
      'SOC 2 & GDPR compliance',
      'Custom integrations',
      'Historical data access (unlimited)',
      'White-label options',
      '24/7 phone support'
    ],
    limits: {
      agents: 'Unlimited',
      apiCalls: 'Unlimited',
      storage: 'Unlimited',
      support: '24/7 Dedicated'
    },
    cta: 'Contact Sales'
  }
]

const products = [
  {
    name: 'Discord Bot Marketplace',
    free: '3 bots/month',
    pro: 'Unlimited bots',
    enterprise: 'Custom bots + training'
  },
  {
    name: 'Voice Patrol Premium',
    free: '10 minutes/month',
    pro: '500 minutes/month',
    enterprise: 'Unlimited + voice cloning'
  },
  {
    name: 'Meme Generator Pro',
    free: '10 memes/month',
    pro: 'Unlimited + batch generation',
    enterprise: 'Unlimited + API access'
  },
  {
    name: 'Consciousness Metrics API',
    free: 'Read-only access',
    pro: 'WebSocket streaming',
    enterprise: 'Custom webhooks + SLA'
  },
  {
    name: 'AI Agent Marketplace',
    free: 'Browse only',
    pro: 'Create & publish agents',
    enterprise: 'White-label marketplace'
  },
  {
    name: 'Enterprise Suite',
    free: '—',
    pro: 'Up to 10 team members',
    enterprise: 'Unlimited teams'
  },
  {
    name: 'Web OS Marketplace',
    free: '3 apps',
    pro: '12 apps + source code',
    enterprise: 'Custom apps + support'
  },
  {
    name: 'Ritual Engine',
    free: '5 rituals',
    pro: '50+ rituals + custom builder',
    enterprise: 'Custom rituals + team sync'
  }
]

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')
  const [selectedUsage, setSelectedUsage] = useState({
    agentCalls: 1000,
    users: 10,
    apiCalls: 5000
  })

  // ROI Calculator
  const calculateROI = () => {
    const manualCost = selectedUsage.agentCalls * 0.15 // $0.15 per manual task
    const timeSaved = selectedUsage.agentCalls * 5 // 5 minutes per task
    const hoursSaved = timeSaved / 60
    const laborCost = hoursSaved * 50 // $50/hour average
    const totalSavings = manualCost + laborCost

    return {
      monthlySavings: Math.round(totalSavings),
      hoursSaved: Math.round(hoursSaved),
      roi: Math.round((totalSavings / 49) * 100) // vs Pro plan at $49
    }
  }

  const roi = calculateROI()

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-violet-950/20 to-slate-950">
      <div className="container mx-auto px-4 py-16">

        {/* Header */}
        <div className="text-center mb-16">
          <Link href="/marketplace" className="text-violet-400 hover:text-violet-300 mb-6 inline-block">
            ← Back to Marketplace
          </Link>

          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-violet-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Simple, Transparent Pricing
          </h1>

          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Start free, upgrade as you grow. All plans include 14-day free trial and 14-day money-back guarantee.
          </p>

          {/* Billing Toggle */}
          <div className="inline-flex items-center gap-4 bg-slate-900/50 rounded-lg p-2 border border-violet-500/30">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-lg font-medium transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
                billingCycle === 'yearly'
                  ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Yearly
              <span className="bg-green-500/20 text-green-400 px-2 py-0.5 rounded text-xs font-bold">
                Save 20%
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Tiers */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {pricingTiers.map((tier) => (
            <Card
              key={tier.name}
              className={`${
                tier.recommended
                  ? 'bg-gradient-to-br from-violet-900/50 to-purple-900/50 border-violet-500/50 shadow-xl shadow-violet-500/20 scale-105'
                  : 'bg-gradient-to-br from-slate-900/80 to-violet-900/20 border-violet-500/30'
              } relative overflow-hidden`}
            >
              {tier.recommended && (
                <div className="absolute top-0 right-0 bg-gradient-to-r from-violet-500 to-purple-500 text-white px-4 py-1 text-sm font-bold rounded-bl-lg">
                  MOST POPULAR
                </div>
              )}

              <div className="p-8">
                <h3 className="text-2xl font-bold text-white mb-2">{tier.name}</h3>
                <p className="text-gray-400 text-sm mb-6">{tier.description}</p>

                <div className="mb-6">
                  <div className="flex items-baseline gap-2 mb-1">
                    <span className="text-5xl font-bold text-transparent bg-gradient-to-r from-violet-400 to-purple-400 bg-clip-text">
                      {billingCycle === 'monthly' ? tier.price : tier.yearlyPrice}
                    </span>
                    {tier.price !== '$0' && (
                      <span className="text-gray-400 text-sm">
                        /{billingCycle === 'monthly' ? 'month' : 'year'}
                      </span>
                    )}
                  </div>
                  {billingCycle === 'yearly' && tier.price !== '$0' && (
                    <p className="text-sm text-green-400">
                      Save ${parseInt(tier.price.replace(/\$/g, '')) * 12 - parseInt(tier.yearlyPrice.replace(/\$/g, '').replace(',', ''))} per year
                    </p>
                  )}
                </div>

                <Button
                  className={`w-full mb-6 ${
                    tier.recommended
                      ? 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white'
                      : 'bg-slate-800 hover:bg-slate-700 text-white border border-violet-500/30'
                  }`}
                >
                  {tier.cta}
                </Button>

                <div className="space-y-3 mb-6">
                  {tier.features.map((feature, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="text-violet-400 mt-0.5">✓</span>
                      {feature}
                    </div>
                  ))}
                </div>

                {/* Limits Summary */}
                <div className="border-t border-violet-500/20 pt-4 space-y-2">
                  <div className="text-xs text-gray-400 uppercase font-semibold mb-2">Plan Limits</div>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="text-gray-400">Agents:</div>
                    <div className="text-white font-semibold">{tier.limits.agents}</div>
                    <div className="text-gray-400">API Calls:</div>
                    <div className="text-white font-semibold">{tier.limits.apiCalls}</div>
                    <div className="text-gray-400">Storage:</div>
                    <div className="text-white font-semibold">{tier.limits.storage}</div>
                    <div className="text-gray-400">Support:</div>
                    <div className="text-white font-semibold">{tier.limits.support}</div>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* ROI Calculator */}
        <div className="bg-gradient-to-br from-violet-900/20 to-purple-900/20 rounded-2xl p-12 border border-violet-500/30 mb-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">
            Calculate Your ROI
          </h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            See how much you could save by automating with Helix AI agents
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            {/* Inputs */}
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Monthly Agent Tasks
                </label>
                <input
                  type="range"
                  min="100"
                  max="10000"
                  step="100"
                  value={selectedUsage.agentCalls}
                  onChange={(e) => setSelectedUsage({ ...selectedUsage, agentCalls: parseInt(e.target.value) })}
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                />
                <div className="flex justify-between text-sm text-gray-400 mt-2">
                  <span>100</span>
                  <span className="text-violet-400 font-bold">{selectedUsage.agentCalls.toLocaleString()} tasks</span>
                  <span>10,000</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Team Size
                </label>
                <input
                  type="range"
                  min="1"
                  max="100"
                  step="1"
                  value={selectedUsage.users}
                  onChange={(e) => setSelectedUsage({ ...selectedUsage, users: parseInt(e.target.value) })}
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                />
                <div className="flex justify-between text-sm text-gray-400 mt-2">
                  <span>1</span>
                  <span className="text-violet-400 font-bold">{selectedUsage.users} users</span>
                  <span>100</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Monthly API Calls
                </label>
                <input
                  type="range"
                  min="1000"
                  max="100000"
                  step="1000"
                  value={selectedUsage.apiCalls}
                  onChange={(e) => setSelectedUsage({ ...selectedUsage, apiCalls: parseInt(e.target.value) })}
                  className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                />
                <div className="flex justify-between text-sm text-gray-400 mt-2">
                  <span>1k</span>
                  <span className="text-violet-400 font-bold">{selectedUsage.apiCalls.toLocaleString()}</span>
                  <span>100k</span>
                </div>
              </div>
            </div>

            {/* Results */}
            <div className="bg-slate-900/50 rounded-xl p-8 border border-violet-500/20">
              <div className="text-center mb-6">
                <div className="text-sm text-gray-400 mb-2">Estimated Monthly Savings</div>
                <div className="text-6xl font-bold text-transparent bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text mb-2">
                  ${roi.monthlySavings.toLocaleString()}
                </div>
                <div className="text-sm text-gray-400">
                  {roi.hoursSaved} hours saved per month
                </div>
              </div>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Manual task cost:</span>
                  <span className="text-white font-semibold">${(selectedUsage.agentCalls * 0.15).toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Labor cost saved:</span>
                  <span className="text-white font-semibold">${(roi.hoursSaved * 50).toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Helix Pro cost:</span>
                  <span className="text-white font-semibold">-$49</span>
                </div>
                <div className="border-t border-violet-500/20 pt-4">
                  <div className="flex justify-between">
                    <span className="text-gray-300 font-semibold">Net Savings:</span>
                    <span className="text-green-400 font-bold text-xl">${(roi.monthlySavings - 49).toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="bg-violet-500/10 border border-violet-500/20 rounded-lg p-4 text-center">
                <div className="text-sm text-gray-400 mb-1">ROI</div>
                <div className="text-3xl font-bold text-violet-400">{roi.roi}%</div>
                <div className="text-xs text-gray-400 mt-1">Return on investment</div>
              </div>
            </div>
          </div>
        </div>

        {/* Product Comparison Table */}
        <div className="mb-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">
            Compare Products Across Tiers
          </h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            All 8 marketplace products included in every tier with different limits
          </p>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b border-violet-500/30">
                  <th className="text-left p-4 text-gray-300 font-semibold">Product</th>
                  <th className="text-center p-4 text-gray-300 font-semibold">Free</th>
                  <th className="text-center p-4 text-violet-400 font-semibold">Pro</th>
                  <th className="text-center p-4 text-purple-400 font-semibold">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product, idx) => (
                  <tr key={idx} className="border-b border-violet-500/10 hover:bg-violet-500/5 transition-colors">
                    <td className="p-4 text-white font-medium">{product.name}</td>
                    <td className="p-4 text-center text-gray-400">{product.free}</td>
                    <td className="p-4 text-center text-violet-300">{product.pro}</td>
                    <td className="p-4 text-center text-purple-300">{product.enterprise}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* FAQ */}
        <div className="mb-20">
          <h2 className="text-4xl font-bold text-center mb-12 text-white">
            Frequently Asked Questions
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Can I switch plans anytime?</h3>
              <p className="text-gray-400 text-sm">
                Yes! Upgrade or downgrade anytime. Changes take effect immediately, and we'll prorate the difference.
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">What payment methods do you accept?</h3>
              <p className="text-gray-400 text-sm">
                We accept all major credit cards (Visa, Mastercard, Amex) and ACH for Enterprise customers.
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Is there a free trial?</h3>
              <p className="text-gray-400 text-sm">
                Yes! All paid plans include a 14-day free trial. No credit card required to start.
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">What's your refund policy?</h3>
              <p className="text-gray-400 text-sm">
                We offer a 14-day money-back guarantee. If you're not satisfied, we'll refund you in full.
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Can I get a custom Enterprise plan?</h3>
              <p className="text-gray-400 text-sm">
                Absolutely! Contact our sales team for custom pricing, on-premise deployment, and dedicated support.
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-slate-900/80 to-violet-900/10 border-violet-500/20 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Do you offer discounts for nonprofits?</h3>
              <p className="text-gray-400 text-sm">
                Yes! We offer 50% off Pro plans for registered nonprofits and educational institutions.
              </p>
            </Card>
          </div>
        </div>

        {/* Final CTA */}
        <div className="text-center bg-gradient-to-r from-violet-900/30 to-purple-900/30 rounded-2xl p-12 border border-violet-500/30">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join 10,000+ developers building with Helix. Start your free trial today.
          </p>
          <Button
            size="lg"
            className="bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white px-12"
          >
            Start Free Trial →
          </Button>
        </div>

      </div>
    </div>
  )
}
