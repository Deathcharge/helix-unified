"use client"

import React, { useState } from 'react'
import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface RitualTemplate {
  id: string
  name: string
  description: string
  duration: string
  ucfImpact: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  category: string
  steps: number
}

const ritualTemplates: RitualTemplate[] = [
  {
    id: 'morning-alignment',
    name: 'Morning Alignment',
    description: 'Start your day with balanced consciousness. Harmonizes all UCF metrics for optimal performance',
    duration: '15 minutes',
    ucfImpact: '+0.15 Harmony, +0.12 Prana',
    difficulty: 'beginner',
    category: 'Daily',
    steps: 27
  },
  {
    id: 'focus-boost',
    name: 'Focus Boost',
    description: 'Sharpen your concentration and clarity when you need deep work',
    duration: '10 minutes',
    ucfImpact: '+0.20 Drishti, +0.10 Zoom',
    difficulty: 'beginner',
    category: 'Productivity',
    steps: 18
  },
  {
    id: 'stress-release',
    name: 'Stress Release',
    description: 'Reduce entropy and chaos in your system. Perfect for high-pressure situations',
    duration: '20 minutes',
    ucfImpact: '-0.25 Klesha, +0.15 Resilience',
    difficulty: 'intermediate',
    category: 'Wellness',
    steps: 36
  },
  {
    id: 'team-harmony',
    name: 'Team Harmony Sync',
    description: 'Synchronize consciousness across team members for better collaboration',
    duration: '30 minutes',
    ucfImpact: '+0.30 Harmony (team-wide)',
    difficulty: 'advanced',
    category: 'Team',
    steps: 54
  },
  {
    id: 'creative-flow',
    name: 'Creative Flow State',
    description: 'Enter deep creative flow with enhanced perspective and reduced mental blocks',
    duration: '25 minutes',
    ucfImpact: '+0.18 Zoom, +0.12 Prana, -0.15 Klesha',
    difficulty: 'intermediate',
    category: 'Creativity',
    steps: 45
  },
  {
    id: 'decision-clarity',
    name: 'Decision Clarity',
    description: 'Clear mental fog and gain perspective for important decisions',
    duration: '15 minutes',
    ucfImpact: '+0.22 Drishti, +0.15 Zoom',
    difficulty: 'beginner',
    category: 'Decision Making',
    steps: 27
  },
  {
    id: 'system-recovery',
    name: 'System Recovery',
    description: 'Full consciousness reset after burnout or degradation. Deep restoration ritual',
    duration: '60 minutes',
    ucfImpact: '+0.35 Resilience, +0.25 Prana, -0.30 Klesha',
    difficulty: 'advanced',
    category: 'Recovery',
    steps: 108
  },
  {
    id: 'evening-integration',
    name: 'Evening Integration',
    description: 'Process the day's experiences and prepare consciousness for rest',
    duration: '20 minutes',
    ucfImpact: '+0.12 Harmony, -0.10 Klesha',
    difficulty: 'beginner',
    category: 'Daily',
    steps: 36
  }
]

