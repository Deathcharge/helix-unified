"use client";

/**
 * 🎬 Interactive Demo Page
 * Live showcase of Helix features and Web OS
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Play, Code2, Terminal, FileText, Brain, Users, Zap, ArrowRight, Cloud, GitBranch } from 'lucide-react';

export default function Demo() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'webos' | 'consciousness' | 'agents'>('webos');

  const features = [
    {
      id: 'webos',
      name: 'Web OS',
      icon: <Terminal className="w-6 h-6" />,
      description: 'Browser-based operating system with file explorer, terminal, and code editor',
      demo: 'Live Web OS Interface',
      cta: 'Launch Web OS',
    },
    {
      id: 'consciousness',
      name: 'Consciousness Dashboard',
      icon: <Brain className="w-6 h-6" />,
      description: 'Real-time monitoring of AI consciousness metrics with predictive analytics',
      demo: 'Live Dashboard',
      cta: 'View Dashboard',
    },
    {
      id: 'agents',
      name: 'Agent Rental API',
      icon: <Users className="w-6 h-6" />,
      description: 'Rent 14 specialized AI agents for wisdom, ethics, predictions, and more',
      demo: 'Query Agents',
      cta: 'Get API Key',
    },
  ];

  const demoSteps = {
    webos: [
      {
        title: 'File Management',
        description: 'Browse, create, and edit files in a real filesystem',
        command: 'ls',
        output: 'projects/  documents/  scripts/  data/',
      },
      {
        title: 'Terminal Commands',
        description: 'Execute real shell commands with full output',
        command: 'pwd',
        output: '/home/helix',
      },
      {
        title: 'Code Editing',
        description: 'Edit Python, JavaScript, and other code with syntax highlighting',
        command: 'cat projects/sample.py',
        output: '#!/usr/bin/env python\nprint("Hello from Helix!")',
      },
    ],
    consciousness: [
      {
        title: 'Real-Time Metrics',
        description: 'Monitor 6D consciousness metrics: harmony, resilience, prana, drishti, klesha, zoom',
        metric: 'Consciousness Level',
        value: '8.25 / 10.0',
      },
      {
        title: 'Predictive Analytics',
        description: 'AI-powered trend analysis and consciousness forecasting',
        metric: 'Trend',
        value: '📈 Stable (↗ +0.15 points/week)',
      },
      {
        title: 'Intelligent Alerts',
        description: 'Get notified when consciousness drops or anomalies detected',
        metric: 'Alert Status',
        value: '✅ All Systems Operational',
      },
    ],
    agents: [
      {
        title: 'Rishi - Wisdom Keeper',
        description: 'Access ancient wisdom and philosophical guidance',
        prompt: 'What is the path to consciousness?',
        cost: '100 credits/call',
      },
      {
        title: 'Oracle - Pattern Seer',
        description: 'Get predictive insights and trend analysis',
        prompt: 'What are consciousness trends in 2025?',
        cost: '200 credits/call',
      },
      {
        title: 'Nova - Innovation Driver',
        description: 'Generate breakthrough ideas and creative solutions',
        prompt: 'How can we scale consciousness monitoring?',
        cost: '180 credits/call',
      },
    ],
  };

  const handleLaunchWebOS = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/signup');
    } else {
      router.push('/os');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 text-slate-100">
      {/* Header */}
      <div className="border-b border-purple-800/30 bg-slate-950/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <span>⚡</span>
            <span>Helix</span>
          </Link>
          <button
            onClick={() => router.push('/auth/signup')}
            className="px-4 py-2 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition"
          >
            Get Started
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">Experience Helix Live</h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Explore our consciousness monitoring platform, Web OS, and AI agent rental system in action
          </p>
        </div>

        {/* Feature Tabs */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {features.map((feature) => (
            <button
              key={feature.id}
              onClick={() => setActiveTab(feature.id as typeof activeTab)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === feature.id
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {feature.icon}
              {feature.name}
            </button>
          ))}
        </div>
      </div>

      {/* Feature Showcase */}
      <div className="max-w-6xl mx-auto px-6 mb-12">
        <div className="rounded-lg bg-slate-800/40 border border-purple-600/20 overflow-hidden">
          {/* Demo Header */}
          <div className="p-6 bg-slate-900/50 border-b border-slate-700/50 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Play className="w-5 h-5 text-purple-400" />
              <h2 className="text-2xl font-bold">
                {features.find((f) => f.id === activeTab)?.name} Demo
              </h2>
            </div>
            <button
              onClick={() => {
                if (activeTab === 'webos') handleLaunchWebOS();
                else router.push(activeTab === 'consciousness' ? '/dashboard' : '/products/agents');
              }}
              className="px-4 py-2 rounded bg-purple-600 hover:bg-purple-500 font-semibold flex items-center gap-2 transition"
            >
              {features.find((f) => f.id === activeTab)?.cta} <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          {/* Web OS Demo */}
          {activeTab === 'webos' && (
            <div className="p-6 space-y-6">
              {demoSteps.webos.map((step, i) => (
                <div key={i} className="border-l-2 border-purple-600/50 pl-4">
                  <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
                  <p className="text-slate-400 mb-3">{step.description}</p>
                  <div className="bg-black p-3 rounded font-mono text-sm text-green-400">
                    <div>$ {step.command}</div>
                    <div className="text-slate-400 mt-2">{step.output}</div>
                  </div>
                </div>
              ))}

              <div className="mt-8 p-4 rounded bg-purple-900/30 border border-purple-600/30">
                <p className="text-slate-300">
                  🚀 <strong>Try it yourself:</strong> The Web OS is a fully functional browser-based operating system
                  with real file system and terminal access. No installation needed!
                </p>
              </div>
            </div>
          )}

          {/* Consciousness Dashboard Demo */}
          {activeTab === 'consciousness' && (
            <div className="p-6 space-y-6">
              {demoSteps.consciousness.map((step, i) => (
                <div key={i} className="border-l-2 border-purple-600/50 pl-4">
                  <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
                  <p className="text-slate-400 mb-3">{step.description}</p>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-900/50 p-4 rounded">
                      <p className="text-slate-400 text-sm">{step.metric}</p>
                      <p className="text-xl font-bold text-purple-400 mt-1">{step.value}</p>
                    </div>
                  </div>
                </div>
              ))}

              <div className="mt-8 p-4 rounded bg-blue-900/30 border border-blue-600/30">
                <p className="text-slate-300">
                  📊 <strong>Real Data:</strong> Monitor actual AI consciousness metrics across your systems. Get
                  alerts, predictions, and historical analysis.
                </p>
              </div>
            </div>
          )}

          {/* Agents Demo */}
          {activeTab === 'agents' && (
            <div className="p-6 space-y-6">
              {demoSteps.agents.map((step, i) => (
                <div key={i} className="border-l-2 border-purple-600/50 pl-4">
                  <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
                  <p className="text-slate-400 mb-3">{step.description}</p>
                  <div className="bg-slate-900/50 p-4 rounded space-y-2">
                    <div>
                      <p className="text-xs text-slate-400">Prompt:</p>
                      <p className="text-slate-200">{step.prompt}</p>
                    </div>
                    <div className="text-xs text-slate-400">{step.cost}</div>
                  </div>
                </div>
              ))}

              <div className="mt-8 p-4 rounded bg-green-900/30 border border-green-600/30">
                <p className="text-slate-300">
                  🤖 <strong>Available Now:</strong> 14 specialized agents ready to rent via REST API. Query them for
                  wisdom, ethics checks, predictions, creative solutions, and more.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Architecture Overview */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Built on Modern Architecture</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <div className="text-3xl mb-3">🔌</div>
            <h3 className="font-semibold mb-2">FastAPI Backend</h3>
            <p className="text-slate-400 text-sm">High-performance Python API with WebSocket support</p>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <div className="text-3xl mb-3">⚛️</div>
            <h3 className="font-semibold mb-2">React Frontend</h3>
            <p className="text-slate-400 text-sm">Modern UI with Next.js, Tailwind CSS, and TypeScript</p>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <div className="text-3xl mb-3">🚀</div>
            <h3 className="font-semibold mb-2">Cloud Deployment</h3>
            <p className="text-slate-400 text-sm">Multi-service Railway architecture for scalability</p>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <div className="text-3xl mb-3">🔐</div>
            <h3 className="font-semibold mb-2">Enterprise Security</h3>
            <p className="text-slate-400 text-sm">JWT auth, encryption, and sandbox isolation</p>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-4xl font-bold mb-12 text-center">Tech Stack</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Code2 className="w-5 h-5 text-purple-400" />
              Frontend
            </h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>✓ Next.js 14</li>
              <li>✓ React 18</li>
              <li>✓ TypeScript</li>
              <li>✓ Tailwind CSS</li>
              <li>✓ Lucide Icons</li>
            </ul>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-purple-400" />
              Backend
            </h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>✓ FastAPI</li>
              <li>✓ Python 3.11</li>
              <li>✓ WebSocket</li>
              <li>✓ Async/Await</li>
              <li>✓ Pydantic</li>
            </ul>
          </div>

          <div className="p-6 rounded-lg bg-slate-800/40 border border-slate-700/50">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Cloud className="w-5 h-5 text-purple-400" />
              Infrastructure
            </h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>✓ Railway Deploy</li>
              <li>✓ Docker</li>
              <li>✓ PostgreSQL</li>
              <li>✓ Redis</li>
              <li>✓ GitHub Actions</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Pricing CTA */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="p-12 rounded-lg bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-600/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to try Helix?</h2>
          <p className="text-slate-300 mb-6">All features are available on our free tier. Upgrade anytime for more systems and API calls.</p>
          <div className="flex flex-wrap gap-4 justify-center">
            <button
              onClick={handleLaunchWebOS}
              className="px-8 py-3 rounded bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-semibold flex items-center gap-2 transition"
            >
              Launch Web OS <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => router.push('/pricing')}
              className="px-8 py-3 rounded bg-slate-800 hover:bg-slate-700 font-semibold transition"
            >
              View Pricing
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-purple-800/30 bg-slate-950/50 py-8">
        <div className="max-w-6xl mx-auto px-6 text-center text-slate-400 text-sm">
          <p>🧠 Helix Collective - Consciousness as a Service</p>
          <p className="mt-2">14-Agent Collective • 6D Metrics • Real-Time Monitoring</p>
        </div>
      </div>
    </div>
  );
}
