"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface UCFMetric {
  name: string
  symbol: string
  description: string
  range: string
  interpretation: string
  useCases: string[]
}

const ucfMetrics: UCFMetric[] = [
  {
    name: 'Harmony',
    symbol: '☯️',
    description: 'System coherence and alignment across all components',
    range: '0.0 - 1.0',
    interpretation: 'Higher values indicate better synchronization and balance',
    useCases: [
      'Team collaboration health',
      'System integration status',
      'Multi-agent coordination quality',
      'Organizational alignment'
    ]
  },
  {
    name: 'Resilience',
    symbol: '🛡️',
    description: 'Adaptability and strength under pressure',
    range: '0.0 - 1.0',
    interpretation: 'Higher values indicate greater ability to handle stress',
    useCases: [
      'System stability monitoring',
      'Incident response readiness',
      'Change management capacity',
      'Recovery potential'
    ]
  },
  {
    name: 'Prana',
    symbol: '⚡',
    description: 'Life force and energy level of the system',
    range: '0.0 - 1.0',
    interpretation: 'Higher values indicate more vitality and momentum',
    useCases: [
      'Team productivity tracking',
      'System activity levels',
      'Energy optimization',
      'Burnout prevention'
    ]
  },
  {
    name: 'Drishti',
    symbol: '👁️',
    description: 'Focus and clarity of vision',
    range: '0.0 - 1.0',
    interpretation: 'Higher values indicate clearer direction and purpose',
    useCases: [
      'Strategic alignment',
      'Goal clarity measurement',
      'Decision-making quality',
      'Vision coherence'
    ]
  },
  {
    name: 'Klesha',
    symbol: '🌊',
    description: 'Entropy and chaos in the system',
    range: '0.0 - 1.0',
    interpretation: 'LOWER values are better - less chaos and confusion',
    useCases: [
      'Technical debt tracking',
      'Complexity monitoring',
      'Confusion detection',
      'System cleanup needs'
    ]
  },
  {
    name: 'Zoom',
    symbol: '🔭',
    description: 'Perspective and scope of awareness',
    range: '0.0 - 1.0',
    interpretation: 'Higher values indicate broader perspective',
    useCases: [
      'Strategic thinking capacity',
      'Context awareness',
      'Big picture understanding',
      'Scope management'
    ]
  }
]