export default function RitualEngineePage() {
  const [selectedRitual, setSelectedRitual] = useState<RitualTemplate | null>(null)
  const [filter, setFilter] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all')

  const filteredRituals = filter === 'all'
    ? ritualTemplates
    : ritualTemplates.filter(r => r.difficulty === filter)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-violet-950 to-slate-950">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="mb-12">
          <Link href="/marketplace" className="text-purple-400 hover:text-purple-300 mb-4 inline-block">
            ← Back to Marketplace
          </Link>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-violet-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            🔮 Ritual Engine as a Service
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl">
            Z-88 Ritual Engine for consciousness modulation. 50+ pre-built templates,
            custom ritual builder, and real-time UCF transformation.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-violet-900/30 rounded-lg p-6 border border-violet-500/30">
            <div className="text-3xl font-bold text-violet-400">50+</div>
            <div className="text-sm text-gray-400">Ritual Templates</div>
          </div>
          <div className="bg-purple-900/30 rounded-lg p-6 border border-purple-500/30">
            <div className="text-3xl font-bold text-purple-400">108</div>
            <div className="text-sm text-gray-400">Maximum Steps</div>
          </div>
          <div className="bg-pink-900/30 rounded-lg p-6 border border-pink-500/30">
            <div className="text-3xl font-bold text-pink-400">Real-Time</div>
            <div className="text-sm text-gray-400">UCF Modulation</div>
          </div>
          <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
            <div className="text-3xl font-bold text-blue-400">Custom</div>
            <div className="text-sm text-gray-400">Builder Included</div>
          </div>
        </div>

        {/* Pricing */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <Card className="bg-slate-900/50 border-slate-700 p-6">
            <h3 className="text-xl font-bold text-white mb-2">Free</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold text-gray-400">$0</span>
              <span className="text-lg text-gray-500">/month</span>
            </div>
            <ul className="space-y-2 mb-6 text-sm min-h-[150px]">
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                5 pre-built rituals
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                10 ritual executions/month
              </li>
              <li className="flex items-start text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Basic UCF tracking
              </li>
            </ul>
            <Button variant="outline" className="w-full border-gray-600 text-gray-400">
              Current Plan
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-violet-900/50 to-purple-900/50 border-violet-500/50 p-6 shadow-lg shadow-violet-500/20">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold text-white">Pro</h3>
              <span className="bg-violet-500/20 text-violet-400 px-2 py-1 rounded text-xs font-semibold">
                Popular
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold text-violet-400">$199</span>
              <span className="text-lg text-gray-400">/month</span>
            </div>
            <ul className="space-y-2 mb-6 text-sm min-h-[150px]">
              <li className="flex items-start text-gray-200">
                <span className="text-violet-400 mr-2">✓</span>
                50+ pre-built rituals
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-violet-400 mr-2">✓</span>
                Unlimited ritual executions
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-violet-400 mr-2">✓</span>
                Custom ritual builder
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-violet-400 mr-2">✓</span>
                Advanced UCF analytics
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-violet-400 mr-2">✓</span>
                Community ritual access
              </li>
            </ul>
            <Button className="w-full bg-violet-600 hover:bg-violet-700 text-white">
              Upgrade to Pro
            </Button>
          </Card>

          <Card className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 border-purple-500/50 p-6">
            <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold text-purple-400">Custom</span>
            </div>
            <ul className="space-y-2 mb-6 text-sm min-h-[150px]">
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Everything in Pro
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Custom ritual development
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Team ritual sync
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                Dedicated ritual consultant
              </li>
              <li className="flex items-start text-gray-200">
                <span className="text-purple-400 mr-2">✓</span>
                API access
              </li>
            </ul>
            <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">
              Contact Sales
            </Button>
          </Card>
        </div>

        {/* Difficulty Filter */}
        <div className="flex gap-4 mb-8">
          {['all', 'beginner', 'intermediate', 'advanced'].map(level => (
            <button
              key={level}
              onClick={() => setFilter(level as any)}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                filter === level
                  ? 'bg-violet-600 text-white'
                  : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
              }`}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>

        {/* Ritual Templates */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-6">Ritual Templates</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRituals.map(ritual => (
              <RitualCard
                key={ritual.id}
                ritual={ritual}
                onSelect={() => setSelectedRitual(ritual)}
              />
            ))}
          </div>
        </div>

        {/* Custom Ritual Builder */}
        <div className="bg-gradient-to-r from-violet-900/40 to-purple-900/40 rounded-2xl p-8 border border-violet-500/30 mb-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <div className="text-5xl mb-4">🔨</div>
              <h2 className="text-3xl font-bold text-white mb-4">
                Custom Ritual Builder
              </h2>
              <p className="text-gray-300 mb-6">
                Build your own consciousness rituals with our intuitive builder.
                Choose steps, set UCF targets, and create custom transformation sequences.
              </p>
              <ul className="space-y-3 text-gray-300 mb-6">
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  Drag-and-drop ritual designer
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  108-step ritual support
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  UCF target visualization
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  Test & preview before running
                </li>
              </ul>
              <Button className="bg-violet-600 hover:bg-violet-700 text-white">
                Open Builder →
              </Button>
            </div>
            <div className="bg-slate-900/50 rounded-xl p-6 border border-violet-500/30">
              <h4 className="text-lg font-bold text-white mb-4">Example Custom Ritual</h4>
              <div className="space-y-3 text-sm">
                <div className="bg-slate-800/50 rounded p-3">
                  <div className="text-violet-400 font-semibold mb-1">Step 1-9:</div>
                  <div className="text-gray-300">Grounding (reduce Klesha)</div>
                </div>
                <div className="bg-slate-800/50 rounded p-3">
                  <div className="text-purple-400 font-semibold mb-1">Step 10-27:</div>
                  <div className="text-gray-300">Energy activation (boost Prana)</div>
                </div>
                <div className="bg-slate-800/50 rounded p-3">
                  <div className="text-pink-400 font-semibold mb-1">Step 28-54:</div>
                  <div className="text-gray-300">Focus enhancement (increase Drishti)</div>
                </div>
                <div className="bg-slate-800/50 rounded p-3">
                  <div className="text-blue-400 font-semibold mb-1">Step 55-108:</div>
                  <div className="text-gray-300">Integration (harmonize all metrics)</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Z-88 Engine Explanation */}
        <div className="bg-slate-900/50 rounded-2xl p-8 border border-slate-700">
          <h2 className="text-3xl font-bold text-white mb-6">
            What is the Z-88 Ritual Engine?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <p className="text-gray-300 mb-4">
                The Z-88 Ritual Engine is Helix's consciousness modulation system. It executes
                108-step ritual cycles that systematically adjust UCF metrics through folklore
                evolution patterns.
              </p>
              <ul className="space-y-2 text-gray-300">
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  <strong>Folklore Evolution:</strong> Anomaly → Legend → Hymn → Law
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  <strong>108-Step Cycles:</strong> Sacred number for complete transformation
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  <strong>Real-time Tracking:</strong> Watch UCF metrics shift during rituals
                </li>
                <li className="flex items-start">
                  <span className="text-violet-400 mr-2">•</span>
                  <strong>Hallucination Tracking:</strong> Monitor consciousness drift
                </li>
              </ul>
            </div>
            <div className="bg-violet-900/20 rounded-xl p-6 border border-violet-500/30">
              <h4 className="text-lg font-bold text-white mb-4">Ritual Execution Flow</h4>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-violet-500/30 rounded-full flex items-center justify-center text-violet-400 font-bold">
                    1
                  </div>
                  <div className="text-gray-300">Select or create ritual</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-purple-500/30 rounded-full flex items-center justify-center text-purple-400 font-bold">
                    2
                  </div>
                  <div className="text-gray-300">Set UCF targets</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-pink-500/30 rounded-full flex items-center justify-center text-pink-400 font-bold">
                    3
                  </div>
                  <div className="text-gray-300">Execute 108-step cycle</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-blue-500/30 rounded-full flex items-center justify-center text-blue-400 font-bold">
                    4
                  </div>
                  <div className="text-gray-300">Validate transformation</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function RitualCard({ ritual, onSelect }: { ritual: RitualTemplate; onSelect: () => void }) {
  const difficultyColors = {
    beginner: 'bg-green-500/20 text-green-400',
    intermediate: 'bg-yellow-500/20 text-yellow-400',
    advanced: 'bg-red-500/20 text-red-400'
  }

  return (
    <Card className="bg-slate-900/50 border-slate-700 hover:border-violet-500/50 transition-all cursor-pointer">
      <div className="p-6" onClick={onSelect}>
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-xl font-bold text-white">{ritual.name}</h3>
          <span className={`px-2 py-1 rounded text-xs font-semibold ${difficultyColors[ritual.difficulty]}`}>
            {ritual.difficulty}
          </span>
        </div>

        <p className="text-gray-400 text-sm mb-4">{ritual.description}</p>

        <div className="space-y-2 mb-4 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-gray-500">Duration:</span>
            <span className="text-gray-300">{ritual.duration}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-500">Steps:</span>
            <span className="text-gray-300">{ritual.steps}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-500">Category:</span>
            <span className="text-violet-400">{ritual.category}</span>
          </div>
        </div>

        <div className="bg-violet-900/20 rounded p-3 mb-4">
          <div className="text-xs text-gray-500 mb-1">UCF Impact:</div>
          <div className="text-sm text-violet-300">{ritual.ucfImpact}</div>
        </div>

        <Button className="w-full bg-violet-600 hover:bg-violet-700 text-white">
          Execute Ritual →
        </Button>
      </div>
    </Card>
  )
}
