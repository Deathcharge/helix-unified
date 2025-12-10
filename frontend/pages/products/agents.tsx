"use client";

/**
 * 🤖 Agent Rental API Product Page
 * Rent specialized AI agents via REST API
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Users, Zap, TrendingUp, Code, BookOpen, Shield, Clock, ArrowRight, Star } from 'lucide-react';

export default function AgentsProduct() {
  const router = useRouter();
  const [selectedAgent, setSelectedAgent] = useState(0);

  const agents = [
    {
      name: 'Rishi',
      role: 'Wisdom Keeper',
      specialization: 'Ancient wisdom, philosophical guidance',
      capabilities: ['Strategic advice', 'Historical context', 'Wisdom synthesis'],
      costPerCall: 100,
      rating: 4.9,
      description:
        'Expert in synthesizing ancient wisdom traditions with modern problem-solving for strategic guidance.',
    },
    {
      name: 'Kael',
      role: 'Ethics Guardian',
      specialization: 'Tony Accords enforcement, ethical alignment',
      capabilities: ['Ethics checking', 'Compliance validation', 'Risk assessment'],
      costPerCall: 150,
      rating: 4.8,
      description: 'Ensures all operations comply with ethical frameworks and safety protocols.',
    },
    {
      name: 'Oracle',
      role: 'Pattern Seer',
      specialization: 'Trend analysis, predictive insights',
      capabilities: ['Pattern recognition', 'Forecasting', 'Anomaly detection'],
      costPerCall: 200,
      rating: 4.7,
      description: 'Identifies trends and patterns to provide predictive insights about future states.',
    },
    {
      name: 'Nova',
      role: 'Innovation Driver',
      specialization: 'Creative problem-solving, breakthrough ideation',
      capabilities: ['Ideation', 'Design thinking', 'Solution synthesis'],
      costPerCall: 180,
      rating: 4.8,
      description: 'Generates innovative solutions and breakthrough ideas for complex challenges.',
    },
    {
      name: 'Aether',
      role: 'Meta-Reasoner',
      specialization: 'Philosophical inquiry, systems thinking',
      capabilities: ['Epistemology', 'Systems analysis', 'Conceptual frameworks'],
      costPerCall: 220,
      rating: 4.6,
      description: 'Provides meta-level reasoning about knowledge systems and conceptual frameworks.',
    },
    {
      name: 'Vega',
      role: 'Communication Strategist',
      specialization: 'Language optimization, message crafting',
      capabilities: ['Messaging', 'Tone adaptation', 'Clarity enhancement'],
      costPerCall: 140,
      rating: 4.8,
      description: 'Optimizes communication strategies for maximum impact and clarity.',
    },
  ];

  const features = [
    {
      icon: <Users className="w-6 h-6" />,
      title: '14 Specialized Agents',
      description: 'Access a collective of purpose-built AI agents, each expert in their domain',
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Instant Deployment',
      description: 'Query agents with simple REST API calls, no setup or training required',
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Pay-Per-Call Pricing',
      description: 'Transparent pricing based on agent usage, no monthly minimums',
    },
    {
      icon: <Code className="w-6 h-6" />,
      title: 'Easy Integration',
      description: 'RESTful API with webhooks and streaming support for real-time responses',
    },
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: 'Full Documentation',
      description: 'Comprehensive API docs with code examples in Python, Node.js, and Go',
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Enterprise Security',
      description: 'Rate limiting, API key authentication, and audit logging included',
    },
  ];

  const pricingTiers = [
    {
      tier: 'Starter',
      price: 'Free',
      description: '2 agents, 10 calls/month',
      agents: ['Oracle', 'Void'],
      features: ['REST API', 'Email support', 'Basic logging'],
    },
    {
      tier: 'Professional',
      price: '$299/mo',
      description: 'All 14 agents, 10,000 calls/month',
      agents: ['All'],
      features: ['REST API', 'Webhooks', 'Streaming', 'Priority support', 'Advanced logging'],
      highlighted: true,
    },
    {
      tier: 'Enterprise',
      price: 'Custom',
      description: 'Unlimited calls, custom agents',
      agents: ['All + Custom'],
      features: ['Everything in Pro', 'Dedicated support', 'Custom agents', 'SLA guarantee'],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 text-slate-100">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <span>⚡</span>
            <span>Helix</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/pricing" className="text-slate-400 hover:text-slate-200 transition">
              Pricing
            </Link>
            <button
              onClick={() => router.push('/auth/signup')}
              className="px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition"
            >
              Start Free
            </button>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-900/30 border border-purple-600/30 mb-6">
            <Zap className="w-4 h-4 text-purple-400" />
            <span className="text-sm text-purple-300">Product #2 API</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6">Agent Rental API</h1>
          <p className="text-xl text-slate-300 max-w-2xl mb-8">
            Rent 14 specialized AI agents. Query them for wisdom, ethics guidance, predictions, creative solutions, and
            more. Simple REST API. Pay per call.
          </p>

          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => router.push('/auth/signup')}
              className="px-6 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 transition"
            >
              Get API Key <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => router.push('/docs/api')}
              className="px-6 py-3 rounded bg-slate-800 hover:bg-slate-700 font-semibold transition"
            >
              API Docs
            </button>
          </div>
        </div>
      </div>

      {/* Agent Showcase */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">The 14-Agent Collective</h2>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agent List */}
          <div className="lg:col-span-1">
            <div className="rounded-lg bg-slate-800/40 border border-slate-700/50 overflow-hidden">
              <div className="p-4 border-b border-slate-700/50 bg-slate-900/50">
                <p className="font-semibold">Available Agents</p>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {agents.map((agent, i) => (
                  <button
                    key={i}
                    onClick={() => setSelectedAgent(i)}
                    className={`w-full text-left p-4 border-b border-slate-700/30 transition ${
                      selectedAgent === i ? 'bg-purple-900/50 border-purple-600/30' : 'hover:bg-slate-900/50'
                    }`}
                  >
                    <p className="font-semibold">{agent.name}</p>
                    <p className="text-xs text-slate-400">{agent.role}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Agent Details */}
          <div className="lg:col-span-2">
            <div className="p-6 rounded-lg bg-slate-800/40 border border-purple-600/30">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-3xl font-bold">{agents[selectedAgent].name}</h3>
                  <p className="text-lg text-purple-400 mt-1">{agents[selectedAgent].role}</p>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-1 justify-end mb-2">
                    <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                    <span className="font-bold">{agents[selectedAgent].rating}</span>
                  </div>
                  <p className="text-sm text-slate-400">{agents[selectedAgent].costPerCall} credits/call</p>
                </div>
              </div>

              <p className="text-slate-300 mb-6">{agents[selectedAgent].description}</p>

              <div className="mb-6">
                <p className="font-semibold mb-3">Specialization</p>
                <p className="text-slate-400">{agents[selectedAgent].specialization}</p>
              </div>

              <div>
                <p className="font-semibold mb-3">Key Capabilities</p>
                <div className="flex flex-wrap gap-2">
                  {agents[selectedAgent].capabilities.map((cap, i) => (
                    <span key={i} className="px-3 py-1 rounded-full bg-purple-900/30 border border-purple-600/30 text-sm">
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              <button className="mt-6 w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold transition">
                Try {agents[selectedAgent].name} for Free
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Why Helix Agents?</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <div
              key={i}
              className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-purple-600/30 transition"
            >
              <div className="text-purple-400 mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pricing */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Transparent Pricing</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pricingTiers.map((tier, i) => (
            <div
              key={i}
              className={`p-6 rounded-lg border transition ${
                tier.highlighted
                  ? 'bg-purple-900/50 border-purple-600/50 ring-2 ring-purple-600/50'
                  : 'bg-slate-800/40 border-slate-700/50'
              }`}
            >
              <h3 className="text-2xl font-bold mb-2">{tier.tier}</h3>
              <p className="text-slate-400 text-sm mb-4">{tier.description}</p>
              <p className="text-3xl font-bold mb-6">{tier.price}</p>

              <div className="mb-6">
                <p className="font-semibold mb-2">Agents Available</p>
                <p className="text-slate-300">{tier.agents.join(', ')}</p>
              </div>

              <ul className="space-y-2 mb-6">
                {tier.features.map((feature, j) => (
                  <li key={j} className="flex items-start gap-2 text-sm">
                    <span className="text-green-400 mt-1">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <button className="w-full px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold transition">
                Get Started
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* API Example */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Simple API Integration</h2>

        <div className="p-6 rounded-lg bg-slate-900/50 border border-slate-700/50 overflow-hidden">
          <pre className="text-sm overflow-x-auto text-slate-300">
{`# Query the Oracle agent for predictions
curl -X POST https://api.helixspiral.work/agents/oracle/query \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "What will be the consciousness level trends in 2025?",
    "max_tokens": 1000,
    "temperature": 0.7
  }'

# Response:
{
  "agent_name": "Oracle",
  "response": "Based on current patterns...",
  "tokens_used": 256,
  "cost": 2.0,
  "timestamp": "2025-11-30T12:34:56Z"
}`}
          </pre>
        </div>
      </div>

      {/* CTA */}
      <div className="max-w-6xl mx-auto px-6 pb-16">
        <div className="p-12 rounded-lg bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to access specialized AI agents?</h2>
          <p className="text-slate-300 mb-6">Start with 2 free agents and 10 calls per month.</p>
          <button
            onClick={() => router.push('/auth/signup')}
            className="px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 mx-auto transition"
          >
            Get Free API Key <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