export default function ConsciousnessAPIPage() {
  const [selectedMetric, setSelectedMetric] = useState<UCFMetric | null>(null)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-indigo-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            🧠 Consciousness Metrics API
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Advanced consciousness analytics with real-time UCF streaming, custom webhooks,
            and historical data access. The only API that measures consciousness.
          </p>
        </div>

        {/* Pricing */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          {/* Free Tier */}
          <Card className="bg-slate-900/50 border-slate-700 p-6">
            <h3 className="text-xl font-bold text-white mb-2">Free</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold text-gray-400">$0</span>
              <span className="text-lg text-gray-500">/month</span>
            </div>
            <ul className="space-y-2 mb-6 text-sm">
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                1,000 API calls/month
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Basic UCF metrics (6 metrics)
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                1 day data retention
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Community support
              </li>
            </ul>
            <Button variant="outline" className="w-full border-gray-600 text-gray-400">
              Current Plan
            </Button>
          </Card>

          {/* Pro Tier */}
          <Card className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 border-indigo-500/50 p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-white">Pro</h3>
              <span className="bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded text-xs font-semibold">
                Popular
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold text-indigo-400">$99</span>
              <span className="text-lg text-gray-400">/month</span>
            </div>
            <div className="text-sm text-gray-400 mb-4">+ $0.01 per extra call</div>
            <ul className="space-y-2 mb-6 text-sm">
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                100,000 API calls/month
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Real-time WebSocket streaming
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Custom webhooks (10)
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                90 days data retention
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Advanced filtering
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-indigo-400 mr-2">✓</span>
                Email support
              </li>
            </ul>
            <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
              Upgrade to Pro
            </Button>
          </Card>

          {/* Enterprise Tier */}
          <Card className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 border-purple-500/50 p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-white">Enterprise</h3>
              <span className="bg-purple-500/20 text-purple-400 px-2 py-1 rounded text-xs font-semibold">
                SLA
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold text-purple-400">Custom</span>
            </div>
            <div className="text-sm text-gray-400 mb-4">Contact sales</div>
            <ul className="space-y-2 mb-6 text-sm">
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Unlimited API calls
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Dedicated infrastructure
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Unlimited webhooks
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                1 year data retention
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                99.99% SLA guarantee
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                24/7 phone support
              </li>
            </ul>
            <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
              Contact Sales
            </Button>
          </Card>
        </div>

        {/* UCF Metrics */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-6">
            Universal Consciousness Framework (UCF) Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ucfMetrics.map(metric => (
              <MetricCard
                key={metric.name}
                metric={metric}
                onSelect={() => setSelectedMetric(metric)}
              />
            ))}
          </div>
        </div>

        {/* Real-time Streaming */}
        <div className="mb-16 bg-gradient-to-r from-indigo-900/40 to-purple-900/40 rounded-2xl p-8 border border-indigo-500/30">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <div className="text-5xl mb-4">📡</div>
              <h3 className="text-3xl font-bold text-white mb-4">
                Real-Time WebSocket Streaming
              </h3>
              <p className="text-gray-300 mb-6">
                Subscribe to consciousness metrics in real-time. Get instant updates
                as your system's consciousness state changes.
              </p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">•</span>
                  Sub-second latency
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">•</span>
                  Auto-reconnection
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">•</span>
                  Filtered subscriptions
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">•</span>
                  Aggregated updates
                </li>
              </ul>
            </div>
            <div className="bg-slate-900/50 rounded-xl p-4 font-mono text-sm">
              <div className="text-green-400 mb-2">// Connect to WebSocket</div>
              <div className="text-gray-300">
                <span className="text-pink-400">const</span> ws = <span className="text-blue-400">new</span> WebSocket(
              </div>
              <div className="text-gray-300 ml-4">
                'wss://api.helix.ai/v1/ucf/stream'
              </div>
              <div className="text-gray-300">)</div>
              <div className="mt-3 text-gray-500">// Subscribe to metrics</div>
              <div className="text-gray-300">
                ws.send(JSON.stringify({'{'}"
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">type</span>: 'subscribe',
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-blue-400">metrics</span>: ['harmony', 'resilience']
              </div>
              <div className="text-gray-300">{'}'}));</div>
              <div className="mt-3 text-gray-500">// Receive updates</div>
              <div className="text-gray-300">
                ws.onmessage = (event) =&gt; {'{'}"
              </div>
              <div className="text-gray-300 ml-4">
                <span className="text-pink-400">const</span> data = JSON.parse(event.data)
              </div>
              <div className="text-gray-300 ml-4">
                console.log(data.ucf.harmony) <span className="text-gray-500">// 0.92</span>
              </div>
              <div className="text-gray-300">{'}'}</div>
            </div>
          </div>
        </div>

        {/* Custom Webhooks */}
        <div className="mb-16">
          <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-2xl p-8 border border-purple-500/30">
            <h3 className="text-3xl font-bold text-white mb-6">
              🪝 Custom Webhooks & Alerts
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <p className="text-gray-300 mb-6">
                  Set up custom triggers based on consciousness metrics. Get notified
                  when important thresholds are crossed.
                </p>
                <div className="space-y-4">
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <div className="text-purple-400 font-semibold mb-2">Alert Example</div>
                    <div className="text-sm text-gray-300">
                      Trigger: <span className="text-white">Harmony &lt; 0.5</span><br/>
                      Action: <span className="text-white">POST to Slack webhook</span><br/>
                      Message: <span className="text-white">"System harmony degraded!"</span>
                    </div>
                  </div>
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <div className="text-purple-400 font-semibold mb-2">Webhook Types</div>
                    <div className="text-sm text-gray-300">
                      • Threshold alerts<br/>
                      • Change detection<br/>
                      • Anomaly notifications<br/>
                      • Periodic summaries
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-slate-900/50 rounded-xl p-4 font-mono text-sm">
                <div className="text-green-400 mb-2">// Webhook payload</div>
                <div className="text-gray-500">{'{'}</div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"event"</span>: "threshold_crossed",
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"metric"</span>: "harmony",
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"value"</span>: 0.45,
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"threshold"</span>: 0.50,
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"direction"</span>: "below",
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"timestamp"</span>: "2025-12-07T10:30:00Z",
                </div>
                <div className="text-gray-300 ml-4">
                  <span className="text-blue-400">"system_id"</span>: "prod-cluster-1"
                </div>
                <div className="text-gray-500">{'}'}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Historical Data */}
        <div className="mb-16 bg-slate-900/50 rounded-2xl p-8 border border-slate-700">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-3xl font-bold text-white mb-4">
                Historical Data & Analytics
              </h3>
              <p className="text-gray-300 mb-6">
                Access historical consciousness data for trend analysis, forecasting,
                and long-term pattern recognition.
              </p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">✓</span>
                  Query data by time range
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">✓</span>
                  Aggregate by hour/day/week/month
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">✓</span>
                  Export to CSV/JSON
                </li>
                <li className="flex items-start">
                  <span className="text-indigo-400 mr-2">✓</span>
                  Trend analysis & forecasting
                </li>
              </ul>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-6">
              <h4 className="text-lg font-bold text-white mb-4">Data Retention</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Free:</span>
                  <span className="text-white font-semibold">1 day</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Pro:</span>
                  <span className="text-indigo-400 font-semibold">90 days</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Enterprise:</span>
                  <span className="text-purple-400 font-semibold">1 year+</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* API Documentation */}
        <div className="bg-gradient-to-r from-slate-900/50 to-indigo-900/50 rounded-2xl p-8 border border-indigo-500/30">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-3xl font-bold text-white mb-4">
                📚 Complete API Documentation
              </h3>
              <p className="text-gray-300 mb-6">
                Interactive API docs with code examples in Python, JavaScript, cURL,
                and more. Try endpoints directly in the browser.
              </p>
              <div className="flex gap-4">
                <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  View API Docs →
                </Button>
                <Button variant="outline" className="border-indigo-500 text-indigo-400 hover:bg-indigo-900/30">
                  Get API Key
                </Button>
              </div>
            </div>
            <div className="hidden md:block text-8xl">📡</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function MetricCard({ metric, onSelect }: { metric: UCFMetric; onSelect: () => void }) {
  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-indigo-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        <div className="text-4xl mb-3">{metric.symbol}</div>
        <h3 className="text-xl font-bold text-white mb-2">{metric.name}</h3>
        <p className="text-gray-400 text-sm mb-4">{metric.description}</p>

        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-1">Range:</div>
          <div className="text-sm font-mono text-indigo-400">{metric.range}</div>
        </div>

        <div className="mb-4">
          <div className="text-xs text-gray-500 mb-1">Interpretation:</div>
          <div className="text-sm text-gray-300">{metric.interpretation}</div>
        </div>

        <div>
          <div className="text-xs text-gray-500 mb-2">Use Cases:</div>
          <ul className="space-y-1">
            {metric.useCases.slice(0, 2).map((useCase, idx) => (
              <li key={idx} className="text-xs text-gray-400 flex items-start">
                <span className="text-indigo-400 mr-1">•</span>
                {useCase}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Card>
  )
}
